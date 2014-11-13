## ZOR - 50 (Cryptography) ##
#### Writeup by Gladius Maximus

### Problem ###

Daedalus has encrypted their blueprints! Can you get us the password?

[ZOR.py](https://picoctf.com/api/autogen/serve/ZOR.py?static=true&pid=75648af599de2ecff06e8b74e5fd15c2)

[encrypted](https://picoctf.com/api/autogen/serve/encrypted?static=false&pid=75648af599de2ecff06e8b74e5fd15c2)

### Hint ###

The password gets reduced to a one byte XOR key. That's only 256 possible keys!

## Answer ##

### Overview ###

Use a frequency analysis and make the most common character in the cipher text
decrypt to space (the most common character in most plaintexts). Ignore th
`password` function and XOR the data directly.

### Details ###

XOR has the rare property that it is its own inverse. If $$ m \oplus k = c $$,
then $$ m \oplus c = k $$. This means if we have a known piece of the plaintext
message $$ m $$, and a known piece of the ciphertext, $$ c $$, (and we know it is an XOR
encryption), then we can deduce the key, $$ k $$.

The most common character in the cipher text probably decodes to the most
common character in English. The most common character in most English
plaintexts is usually space. It occurs about twice as often as `e` according to
[some pages](http://www.data-compression.com/english.html). The most common
character in cipher text is a bit harder to get. Luckily, python has a really
nice
[`Counter` class](https://docs.python.org/2/library/collections.html#collections.Counter).

```python
from collections import Counter

frequency = Counter()
with open('encrypted', 'r') as f:
    data = f.read()
    for ch in data:
        frequency[ch] += 1

c = frequency.most_common(10)[0][0]
m = ' '
print (repr(a) + ' decrypts to ' + repr(m))
```

Output:

```
'\xb2' decrypts to ' '
```

This gets the most common characters in the cipher text, `c`. We want to find a
`k` such that `m` decrypts to `c`. In other words find $$ k $$ such that $$ m
\oplus k = c $$. We have stated above that XOR is its own inverse, so $$ m
\oplus c = k $$.

```python
def xor(input_data, key):
    result = ""
    for ch in input_data:
        result += chr(ord(ch) ^ ord(key))
    return result

k = xor(c, m)
```

Now that we know k, we can decrypt the whole message.

```python
print (xor(data, k))
```

Output:

```
This message is for Daedalus Corporation only. Our blueprints for the
Cyborg are protected with a password. That password is
d01f2c9f64ed5bdfce6dbfcf3da5db
```

Notice we never actually use the `encrypt` or `decrypt` function we are
provided with. Guessing the password for these is a bit harder. The hint says
"that's only 256 possible keys." They mean instead of trying to guess the
password which has several million (possibly infinite) keys, we can guess the
key for the xor part, which has only 256 possible keys. To do this, we just did
a simple frequency analysis. The entire script described in this write-up can
be found [here](zor_crack.py).

### Flag ###

    d01f2c9f64ed5bdfce6dbfcf3da5db
