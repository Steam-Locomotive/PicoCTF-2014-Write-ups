## Revenge of the Bleichenbacher - 170 ##
###Writeup by ZIceZ

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
	![Alt text] (http://www.paradigm.ac.uk/images/figure18.gif) 
The receiver verifies the digital signature like this:
	![Alt text](http://www.paradigm.ac.uk/images/figure19.gif)
If the hash function of the message matches the decrypted message then the receiver knows that the message originated from the source and was not tampered with. [Credit for the pictures](http://www.paradigm.ac.uk/workbook/metadata/authenticity-signatures.html).

In our problem, the service checks the the following components in a signature to determine its authenticity. 

	00 01 ff ff ff ff ff (something) 00 hash of message (something)
The length of the signature can be up to 768 characters long or 3072 bits long.
The exploit discovered by Bleichenbacher takes the advantage of the fact that the server doesn't check everything in a signature. It only checks the conditions mentioned above. Following the format, an adversary has a lot of room to work with by placing junk data in (something) to forge a signature.

We know that the public key is 3, so our forged signature has to be a number that when taken to the power of 3 will matches the format above. We can work backward to find this number by find a number that fits the format and is a perfect cube then simply take the cube of that number for our forged signature.
Bleichenbacher did this already for us already, and you can read more on that [here](http://www.imc.org/ietf-openpgp/mail-archive/msg06063.html). Let modify his formula a bit so it will fit our problem. 

Let have the required section of our message (168 bits long) be equal to D:

	00 hash of message = D
	(8 bit)+(160 bit)
So our formula for the padded decrypted message is:
$$2^{3057} - 2^{2244} + D*2^{2072} + garbage $$
Where 2^3057 - 2^2360 is the space left for the 00 01 ff ff ff ff ff (something) at the front. D is placed 2072 bits from the right of the message. The rest is filled with garbage.
We can simplify this formula further by letting N be:
$$ 2^{168} - D $$
Then our formula is just:
$$2^{3057} - N*2^{2072} + garbage $$
If we use our knowledge from Algebra,
$$ (A-B)^3 = A^3 - 3A^2B + 3AB^2 - B^3$$
Playing around with the number a little bit, our formula can be fit into our cubic expansion. Then we can solve for (A-B) giving us:
$$
2^{1019} - \frac{N*2^{34}}{3}
$$


