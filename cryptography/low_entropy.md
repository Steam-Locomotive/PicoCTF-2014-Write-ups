## Low Entropy - 110 (Cryptography) ##
#### Writeup by Oksisane

### Problem ###

Daedalus Corp's spy in Thyrin Labs seems to sometimes use an encrypted drop box for their messages. We intercepted one of their messages, but we don't seem to be able to decrypt it. Fortunately, we have the source and the address of their key generation server: maybe there's a way to use that to decrypt their message? Unfortunately, we don't have their list of cached primes...

Their source, and our intercepted message, are [here](https://picoctf.com/problem-static/crypto/low-entropy/handout.zip). The key generation service is running at `vuln2014.picoctf.com:51818`.

### Hint ###

We're pretty sure that 30 total possible primes is low enough that we should be able to correlate different keys somehow...


## Answer ##

### Overview ###

Factor the given publickey since we have only 30 primes, then use the factors to compute the private key and decrypt the message.

### Details ###
For the purposes of this solution, I am going to assume you are familiar with the basics of the RSA encryption/decryption

In this problem we are given a server which generates RSA moduli and are told that there are only 30 possible primes that the server uses to generate them. First, we copy the given modulus `0xc20a1d8b3903e1864d14a4d1f32ce57e4665fc5683960d2f7c0f30d5d247f5fa264fa66b49e801943ab68be3d9a4b393ae22963888bf145f07101616e62e0db2b04644524516c966d8923acf12af049a1d9d6fe3e786763613ee9b8f541291dcf8f0ac9dccc5d47565ef332d466bc80dc5763f1b1139f14d3c0bae072725815f` and the cipher text
`0x49f573321bdb3ad0a78f0e0c7cd4f4aa2a6d5911c90540ddbbaf067c6aabaccde78c8ff70c5a4abe7d4efa19074a5249b2e6525a0168c0c49535bc993efb7e2c221f4f349a014477d4134f03413fd7241303e634499313034dbb4ac96606faed5de01e784f2706e85bf3e814f5f88027b8aeccf18c928821c9d2d830b5050a1e` out of the `intercepted_message.pcap` using [Wireshark](https://www.wireshark.org/). We can glean two key observations from this:
1. This modulus must be a product of two of the 30 primes being used.
2. The server lets us generate as many moduli as we want.

If we repeatedly request moduli it wont be too long before one of the keys shares a prime with our modulus (See a python sample of this below). If this occurs, the GCD of the two moduli will be the `p` component of the modulus and dividing the modulus, `N` by `p` will yeild the other prime `q`. Now that we have the two primes and know the public exponent, `e` equals 65537, we can easily compute the private exponent `d` as `70118266743531770742541821902419779511239599511770182985184154839839018008193467076473425663009520539545369270962530218486192141886710801892227602961998928213537654150767790772889562458972990736497832327701547730106443165511208494243221689127374975558908570745982766653293349491204750802344491680794276628473` and the message as `41494331723717004087840363038436379137678883897083290482504777727264502253603851759718429929339251785330232810578894088434140357577326859552100822540305154760883449774383987636028167175968532867374560076986174085246917601557997651752239365247146390720857679075750704377311507373191982`
Finally, converting the decrypted number to plaintext reveals the message:

`Good thing no one can read this! I'd hate for them to know that the flag is make_sure_your_rng_generates_lotsa_primes.`
and the flag!

Python Sample Code for finding the gcd of the modulus:
```python
from fractions import gcd
import socket

server = "vuln2014.picoctf.com"
c =  int(0xc20a1d8b3903e1864d14a4d1f32ce57e4665fc5683960d2f7c0f30d5d247f5fa264fa66b49e801943ab68be3d9a4b393ae22963888bf145f07101616e62e0db2b04644524516c966d8923acf12af049a1d9d6fe3e786763613ee9b8f541291dcf8f0ac9dccc5d47565ef332d466bc80dc5763f1b1139f14d3c0bae072725815f)
test_num = 1
while gcd(c,test_num) == 1:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, 51818))
    sock.recv(2048)
    string = "0x" + sock.recv(2048)
    test_num =  int(string,16)
print gcd(test_num,c)
print c/gcd(test_num,c)

```
### Flag ###

    make_sure_your_rng_generates_lotsa_primes
