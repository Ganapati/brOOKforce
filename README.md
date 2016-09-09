Usage
-----

 - Add "?" char in message where you want to bruteforce bits
 - Add "#CHECKSUM#" in message where you want to insert the generated checksum
 - Support Raw or Binary message

Example Binary: 
```
 1111100001010????11010#CHECKSUM#
```

Example Raw:
```
 FOOBAR????11010#CHECKSUM#
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
                charset="01"
                checksum=simple_crc)

bf.emit()
```

Usage example
-------------

(Static checksum, always return "01")

Binary injection :
```
~/s/brOOKforce ❯❯❯ sudo python ./brOOKforce.py --message "#CHECKSUM#001??00111" --charset "01" -v
MESSAGE : 'Hp' (10010001110000)
MESSAGE : 'Jp' (10010101110000)
MESSAGE : 'Lp' (10011001110000)
MESSAGE : 'Np' (10011101110000)
```

Non Binary injection :
```
~/s/brOOKforce ❯❯❯ sudo python ./brOOKforce.py --message "#CHECKSUM#AB??EF" --charset "CD" -v
MESSAGE : '01ABCCEF' (110000110001100000110000101000011100001110001011000110)
MESSAGE : '01ABCDEF' (110000110001100000110000101000011100010010001011000110)
MESSAGE : '01ABDCEF' (110000110001100000110000101000100100001110001011000110)
MESSAGE : '01ABDDEF' (110000110001100000110000101000100100010010001011000110)
```