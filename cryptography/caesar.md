# Caesar - 20 (Cryptography) ##
####Writeup by evantey14
Created: 2014-11-07 22:24:00
Last modified: 2014-11-09 22:28:33

### Problem
You find an encrypted message written on the documents. Can you decrypt it?
[encrypted.txt](https://picoctf.com/api/autogen/serve/encrypted.txt?static=false&pid=6d086db90583fcea884ecf10f2dc6319)

###Hint

Is there a cipher named the same as the title of this problem?

##Answer

###Overview

Decrypt the ciphertext with a Caesar cipher

###Details
The namesake Caesar cipher is a simple cipher where each letter in the plaintext (the original message) is substituted with the letter N characters down the alphabet. This means if N=5, an `e` would encoded as a `j`, and a `y` would wrap around to become a `d`.

In the problem, we are given a cipher text (the encoded message)

`xliwigvixtewwtlvewimwewtlonvlbuuihprubmdpcomvxkjxkd`

but we don't know what N was used to encrypt the plaintext. Lucky for us, we can easily decrypt a Caesar cipher since there are only 25 possible values for N. Remember that we are decrypting, so we need to shift each letter in the ciphertext to the left until we find a sensible plaintext. Because the Caesar cipher wraps around, shifting N to the left is the same as shifting 26-N to the right (i.e. encrypting a second time, with a complementary N) So to decrypt the `j` from our earlier example, we can shift 26-5=21 to the right to get `e`.

Using an [online tool](http://rumkin.com/tools/cipher/caesar.php) that shifts text by an N of our choice, we can paste in the ciphertext, and cycle through all N's until we find a sensible plaintext.

For us, this happens at N=22, where we see
`thesecretpassphraseisasphkjrhxqqedlnqxizlykirtgftgz`.

###Flag
    asphkjrhxqqedlnqxizlykirtgftgz

