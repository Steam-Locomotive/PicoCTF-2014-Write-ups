import itertools
import struct
import socket
import json
from os import urandom

def xor(buf, key):
    """ Repeated key xor """

    encrypted = []
    for i, cr in enumerate(buf):
        k = key[i % len(key)]
        encrypted += [cr ^ k]
    return bytes(encrypted)

def secure_pad(buf):
    """ Ensure message is padded to block size. """
    key = urandom(5)
    buf = bytes([0x13, 0x33, 0x7B, 0xEE, 0xF0]) + buf
    buf = buf + urandom(16 - len(buf) % 16)
	# now we know: len(buf) % 16 == 0
    enc = xor(buf, key)
    return enc
    
def remove_pad(buf):
    """ Removes the secure padding from the msg. """
    if len(buf) > 0 and len(buf) % 16 == 0:
        encrypted_key = buf[:5]
        key = xor(encrypted_key, bytes([0x13, 0x33, 0x7B, 0xEE, 0xF0]))
        dec = xor(buf, key)
        return dec[5:]

def decode(buf):
    buf = remove_pad(buf)
    k, cookie, lmsg, msg = struct.unpack("!B2L128s", buf[:137 - len(buf)])
    return cookie, msg[:lmsg].decode('utf-8')

HOST = 'vuln2014.picoctf.com'
PORT = 21212
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))
	
c.send(struct.pack('!i', 0xAA))
resp = c.recv(1024)
cookie, msg = decode(resp)
print (msg)

c.send(secure_pad(struct.pack('!B2LHL', 0xFF, cookie, 0, 1, 0)))
resp = c.recv(1024)
cookie, msg = decode(resp)
data = json.loads(msg)
print (data)

entries = set()
entry = 0
for entry in itertools.count(0):
    c.send(secure_pad(struct.pack('!B2LHL', 0xFF, cookie, 0, 1, entry))) 
    resp = c.recv(1024)
    cookie, msg = decode(resp)
    try:
        f = json.loads(msg)
    except ValueError:
        print ('iterated through whole database')
        break

    if f['BADGE'] in entries:
        print (entry, f)
    entries.add(f['BADGE'])
    
print (entry)

