## Revenge of the Bleichenbacher - 170 ##
#### Writeup by ZIceZ and Oksisane #### 

### Problem ###
We found a Daedalus Corp command server, that lets people read some shared files. But it requires cryptographically signed commands! Can you forge a signature for us? It's running at vuln2014.picoctf.com. The JAR file for the service is [here](https://picoctf.com/problem-static/crypto/revenge-of-the-bleichenbacher/CommandServer.jar).

### Hint ###
The service's signature checks are incomplete: can you figure out a way to put in some garbage? In particular, we think it may be vulnerable to a similar bug that Mozilla's NSS library was recently: see [here](https://www.mozilla.org/security/announce/2014/mfsa2014-73.html).

## Answer ##
### Overview ###
Forge a signature using a technique developed by [Bleichenbacher](http://www.imc.org/ietf-openpgp/mail-archive/msg06063.html).
###Details ###
First, what exactly is a RSA signature? A signature is used to verify the origin of a message. Here is how it works:
The source creates a digital signature through the following process:

<img src="http://www.paradigm.ac.uk/images/figure18.gif"/>


The receiver verifies the digital signature like this:

<img src="http://www.paradigm.ac.uk/images/figure19.gif"/>

If the hash function of the message matches the decrypted message then the receiver knows that the message originated from the source and was not tampered with. [Credit for the pictures](http://www.paradigm.ac.uk/workbook/metadata/authenticity-signatures.html).

In our problem, the service checks the the following components in a signature to determine its authenticity.

	00 01 ff ff ff ff ff (repeat ff as needed) 00 (hash of command) (garbage)
The length of the signature can be up to 768 characters long or 3072 bits long.
The exploit discovered by Bleichenbacher takes the advantage of the fact that the server doesn't check that the hash is the last thing in the signature. Rahter it only checks the conditions mentioned above. Following the format, an adversary has a lot of room to work with by placing junk data in (garbage) to forge a signature that satisfies the requirements.

We know that the public key is 3, so our forged signature has to be a number that when taken to the power of 3 will matches the format above. We can work backward to find this number by finding a number that fits the format and is a perfect cube then simply take the cube root of that number for our forged signature.
Bleichenbacher did this already for us already, and you can read more on that [here](http://www.imc.org/ietf-openpgp/mail-archive/msg06063.html). Let modify his formula a bit so it will fit our problem.

Let have the required section of our message (168 bits long) be equal to D:

	00 hash of message = D
	(8 bit)+(160 bit)
So our formula for the padded decrypted message is:
$$2^{3057} - 2^{2244} + D*2^{2072} + garbage $$
Where 2^3057 - 2^2360 is the space left for the 00 01 ff ff ff ff ff (repeat ff as needed) at the front. D is placed 2072 bits from the right of the message. The rest is filled with garbage.
We can simplify this formula further by letting N be:
$$ 2^{168} - D $$
Then our formula is just:
$$2^{3057} - N*2^{2072} + garbage $$
If we use our knowledge from Algebra,
$$ (A-B)^3 = A^3 - 3A^2B + 3AB^2 - B^3$$
Playing around with the number a little bit, our formula can be fit into the cubic expansion. Then we can solve for (A-B) giving us:
$$
2^{1019} - \frac{N*2^{34}}{3}
$$
So lets solve this! Let's try the  `open` command first. The sha-1 hash of the word `open` is `5fc7e38bffe00ca46add89145464a2eaf759d5c2` so our D value is `0x005fc7e38bffe00ca46add89145464a2eaf759d5c2`. We can compute the value we need in Python, using this short script:
```python
import hashlib
commandtosign = "open"
hashtosign = "0x00" + hashlib.sha1(commandtosign).hexdigest()
N = 2**168 - int(hashtosign,16)
print hex(2**1019 - ((N * 2**34) / 3))
```
This gives us the result
```
0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeab2a5fda0fffd566308e7cb6c5c5db83e3f477c7ad55555556L
```
We can check if this is the correct signature by seeing if the following Java code (extracted from the Jar) returns true:
```java
private static final BigInteger N = new BigInteger(
		"c5ddc7decb1beede4ebb96742e4279eb120b9c8b44472c0d0bb39da95a10cf72b630dbea181eeda65772779de8b6af53f2b0c5c3eccae2ef7a349b66637345f1cc0dec4d63550206688751e49da001b2f901cf39ebb1758bae0a89a3a4f8342fa26283f802ce6df144113a2abe075497d373435f80aa96bdf1ea500f58eea6bffb28add63c9d337dacf3bbf81996c7b6b9ac532007010acedb0714a547486c78ca162a0a85c643ce774b2805bd294435d262fb390adce055b971396c0363bb5f7aa409f5c223fa9c211945cb6be7a8df23a3357257a11bfe4bd983799d975e9ba337e928c33a7cd9638c5f4553b2a263233442677f848e948ccc4470a5a5bc16682b3a24188398389a079096d28588f03d01b7bfa6cce9a829e2f5c1b1cc785e891ffa89d63607f48473126f99aca203e0c2e77f21a35b6d6c8816c0650715144ff148d9c60f81bfacbfc5ef879a07bb6cd8e12476803006cc7ae25e8faafa4ee52dac698d7927092d10c4fb748dea6b3dd62a3588cf315f54216689877f3f0d",16);
public static boolean verifySignature(String paramString1,
		String paramString2) {
	String str1 = sha1(paramString1);
	BigInteger localBigInteger1 = new BigInteger(paramString2, 16);
	BigInteger localBigInteger2 = localBigInteger1.modPow(new BigInteger(
			"3"), N);
	String str2 = localBigInteger2.toString(16);

	while (str2.length() < 768) {
		str2 = "0" + str2;
	}
	if ((str2.indexOf("0001ffffffffff") == 0) && (str2.length() == 768)
			&& (str2.contains(str1))) {
		for (int i = str2.indexOf("f"); i < str2.indexOf(str1) - 2; i++) {
			if (str2.charAt(i) != 'f') {
				return false;
			}
		}
		if ((str2.charAt(str2.indexOf(str1) - 2) != '0')
				|| (str2.charAt(str2.indexOf(str1) - 1) != '0')) {
			return false;
		}
		return true;
	}
	return false;
}
public static void main(String args[]) {
    String signature = "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeab2a5fda0fffd566308e7cb6c5c5db83e3f477c7ad55555556";
    System.out.println(verifySignature("open",signature));
}
```
It does! All that remains is to logon to the server by running
```bash
nc vuln2014.picoctf.com  4919
```
Which gives the output

```bash
pico89244@shell:~$ nc vuln2014.picoctf.com  4919
open 7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeab2a5fda0fffd566308e7cb6c5c5db83e3f477c7ad55555556
Please enter which file you'd like to read.
flag
arent_signature_forgeries_just_great
```
### Flag ###
    arent_signature_forgeries_just_great

