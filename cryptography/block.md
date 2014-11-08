## Block - 130 (Cryptography) ##
by ZIceZ
### Problem ###
Daedalus Corp has been using this script to encrypt it's data! We think this file contains a password to their command server. Can you crack it?
[block.py](https://picoctf.com/api/autogen/serve/block.py?static=true&pid=e1e4c8c9ccd9fc39c391da4bcd093fb2)
[encrypted](https://picoctf.com/api/autogen/serve/encrypted?static=false&pid=e1e4c8c9ccd9fc39c391da4bcd093fb2)

### Hint ###
Is double encryption twice as secure? 

## Answer ##
### Overview ###
Find the keys through brute force using meet in the middle attack.

### Details ###
The encryption used is called [substitution-permutation network](http://en.wikipedia.org/wiki/Substitution-permutation_network), and the encryption algorithm is properly implemented. However, the python program adds  "message: " to the beginning of every data being encrypted. Check out line 96 in the python program. This means that we know the text and the cipher text of the first 8 characters of the encrypted file. But we only need the first 3 characters to figure out the key because the encryption encrypts three characters at a time.

A special trait of substitution-permutation network is that even if an adversary obtain the text and the cipher text it's still impossible to figure out the key used to encrypted. Thus, we have to brute force the key, but a key in this case is only 2^24 bits long which is very brute force-able. Although, the encryption uses two keys, so one would think that 2^48 calculation is needed crack the key. This is where [meet in the middle attack](http://en.wikipedia.org/wiki/Meet-in-the-middle_attack) comes in. 

Since we have the text and the cipher, we can use meet in the middle to reduces the amount of calculation needed to crack both keys.

The encryption algorithm does this:
Text ---- encryption with key 1 ---> (something) ---- encryption with key 2 ---> Ciphertext

The attack works by creating a table of all possible value of (something) with all the possible combinations of key 1. Then we decrypt the ciphertext by guessing value of key 2 back and cross checking the resulting value with the table generated with key 1. When we get a match of what we decrypted with a value in the table generated, we will find out the correct value of key 1 and key 2.

Meet in the middle attack:
Text ----- some key 1 ----> (something) == (something) <------ some key 2 ---- Ciphertext

Instead of doing 2^48 calculations, we have essentially done two 2^24 calculations instead which is only 2^25 calculations.

My brute forcing python code:
```python
from time import ctime
from pickle import dump
print (ctime(), 'start')

a = {}
for i in xrange(0, 16**6):
    a[encrypt_data('message: ', i)] = i

print (ctime(), 'gen dict')
with open('int.txt', 'w+') as f:
    dump(a, f)
print (ctime(), 'dump dict')

f = '\xa1\x98\xa4\x03\x85\x81\xc5\x10\x9e'
counter = 0
for i in xrange(0, 16**6):
    try:
        print ('{0:d}, {1:d}'.format(a[decrypt_data(f, i)], i))
    except KeyError:
        pass
    if i % 16**5 == 0:
        print (ctime(), str(i) + ' iterations'
```
With the keys, it's trivial to decrypt the file and get the flag. 


