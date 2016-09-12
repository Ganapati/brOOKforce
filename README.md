Usage
-----

 - Add "?" char in message where you want to bruteforce bits or char
 - If checksum is needed, add "#CHECKSUM#" in message where you want to insert the generated value and defined a checksum function
 - Support Raw or Binary message

Examples
--------
(Static checksum, always return 01)

Binary: 
```
>>> sudo python ./brOOKforce.py -m "#CHECKSUM#01??10010111010" -c "01" -v

MESSAGE : 'R]\x00'
MESSAGE : 'V]\x00'
MESSAGE : 'Z]\x00'
MESSAGE : '^]\x00'
```

Ascii:
```
>>> sudo python ./brOOKforce.py -m "#CHECKSUM#FOOB??RBAZ" -c "AR" -v

MESSAGE : '01FOOBAARBAZ'
MESSAGE : '01FOOBARRBAZ'
MESSAGE : '01FOOBRARBAZ'
MESSAGE : '01FOOBRRRBAZ'
```

Raw
```
>>> sudo python ./brOOKforce.py -m "#CHECKSUM#\x02\x0?\xff\xff\xff\xff" -c "0123456789abcdef" -v

MESSAGE : '01\x02\x00\xff\xff\xff\xff'
MESSAGE : '01\x02\x01\xff\xff\xff\xff'
MESSAGE : '01\x02\x02\xff\xff\xff\xff'
MESSAGE : '01\x02\x03\xff\xff\xff\xff'
MESSAGE : '01\x02\x04\xff\xff\xff\xff'
MESSAGE : '01\x02\x05\xff\xff\xff\xff'
MESSAGE : '01\x02\x06\xff\xff\xff\xff'
MESSAGE : '01\x02\x07\xff\xff\xff\xff'
MESSAGE : '01\x02\x08\xff\xff\xff\xff'
MESSAGE : '01\x02\t\xff\xff\xff\xff'
MESSAGE : '01\x02\n\xff\xff\xff\xff'
MESSAGE : '01\x02\x0b\xff\xff\xff\xff'
MESSAGE : '01\x02\x0c\xff\xff\xff\xff'
MESSAGE : '01\x02\r\xff\xff\xff\xff'
MESSAGE : '01\x02\x0e\xff\xff\xff\xff'
MESSAGE : '01\x02\x0f\xff\xff\xff\xff'
```

Custom checksum
---------------
```python
from brOOKforce import Brookforce

def simple_crc(message):
    # xor all bytes (before #CHECKSUM#)
    payload = message[:-10]
    crc = "\x00"
    for _ in payload:
        crc = chr(ord(crc)^ord(_))
    return crc

bf = Brookforce(frequency=433000000, 
                rate=25000, 
                message="1100????#CHECKSUM#", 
                preamble="11110000",
                repeat=2,
                charset="01"
                checksum=simple_crc)

bf.emit()
```