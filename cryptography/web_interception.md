## Web Interception - 140 (Cryptography)
#### Writeup by Gladius Maximus

Created: 2014-11-08 00:49:29

Last modified: 2014-11-09 23:09:56


Created: 2014-11-08 00:49:29

Last modified: 2014-11-09 23:02:57


Created: 2014-11-08 00:49:29

Last modified: 2014-11-09 23:02:50


Created: 2014-11-08 00:49:29

Last modified: 2014-11-09 23:02:46


Created: 2014-11-08 00:49:29

Last modified: 2014-11-09 23:01:35


### Problem ###

We were able to get some code running in a Daedalus browser. Unfortunately we
can't quite get it to send us a cookie for its internal login page
ourselves... But we can make it make requests that we can see, and it seems to
be encrypting using ECB mode. See [here](server.py) for more details about what
we can get. It's running at vuln2014.picoctf.com:65414. Can you get us the
cookie?

### Hint ###

In ECB mode, the same plaintext block appearing in two different places leads
to the same ciphertext block appearing in both places. Can you figure out how
to use this, and the encryption oracle that you have, to decrypt the cookies
one byte at a time?

## Answer ##

### Overview ###

The server prepends the user input with 'GET /' and then appends a secret
message. It encrypts this and sends it back to you. The object is to get the
secrete message. The server encrypts in blocks of 16 bytes. Change the user
input until it equals the response from the server. Guessing a whole block at
a time is hard, but if you know the first 15 bytes and are guessing for the
last 1 byte, it is doable.

### Details ###

The server concatenates a 5 byte string, your input (given as a hexidecimal
string, where a pair of hexidecimal digits reperesent a character), and then
the secret data. it encrypts all of that data, and sends it back (as a
hexidecimal string) with a newline tacked on. I glean this from the following
piece of code:

```python
def oracle(s):
  return AESCipher(key).encrypt(pkcs7_pad('GET /' + s.decode('hex') + secret_data))

...

    data = self.request.recv(4096).strip('\n')
    self.request.send(oracle(data).encode('hex') + '\n')
    self.request.close()
```

Here is the code required to communicate with the server that abstracts away
all of the monkey business away. It is often a good first step to abstract all
of the irrelevant parts of a problem away:

```python
# client side code
import socket

HOST = 'vuln2014.picoctf.com'
PORT = 65414

def send(string):
    assert len(string) < 4096 / 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.recv(4096)
    sock.sendall(string.encode('hex'))
    resp = sock.recv(4096).strip('\n').decode('hex')
    sock.close()
    return resp
```

If we look at the encryption algorithm on the server, you will notice they are
using PyCrypto. The
[PyCrypto documentation for AES](https://www.dlitz.net/software/pycrypto/api/current/)
says that the encryption works in blocks of 16 bytes. If two plaintext blocks
are identical, then they will produce identical ciphertext blocks. This is
called electronic codebook mode (ECB) of the AES cipher. You can read more
about ECB and why it is insecure
[here](http://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_.28ECB.29). I
hope to be able to attack this cipher by manipulating


(My send function takes care of encoding to hex and all that jazz.) I can find
out the length of the secret. If I send an 8, 9, 10, or 11 long string, the
length of the response is 80 bytes long. If I send a 12, 13, 14, or 15 long
string, the length of the response is 76. Sending 11 bytes must make the
message fit perfectly in 80 bytes. Sending 12 bytes must make it go one over
80, which needs another block (of 16 bytes), so the returned  will end up being
96 characters long. 80 bytes - 5 bytes (for 'GET /') - 11 bytes (for user
input) equals 64 bytes.


Here is the interesting part: if I send 11 bytes of filler text, I can finish
off the block started by `GET /`. Then after that, I can send 15 bytes of
`A`. Then I can send 15 more `A`. Then the block will look like:

    G E T   / A A A A A A A A A A | A A A A A A A A A A A A A A A A A A A A 1 | 2 3 4 ...
    ^                             ^                                           ^
	First block                   Second block                                Third block

where the | denotes a border of the blocks, and the number 1 represents the
first character of the secret, 2 the second character, and so on. Once I have
sent this request, I should store the second block of the result.

Now lets say I send another block. This time I send 15 `A` followed by 15 more
`A`, but after that put in a character, call it `i`. that looks like this:

    G E T   / A A A A A A A A A A | A A A A A A A A A A A A A A A A A A A A i | 1 2 3 ...
    ^                             ^                                           ^
	First block                   Second block                                Third block

If `i` is the first character of the message, they should encrypt to the same
thing. Thus, I can set a counter to go through from i = 0 to 255 and break when
the second block of the encrypted text equals the second block of the old
encrypted text. This can give me the first byte of the message.

Now I can do this for the second one too. I need to record the second block of this
result:

    G E T   / A A A A A A A A A A | A A A A A A A A A A A A A A A A A A A 1 2 | 3 4 5 ...
    ^                             ^                                           ^
	First block                   Second block                                Third block

And then since I know the first character of the secret from the previous round, I
can put that in the message after the As

    G E T   / A A A A A A A A A A | A A A A A A A A A A A A A A A A A A A 1 i | 3 4 5 ...
    ^                             ^                                           ^
	First block                   Second block                                Third block

Then I iterate through I until it encrypts to the same thing, and I have the
second byte. Writing this up looks like this:

```python
alphabet = '''_abcdefghijklmnopqrstuvwxyz\n\rABCDEFGHIJKLMNOPQRSTUVWXYZ/.\t !"#$%&\'()*+,-0123456789:;<=>?@[\\]^`{|}~\x7f\x80\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'''

for i in range(0, 16):
    # one iteration takes about 20 seconds
    target = send('A' * (11 + 15 - i))[16:32]
    for test_char in alphabet:
        resp = send('A' * (11 + 15 - i) + known + test_char)[16:32]
        if resp == target:
            known += test_char
            print (repr(known))
            break
    else:
        print ('no answer for', i)
```

That should yield the first block of the secret: `' HTTP/1.1\r\nCooki'`. That
looks a lot like an HTTP request. Seeing this, I have written the alphabet that
includes all ascii characters in the order of prominence (as predicted). This
new alphabet increases the speed at which we are ablet o get characters,
because the common characters are at the front.

If you want to start getting the second block, you simply look at the third
block when it has 15 characters you know, and 1 you don't. You have to get the
key sequentially. Lets say you already know 15 letters via the method described
above.

    G E T   / A A A A A A A A A A | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 | 17 18 ...
    ^                             ^                                           ^
	First block                   Second block                                Third block

Then you remember the second block of the return. Rember that you already know the first 15 letters from the previous method. You simply send those 15 letters back to the server plus another letter.

    G E T   / A A A A A A A A A A | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 i | 17 18 ...
    ^                             ^                                         ^
	First block                   Second block                              Third block

```python
for i in range(16, 32):
    target = send('A' * (11 + 15 + 16 - i))[32:48]
    for test_char in alphabet:
            resp = send('A' * (11 + 15 + 16 - i) + known + test_char)[32:48]
            if resp == target:
                    known += test_char
                    print (repr(known))
                    break
    else:
        print ('no answer for', i)
```

[Here](web_interception.py) is the complete script that implements all of the
concepts from this document. It gives this funny-looking output as it gets the
flag, piece by piece:

```
' '
' H'
' HT'
' HTT'
' HTTP'
' HTTP/'
' HTTP/1'
' HTTP/1.'
' HTTP/1.1'
' HTTP/1.1\r'
' HTTP/1.1\r\n'
' HTTP/1.1\r\nC'
' HTTP/1.1\r\nCo'
' HTTP/1.1\r\nCoo'
' HTTP/1.1\r\nCook'
' HTTP/1.1\r\nCooki'
' HTTP/1.1\r\nCookie'
' HTTP/1.1\r\nCookie:'
' HTTP/1.1\r\nCookie: '
' HTTP/1.1\r\nCookie: f'
' HTTP/1.1\r\nCookie: fl'
' HTTP/1.1\r\nCookie: fla'
' HTTP/1.1\r\nCookie: flag'
' HTTP/1.1\r\nCookie: flag='
' HTTP/1.1\r\nCookie: flag=c'
' HTTP/1.1\r\nCookie: flag=co'
' HTTP/1.1\r\nCookie: flag=con'
' HTTP/1.1\r\nCookie: flag=cong'
' HTTP/1.1\r\nCookie: flag=congr'
' HTTP/1.1\r\nCookie: flag=congra'
' HTTP/1.1\r\nCookie: flag=congrat'
' HTTP/1.1\r\nCookie: flag=congrats'
' HTTP/1.1\r\nCookie: flag=congrats_'
' HTTP/1.1\r\nCookie: flag=congrats_o'
' HTTP/1.1\r\nCookie: flag=congrats_on'
' HTTP/1.1\r\nCookie: flag=congrats_on_'
' HTTP/1.1\r\nCookie: flag=congrats_on_y'
' HTTP/1.1\r\nCookie: flag=congrats_on_yo'
' HTTP/1.1\r\nCookie: flag=congrats_on_you'
' HTTP/1.1\r\nCookie: flag=congrats_on_your'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_f'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_fi'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_fir'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_firs'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_e'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ec'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_d'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_de'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_dec'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decr'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decry'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryp'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decrypt'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decrypti'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryptio'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryption'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryption\r'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryption\r\n'
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryption\r\n\x01'
no answer for 63
' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryption\r\n\x01'
```

I am not sure why it does not find an answer for 63. Perhaps I got the length of the message wrong.

### Flag ###

    congrats_on_your_first_ecb_decryption

