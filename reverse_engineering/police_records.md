## Police Records - 140 (reverse engineering) ##
#### writeup by Gladius Maximus

### Problem ###

A Theseus double agent has infiltrated the police force but the police won't
give you access to their directory information. Thankfully you found the
[source code](directory_server.py) to their directory server. Write a client to
interact with the server and find the duplicated badge number! The flag is the
badge number.

The server is running on `vuln2014.picoctf.com:21212`.

### Hint ###

You are going to have to understand
[structs](https://docs.python.org/2/library/struct.html).

## Answer ##

### Overview ###

Write a client in a language of choice (python for me) that interacts with the
server and grabs data. You have to look at the source code for the server and
reverse engineer a proper client. 

### Details ###

A struct is a way to send C primitives as a string. C primitives are like char,
float, long, float, unsigned int, etc. The function `struct.pack` takes in a
format string and data and returns the packed data as a string according to the format string. It is
complimentary to `struct.unpack`, which does the opposite.

#### Accessing the server ####

If you look at their code,

```python
# from directory_server.py
data = self.request.recv(1024)
...
code = struct.unpack("!i", data)[0]
if code == 0xAA:
    cookie = self.secure_send(b"WELCOME TO THE POLICE RECORDS DIRECTORY")
    access = True
else:
    raise Exception
```

To connect, you have to send `0xAA` as an integer. Lets get all of the TCP
connection code going. Make a script called `directory_client.py`. When
executing `directory_client.py`, make sure to use python3. Soon we will be
messing with string encodings and such.

```python
# from directory_client.py
import struct
import socket
import json
from os import urandom

HOST = 'vuln2014.picoctf.com'
PORT = 21212
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))

c.send(struct.pack('!i', 0xAA))
```

Now I turn my attention to the `secure_send` function. The server uses it to
send stuff to me

```python
# directory_server.py
def secure_send(self, msg):
    """ Sends msg back to the client securely. """

    cookie = generate_cookie()
    data = struct.pack("!B2L128s", 0xFF, cookie, len(msg), msg)
    encrypted = secure_pad(data)
    self.request.sendall(encrypted)
    return cookie
...
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
        return dec[5:20]
```
<!---
So the server sends a message of 0xFF, a cookie, the length of the
message, and then the actual message. The message itself is padded with the
same five bytes each time. Then bytes are added at the end, until the length of
the message is a multiple of 16. It xors that with a random key.

Intermission for cryptography. For any $a$ and $b$, $a \oplus b$ \oplus b = a$
($\oplus$ stands for xor). xor has the special property that if $a \oplus b =
c$, then $a \oplus c = b$. This means xor is its own inverse. That will come in
handy later. 

If I want to remove the padding, since I know exactly the first five bytes, I
xor them with the first five elements of buffer. Since the ciphertext, $c$, was
made by xoring the message, $m$, with the key, $k$, we have $c = m \oplus
k$. If we know the first part of the message, using the inverse property of xor
stated above, we have $m \oplus c = k$. So we can get the key if part of the
message and part of the ciphertext are known. The `remove_pad` function does
exactly this. It gets the first five bytes of the message, and xors them with
the plaintext they represent. The client and the server both need to always
start the message with known plaintext, so the client can decrypt the
messages. Then we use that key to decrypt the message.
-->

Here is how I will decode the messages. I am using `remove_pad` from the
server's source code. Since `recv` pads the message with null characters, I
want to cut the message to the right size `msg[:lmsg]`.

```python
# directory_client.py
def decode(buf):
    buf = remove_pad(buf)
    k, cookie, lmsg, msg = struct.unpack("!B2L128s", buf[:137 - len(buf)])
    return cookie, msg[:lmsg].decode('utf-8')
```

Now we can interpret messages from the server.

```python
# directory_client.py
...
c.send(struct.pack('!i', 0xAA))
resp = c.recv(1024)
cookie, msg = decode(resp)
print (msg)
```

You should see `WELCOME TO THE POLICE RECORDS DIRECTORY`. Now lets look at the
server's code for what we want to do next.

#### Accessing data on the server ####

```python
# directory_server.py
decrypted = remove_pad(data)
...
magic, user_cookie, badge, cmd, entry = \
        struct.unpack("!B2LHL", decrypted)
if magic != 0xFF or user_cookie != cookie:
    self.request.sendall(b"INSECURE REQUEST")
    running = False
else:
    ...
```

We want to go to the else branch of the if statement. We need magic to equal
`0xFF`, and `user_cookie` to equal the previous cookie. We also need to make sure
that it we are using `secure_pad`, since the server is using `remove_pad` To
implement this, we need to do `c.send(secure_pad(struct.pack('!B2LHL', 0xFF,
cookie, _, _, _)))`

We still need to fillin the blanks. To do that, we need to see how badge, cmd,
and entry are used in the server's code.

```python
# directory_server.py
if cmd == 1:
    officer = self.get_officer_data(entry)
    if officer:
        cookie = self.secure_send(officer)
    else:
        cookie = self.secure_send(b"INVALID ENTRY -- OFFICER DOES NOT EXIST")
else:
    cookie = self.secure_send(b"INVALID COMMAND")
```

This means we want cmd to equal 1, and entry to be 0. Badge is not used
anywhere in the program, so I will set it to 0. Now we have
`c.send(secure_pad(struct.pack('!B2LHL', 0xFF, cookie, 0, 1, _)))`. One last
blank to fill in.

```python
# directory_server.py
def get_officer_data(self, entry):
    """ Retrieve binary format of officer. """

    if 0 <= entry and entry < len(self.OFFICERS):
        return json.dumps(self.OFFICERS[entry]).encode("utf-8")
    return None
```

Zero is always a safe value, because every with data has a zeroeth value. Let
us set entry to zero.

```python
# directory_client.py
c.send(secure_pad(struct.pack('!B2LHL', 0xFF, cookie, 0, 1, 0)))
resp = c.recv(1024)
cookie, msg = decode(resp)
data = json.loads(msg)
print (data)
```

Your output should look something like this.

    {'NAME': 'Emmaline Jarnagin', 'BADGE': 2297648, 'ACTIVE': True, 'TITLE':
    'JANITOR'}

#### Finding the duplicated badge from the data ####

Now we write python code to put it all together. This is the fun part.

```python
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
```

You can see the whole script [here](directory_client.py). The 903th entry is
duplicated.

#### Flag ####

1430758
