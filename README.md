Usage
-----

 - Add "?" char in message where you want to bruteforce bits
 - Add "#CHECKSUM#" in message where you want to insert the generated checksum

 Ex : 
```
 1111100001010????#CHECKSUM#
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
                checksum=simple_crc)
bf.emit()
```