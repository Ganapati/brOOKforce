Usage
-----

 - Add "?" char in message where you want to bruteforce bits
 - Add "#CHECKSUM#" in message where you want to insert the generated checksum

 Example : 
```
 1111100001010????11010#CHECKSUM#
```

Custom checksum
---------------
```python
from brOOKforce import Brookforce

def simple_crc(message):
    # xor all bytes (before #CHECKSUM#)
    message = bitstring.BitArray(bin=message[:-10]).tobytes()
    crc = "\x00"
    for _ in message:
        crc = chr(ord(crc)^ord(_))
    return ''.join(format(ord(x), 'b') for x in crc)

bf = Brookforce(frequency=433000000, 
                rate=25000, 
                message="1100????#CHECKSUM#", 
                preamble="11110000",
                repeat=2,
                checksum=simple_crc)

bf.emit()
```

Usage example
-----------
```
>>> sudo python ./brOOKforce.py -m "1111????#CHECKSUM#" -v
MESSAGE : 1111000011110000
MESSAGE : 1111000111110001
MESSAGE : 1111001011110010
MESSAGE : 1111001111110011
MESSAGE : 1111010011110100
MESSAGE : 1111010111110101
MESSAGE : 1111011011110110
MESSAGE : 1111011111110111
MESSAGE : 1111100011111000
MESSAGE : 1111100111111001
MESSAGE : 1111101011111010
MESSAGE : 1111101111111011
MESSAGE : 1111110011111100
MESSAGE : 1111110111111101
MESSAGE : 1111111011111110
MESSAGE : 1111111111111111
```