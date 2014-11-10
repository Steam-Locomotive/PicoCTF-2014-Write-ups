## The Valley of Fear - 20 (Cryptography) ##
####Writeup by evantey14

Created: 2014-11-07 22:50:06

Last modified: 2014-11-09 23:02:50


Created: 2014-11-07 22:50:06

Last modified: 2014-11-09 23:02:46


Created: 2014-11-07 22:50:06

Last modified: 2014-11-09 23:01:35


### Problem
The hard drive may be corrupted, but you were able to recover a [small chunk of text](https://picoctf.com/problem-static/crypto/the-valley-of-fear/book.txt). Scribbled on the back of the hard drive is a set of mysterious numbers. Can you discover the meaning behind these numbers? (1, 9, 4) (4, 2, 8) (4, 8, 3) (7, 1, 5) (8, 10, 1)

###Hint

Might each set of three numbers represent a word in a message?

##Answer

###Overview

Find a way to relate three numbers to a word in text.

###Details
After opening the text, we see a lot of text formatted into paragraphs. According to the hint, we need to find a coordinate system that maps three numbers to a word in the text. Note that all the numbers are less than 10. Also note that the text is well organized by paragraph and line. This likely means the numbers relate to some textual structure, so lets try (paragraph #, line #, word #)

For the first triplet, we look the first paragraph, ninth line, and fourth word: the. This looks like the start to a good sentence, so continuing, we find: The flag is Ceremonial plates.

###Flag
    Ceremonial plates

