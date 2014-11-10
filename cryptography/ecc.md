## ECC - 100 (Cryptography) ##
####Writeup by ZIceZ

### Problem ###
We found a weird piece of paper with [this](https://picoctf.com/problem-static/crypto/ecc/ecc_handout.txt) written on it. I can't make heads or tails of it, but it seems to be talking about an encoded message. Can you get the message for us?

### Hint ###
Use a computer algebra system with builtin support for elliptic curves, such as Sage. This elliptic curve is defined over the group of integers Z/nZ (Zmod(n) in Sage) and is in Weierstrass form (a1 = a2 = a3 = 0).

## Answer ##
### Overview ###
Elliptical curve encryption.
### Details ###
First solved for the variable b to complete the elliptic curve cryptosystem.
$y^2 = x^3 + a(x) + b \bmod n$ where a = 0
Since we have a coordinate of the system, b can be solved by plugging in X and Y.
$12418605208975891779391^2 = 236857987845294655469221^3 + b \bmod 928669833265826932708591$
Wolfram alpha can solve this equation for you giving
$b = 268892790095131465246420$
With the all the variables found, the cryptosystem can be built to decrypt your message. As the hint suggested, Sage has a built in library that can handle all the calculations. There is an online version of [Sage](cloud.sagemath.com), so downloading it is not necessary. For information on how to setup an elliptic curve, refer to [here](http://www.sagemath.org/doc/constructions/elliptic_curves.html).
```
F = FiniteField(928669833265826932708591)
E = EllipticCurve(F,[0,268892790095131465246420])
G = E.point((236857987845294655469221, 12418605208975891779391))
d = 87441340171043308346177
G*d
```
The result is (6976767380847367326785 : 828669833265826932708578 : 1). Decode the X and Y coordinate with the given function.
```Python
def STR(a):
    a = str(a)
    # Yes, this is a little bit silly :-)
    for i in range(0, len(a) - 1, 2):
            print(chr(int(a[i:i+2])))
print STR(6976767380847367326785)
print STR(828669833265826932708578)
```

### Flag ###
    ELLIPTIC CURVES ARE FUN

