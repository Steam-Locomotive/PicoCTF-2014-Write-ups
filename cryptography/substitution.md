## Substitution - 50 (Cryptography) ##
#### writeup by Gladius Maximus
Created: 2014-11-07 22:12:02
Last modified: 2014-11-09 22:28:33

### Problem ###
There's an authorization code for some Thyrin Labs information here,
along with someone's favorite song. But it's been encrypted! Find the
authorization code.

[encrypted.txt](encrypted.txt)

### Hint ###
You may want to look at what the relative frequencies of letters in english
text are.

## Answer ##

### Overview ###
This is a [simple substitution
cipher](http://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution). It
is susceptible to frequency analysis. There are numerous tools online for
this. Below, I explain how to write your own in python.

### Details ###

A [simple substitution
cipher](http://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution)
maps every character plaintext to a different character for the cipher
text. You can do a 'frequency analysis' on this kind of cipher. I happen to
know that the most common letter in English is 'e'. The most common letter in
the ciphertext is 'h'. Therefore 'h' probably maps to 'e'

We can actually do a lot more than this. I will write a script in python that
get two lists: the first is a sorted list of n-grams, the secound is a sorted
list of n-long words. An n-gram is a string of letters within a word. For
example the [most common
bigram](http://en.wikipedia.org/wiki/Bigram#Bigram_frequency_in_the_English_language)
is 'th' then 'he', 'in', 'er', etc. The [most common
trigram](http://en.wikipedia.org/wiki/Trigram) is 'the', 'and', 'tha', 'ent',
etc. By extension an n-gram just a string of letters within a word. If I find
the most common n-grams in the output, I can compare these to the most common
n-grams in english. The list of n-long words is a lot more straightforward. I
can guess common one-letter words like 'I', and 'a', then common two-letter
words like 'an' or 'it'. We also want to go through the list of words and
finding the most common first letter

To find the n-grams, we can loop through i from zero to the length of the
string minus n. Then we slice the string from i to i plus n. If it contains a
space or newline, ignore it. Otherwise add it to a counter. The pyhton standard
library provides a counter class which is very useful for doing these frequency
analyses. To find n-long words, we can use regex to split the text into words
and add each word the appropriate counter.

```python
import re
from collections import Counter
from data import ctext

ctext_words = filter(bool, re.split('\s', ctext))
max_gram = 15 # up to 15-gram, up to 15-letter words
n_grams = []
n_words = []

for i in range(1, max_gram + 1):
    # for i = 2, do bigrams and 2-letter words
    # for i = 3, do trigrams and 3-letter words
    a = Counter()
    for j in range(len(ctext) - i):
        gram = ctext[j:j + i]
        if ' ' in gram or '\n' in gram:
            continue # skip grams seperated by space
        a[gram] += 1
    n_grams.append(a)

    b = Counter()
    for word in ctext_words:
        if len(word) != i:
            continue
        b[word] += 1
    n_words.append(b)

starting_letters = Counter()
ending_letters = Counter()
for word in ctext_words:
    starting_letters[word[0]] += 1
    ending_letters[word[-1]] += 1
```

To use this script, just let `ctext` be the encrypted text you have and run
it. Now we need to display the results in a meaningful way.

```python
code = {} # fill this in along the way
def decrypt(word):
    decoded = ''
    for letter in word:
        try:
            decoded += code[letter]
        except KeyError:
            decoded += letter
    return decoded


def table(counter, n=10):
    total = sum(counter.values())
    for word, freq in counter.most_common(n):
        print '{0: <10.1f}{1}'.format(float(freq) / total * 100, decrypt(word))
```

Now just type `table(starting_letters)` to get a table of the most common
starting letters and their frequency as a percentage, or `table(n_words[3])` to
get the most common 3 letter long words.

These websites may be helpful

 - [http://www.cryptograms.org/letter-frequencies.php](http://www.cryptograms.org/letter-frequencies.php),
 - [http://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html](http://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html),
 - [http://norvig.com/mayzner.html](http://norvig.com/mayzner.html),
 - [http://www.letterfrequency.org/](http://www.letterfrequency.org/)

From here, we make multiple passes. Here are the most useful results. I made
educated guesses on what the letters should be.

#### First pass ####

Full text: [first_pass.txt](first_pass.txt)

	Single letters
	12.3      h -> E
	9.8       c 
	9.0       r
	8.4       k

We have inconclusive evidence on all of the other letters.

	Letter bigrams
	6.9       ri -> TH
	5.3       ih -> HE

	Letter trigrams
	6.9       rih -> THE

	All letter tetragrams
	2.6       hshw -> EVER
	2.0       bqri
	1.7       khsh -> WERE

	One-letter words
	70.0      e
	30.0      q

I know these map to either 'a' or 'I'.

	Four-letter words
	8.8       bqri -> WITH (consistent with q -> I)

Therefore, we fill in `code` with the appropriate letters. I have decided to
make the deciphered text uppercase, so I can tell apart what is already
deciphered with what is not already deciphered.

```python
code = {'h':'E', 'r':'T', 'i': 'H', 'b':'W', 'e':'A', 'q':'I'}
```

#### Second pass ####

Full text: [second_pass.txt](second_pass.txt)

	Two-letter words
	20.5      co -> OF
	11.4      Tc -> TO
	9.1       WE
	9.1       Ia
	6.8       ac
	6.8       Ik -> IN|IS|IF -> IN?

	Three-letter words
	31.5      THE
	18.5      gcj
	9.3       Auu
	9.3       Akt -> ANt|ASt|AFt -> AND
	6.5       fAk
	5.6       AwE
	2.8       cWk -> OWN|OWS|OWF -> OWN

You can see how the encrypted and decrypted letters mix together. The decrypted
ones are the ones we solved last pass. The decrypted letters are capital and
the encrypted letters are lowercase.

Apparently the text `qk` showed up a lot. We
know the `q` maps to `I` from the first pass, so it shows up as `Ik` (`I` is decrypted,
`k` is encrypted). This could be `IN`, `IS`, or `IF`. This means `k` decrypts
to `N` or `S` or `F`. Trying that out on the three letter words, it becomes
obvious that since there is no word `AS_` or `AF_`, but there is a word `AND`
which is quite frequent, `k` decrypts to `D`.

	Five-letter words
	14.6      kEsEw -> NEVER
	9.8       gcjuu
	9.8       THIkd -> THINK
	9.8       EAwTH -> EARTH
	9.8       lAIkT
	4.9       aTIuu
	2.4       uEAwk
	2.4       gcjsE
	2.4       EsEwg -> EVER

Here I have begun guessing whole words. I have gotten other letters the same
way (you can see the full text [here](second_pass.txt)). Now we have:

```python
code = {'h':'E', 'r':'T', 'i': 'H', 'b':'W', 'e':'A', 'q':'I', 'k':'N', 'c':'O',
        'd':'K', 's':'V', 'w':'R'}
```

#### Third pass ####

Full text: [third_pass.txt](third_pass.txt)

	Thirteen-letter words
	100.0     AjTHORIxATION -> AuTHORIzATION

	Eight-letter words
	12.5      zRINNINz -> GRINNING
	12.5      agfAnORE -> S_CA_ORE
	12.5      IzNORANT -> IGNORANT
	12.5      WHATEVER
	12.5      vROTHERa -> BROTHERS
	12.5      ajNaWEET -> SUNSWEET
	12.5      fREATjRE -> CREATURE
	12.5      aTRANzER -> STRANGER

	Seven-letter words
	20.0      aKINNEt -> SKINNED
	20.0      vERRIEa -> BERRIES
	20.0      WHETHER
	20.0      oRIENta -> _RIEN_S
	20.0      zRINNEt -> GRINNED?

Now the whole thing comes tumbling down. I got a lot more letters this way. You
can see the full text [here](third_pass.txt). Now our code is:

```python
code = {'h':'E', 'r':'T', 'i': 'H', 'b':'W', 'e':'A', 'q':'I', 'k':'N', 'c':'O',
        'd':'K', 's':'V', 'w':'R', 'j':'U', 'x':'Z', 'z':'G', 'v':'B', 'a':'S',
        'f':'C', 'u':'L', 'l':'P', 't':'D', 'o':'F',
```

#### Fourth and fifth pass ####

I started guessing single letters and bigrams. Then I guessed words. Now I am
ready to guess sentences and paragraphs. You can see the
[fourth_pass.txt](fourth_pass.txt) and the final decrypted message in
[fifth_pass.txt](fifth_pass.txt). For these, I am using:

```python
print decrypt(ctext)
```

Now we got it! Lots of people just used an online tool. Those work, but for
educational purposes, I want to tell you how to do it by yourself so you will
know the online tools work. Here is the full script and all of my work:

 - [subst.py](subst.py) has the bulk of this guide
 - [data.py](data.py) has a copy of the encrypted words
     - [first_pass.txt](first_pass.txt) was individual letters and bigrams
     - [second_pass.txt](second_pass.txt) was bigrams and words
     - [third_pass.txt](third_pass.txt) was words
     - [fourth_pass.txt](fourth_pass.txt) was sentences
     - [fourth_pass.txt](fourth_pass.txt) was the full decrypted text
 - [http://www.cryptograms.org/letter-frequencies.php](http://www.cryptograms.org/letter-frequencies.php),
 - [http://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html](http://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html),
 - [http://norvig.com/mayzner.html](http://norvig.com/mayzner.html),
 - [http://www.letterfrequency.org/](http://www.letterfrequency.org/)

### Flag ###

WITHALLTHECOLORSOFTHEWIND

