## RSA Mistakes - 200 (Cryptography) ##
####Writeup by ZIceZ
Created: 2014-11-07 23:22:41
Last modified: 2014-11-09 22:28:22
### Problem ###
Daedalus Corp seems to have had a very weird way of broadcasting some secret data. [We managed to find the server code that broadcasted it, and one of our routers caught some of their traffic](https://picoctf.com/problem-static/crypto/rsa-mistakes/handout.zip) - can you find the secret data? We think someone may have requested the secret using someone else's user id by accident, but we're not sure.

### Hint ###
Two of these messages use the same public key, and are related in a useful way.

## Answer ##
### Overview ###
Use [Franklin-Reiter Related Message Attack](http://en.wikipedia.org/wiki/Coppersmith%27s_Attack#Franklin-Reiter_Related_Message_Attack).
###Details###
The data recovered from the .pcap file contains a series of public keys and messages, and a python program. The python program reviews that the original message was transformed based on the User ID before being encrypted and broadcast. The transformation is:
$$ID*(message) + ID^2$$

From the other file that contains the series of public key, user ID, and message, it turns out that an employee of Daedalus Corp requested the secret message twice but on the second time he accidentally used another person ID.

His unfortunate accident gives us two messages that are related to each other, and are encrypted by the same public key.

Pub key 2
fd2adfc8f9e88d3f31941e82bef75f6f9afcbba4ba2fc19e71aab2bf5eb3dbbfb1ff3e84b6a4900f472cc9450205d2062fa6e532530938ffb9e144e4f9307d8a2ebd01ae578fd10699475491218709cfa0aa1bfbd7f2ebc5151ce9c7e7256f14915a52d235625342c7d052de0521341e00db5748bcad592b82423c556f1c1051 **3 37** (this is the User ID)

Msg 2
0x81579ec88d73deaf602426946939f0339fed44be1b318305e1ab8d4d77a8e1dd7c67ea9cbac059ef06dd7bb91648314924d65165ec66065f4af96f7b4ce53f8edac10775e0d82660aa98ca62125699f7809dac8cf1fc8d44a09cc44f0d04ee318fb0015e5d7dcd7a23f6a5d3b1dbbdf8aab207245edf079d71c6ef5b3fc04416L

Pub key 5
fd2adfc8f9e88d3f31941e82bef75f6f9afcbba4ba2fc19e71aab2bf5eb3dbbfb1ff3e84b6a4900f472cc9450205d2062fa6e532530938ffb9e144e4f9307d8a2ebd01ae578fd10699475491218709cfa0aa1bfbd7f2ebc5151ce9c7e7256f14915a52d235625342c7d052de0521341e00db5748bcad592b82423c556f1c1051 **3 52** (this is the User ID)

Msg 5
0x1348effb7ff42372122f372020b9b22c8e053e048c72258ba7a2606c82129d1688ae6e0df7d4fb97b1009e7a3215aca9089a4dfd6e81351d81b3f4e1b358504f024892302cd72f51000f1664b2de9578fbb284427b04ef0a38135751864541515eada61b4c72e57382cf901922094b3fe0b5ebbdbac16dc572c392f6c9fbd01eL


OK, that's the set up. Now to the exploit. The Franklin-Reiter Related Message Attack uses known fixed relationship between two messages to exploit
$$
M_1 = a*M_2 + b \\
M_1^e \bmod N = (a*M_2+b)^e \bmod N
$$
We also have:
$$
M_1^e \bmod N = C_1\\
M_2^e \bmod N = C_2
$$
Then let set:
$$
g(x) = x^e - C_2 \bmod N \\
h(x) = (a*x+b)^e - C_1 \bmod N
$$
So when $x = M_2$, g(x) and h(x) equal 0. Thus, $x -M_2$ is a factor to the two equation above. Therefore the GCD of the two equations above should return the factor $x-M_2$, and then $M_2$ and $M_1$ can be found.


What we have then is two messages related to each other by some coefficient:
$$37*(message)+37^2 = a*(52*(message)+52^2) + b$$
Solve for a and b:
$a = 37/52$
$b = -555$
Since fractions are not permissible in modulus, we use the multiplicative inverse instead to represent $a$. Also, don't forget that this only solves for the transformed message. Reverse the transformation before decoding.

My code in Sage:
```python
def n2s(n):
    s = hex(n)[2:-1]
    if len(s) % 2 != 0:
        s = '0' + s
    return s.decode('hex')
n = 0xfd2adfc8f9e88d3f31941e82bef75f6f9afcbba4ba2fc19e71aab2bf5eb3dbbfb1ff3e84b6a4900f472cc9450205d2062fa6e532530938ffb9e144e4f9307d8a2ebd01ae578fd10699475491218709cfa0aa1bfbd7f2ebc5151ce9c7e7256f14915a52d235625342c7d052de0521341e00db5748bcad592b82423c556f1c1051L
c1 = 0x81579ec88d73deaf602426946939f0339fed44be1b318305e1ab8d4d77a8e1dd7c67ea9cbac059ef06dd7bb91648314924d65165ec66065f4af96f7b4ce53f8edac10775e0d82660aa98ca62125699f7809dac8cf1fc8d44a09cc44f0d04ee318fb0015e5d7dcd7a23f6a5d3b1dbbdf8aab207245edf079d71c6ef5b3fc04416L
c2 = 0x1348effb7ff42372122f372020b9b22c8e053e048c72258ba7a2606c82129d1688ae6e0df7d4fb97b1009e7a3215aca9089a4dfd6e81351d81b3f4e1b358504f024892302cd72f51000f1664b2de9578fbb284427b04ef0a38135751864541515eada61b4c72e57382cf901922094b3fe0b5ebbdbac16dc572c392f6c9fbd01eL
e = 3
a1 = 37/52
b1 = -555
actuala = inverse_mod(52, n)
x = PolynomialRing(ZZ.quo(n*ZZ), 'x').gen()
f=(x*actuala*37+b1)^e-c1
g=x^e-c2
a = f
b = g
messagemess = 0
run = True
while run:
    r = a % b
    if r == 0:
        print 'FOUND %s' % rp
        c = rp.coeffs()
        messagemess = -pow(c[1], -1, n) * c[0]
        run = False
    rp = r
    a, b = b, r
    i += 1
realmessage = messagemess*actuala-b1
n2s(int(realmessage))
```
Which reveals the message: 'Wow! Your flag is: did_you_know_you_can_sometimes_gcd_outside_a_euclidean_domaipi'
### Flag ###
    did_you_know_you_can_sometimes_gcd_outside_a_euclidean_domaipi

