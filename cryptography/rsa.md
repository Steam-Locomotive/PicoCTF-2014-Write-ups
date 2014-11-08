## RSA - 80 (Cryptography) ##
####writeup by Oksisane

### Problem ###

A Daedalus Corp spy sent an RSA-encrypted message. We got their key data, but we're not very good at math. Can you decrypt it? [Here's](https://picoctf.com/problem-static/crypto/RSA/handout.tgz) the data. Note that the flag is not a number but a number decoded as ASCII text.

### Hint ###

This is just plain old RSA decryption.

## Answer ##

### Overview ###

Decrypt <a href="http://en.wikipedia.org/wiki/RSA_(cryptosystem)">RSA</a> given a public/private key and ciphertext.

### Details ###

 <a href="http://en.wikipedia.org/wiki/RSA_(cryptosystem)">RSA</a> is a extremely popular cryptosystems which relies on [Modular arithmetic](http://en.wikipedia.org/wiki/Modular_arithmetic) for encryption and decryption.

How does RSA work?


One of the reasons RSA is so popular is the simplicity of the cryptosystem. Here are the basic steps of RSA Encryption and Decryption.

1. Choose two (usually large) primes, p and q
2. Compute a value N = p*q, commonly reffered to as the modulus
3. Compute phi(N) = (p-1)*(q-1)
3. Choose a "public exponent value", denoted e. Typically this is 3 or 65537.
4. Compute d, the "private exponent value" which is the multiplicitve inverse of e mod(phi(N))
5. To encrypt a message m, compute m^e mod (N)
6. To decrypt a ciphertext c, compute c^d mod (N)

Opening the `key_data.txt` file we can see that the d and N values have already been provided for us, along with the ciphertext in `ciphertext.txt`. Great! All we have to do now is compute 
$$
c^d \bmod N
$$
Here is an example of this in Python, using the `pow` function.
```python
c = 0x58ae101736022f486216e290d39e839e7d02a124f725865ed1b5eea7144a4c40828bd4d14dcea967561477a516ce338f293ca86efc72a272c332c5468ef43ed5d8062152aae9484a50051d71943cf4c3249d8c4b2f6c39680cc75e58125359edd2544e89f54d2e5cbed06bb3ed61e5ca7643ebb7fa04638aa0a0f23955e5b5d9
d = 0x496747c7dceae300e22d5c3fa7fd1242bda36af8bc280f7f5e630271a92cbcbeb7ae04132a00d5fc379274cbce8c353faa891b40d087d7a4559e829e513c97467345adca3aa66550a68889cf930ecdfde706445b3f110c0cb4a81ca66f8630ed003feea59a51dc1d18a7f6301f2817cb53b1fb58b2a5ad163e9f1f9fe463b901
N = 0xb197d3afe713816582ee988b276f635800f728f118f5125de1c7c1e57f2738351de8ac643c118a5480f867b6d8756021911818e470952bd0a5262ed86b4fc4c2b7962cd197a8bd8d8ae3f821ad712a42285db67c85983581c4c39f80dbb21bf700dbd2ae9709f7e307769b5c0e624b661441c1ddb62ef1fe7684bbe61d8a19e7
pow(c,d,N)
6861258080156838161702842331923358676171560876407473046529829839343656597465212914039681453600936115970901835821496646686989354106193309238635902806952707316468225954530890939348472370864299291305467697683712618633711800447421650242202732L
```
The last step in solving this question is converting the resulting number to  a readable form. For this we again turn to Python where we can convert this number using the function below (credit to [this blog](http://jhafranco.com/2012/01/29/rsa-implementation-in-python/))
``` python
def int2Text(number, size):
    text = "".join([chr((number >> j) & 0xff)
                    for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")
```
Which gives us `Congratulations on decrypting an RSA message! Your flag is modular_arithmetics_not_so_bad_after_all`.

For further information on RSA, [here](http://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf) is a great resource.
### Flag ###

modular_arithmetics_not_so_bad_after_all

