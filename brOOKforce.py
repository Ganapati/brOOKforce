from rflib import *
import time
import bitstring
import argparse
import itertools

class Brookforce(object):
    def __init__(self, frequency=None, rate=None, preamble=None, message=None, repeat=1, checksum=None, charset="01", verbose=False):
        self.frequency = frequency
        self.rate = rate
        self.verbose = verbose
        self.preamble = preamble
        self.message = message
        self.checksum = checksum
        self.repeat = repeat
        self.charset = charset

    def emit(self):

        d = RfCat()
        d.setMdmModulation(MOD_ASK_OOK)
        d.setFreq(self.frequency)
        d.setMaxPower()
        d.setMdmDRate(self.rate)

        preamble = self.build_preamble()
        for message in self.build_message():

            d.makePktFLEN(len(preamble))
            d.RFxmit(preamble)
            d.makePktFLEN(len(message))
                
            for i in range(self.repeat):
                d.RFxmit(message)
               
            time.sleep(0.001)

        d.setModeIDLE()

    def build_preamble(self):
        return bitstring.BitArray(bin=self.preamble).tobytes()

    def build_message(self):
        frmt_message = self.message.replace("?", "%s")
        nb_bf = frmt_message.count("%s")
        for combination in itertools.product(self.charset, repeat=nb_bf):
            final_message = frmt_message % combination
            
            if "#CHECKSUM#" in self.message:
                if self.checksum is not None:
                    checksum = self.checksum(final_message)
                    final_message = final_message.replace("#CHECKSUM#", checksum)
                else:
                    print("Warning, checksum in message, but no checksum method defined")
                    final_message = final_message.replace("#CHECKSUM#", "")
            
            if all(c in '01' for c in final_message):
                binary_message = final_message
                final_message = bitstring.BitArray(bin=final_message).tobytes()
                if self.verbose:
                    print 'MESSAGE : %s (%s)' % (repr(final_message), binary_message)
            else:
                if self.verbose:
                    print 'MESSAGE : %s (%s)' % (repr(final_message), ''.join(format(ord(x), 'b') for x in final_message))
            
            yield final_message

if __name__ == "__main__":
    """ Test method (example)
    """
    parser=argparse.ArgumentParser(description="Bruteforce OOK/ASK")
    parser.add_argument('-p', '--preamble', help='message preamble', default="")
    parser.add_argument('-c', '--charset', help='bruteforce charset', default="01")
    parser.add_argument('-m', '--message', help='message', default=None)
    parser.add_argument('-f', '--frequency', help='frequency', default=433000000, type=int)
    parser.add_argument('-r', '--rate', help='rate', default=2500, type=int)
    parser.add_argument('-x', '--repeat', help='repeat', default=1, type=int)
    parser.add_argument('-v', '--verbose', help='verbose mode', action="store_true")

    args = vars(parser.parse_args())

    def simple_crc(message):
        return "01" # static crc, write your own here !

    bf = Brookforce(preamble=args['preamble'], 
                    message=args['message'],
                    frequency=args['frequency'],
                    rate=args['rate'],
                    repeat=args['repeat'],
                    verbose=args['verbose'],
                    charset=args['charset'],
                    checksum=simple_crc)
    
    bf.emit()