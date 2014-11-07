<!---
In general,
Make your explanations clear and concise
Beginners should be able to understand it
Link to outside resources all da time
All of the text should be aligned to 79 characters.
In Emacs, do Ctrl+x f 79 RET Alt-x auto-fill-mode RET, then do Alt-q to realign text
-->

## Tyrannosaurus Hex - 10 (Miscellaneous) ##

### Problem ###

The contents of the flash drive appear to be password protected. On the back of
the flash drive, you see the hexadecimal number 0xac06e9ba scribbled in
ink. The password prompt, however, only accepts decimal numbers. What number
should you enter? (Press the Hint button for advice on solving the challenge).

<!--- Put the hint verbatim from PicoCTF here. Copy any dependencies and link
to them as if they are in the same folder: \[link name\]\(file name\).  -->

### Hint ###

You could try asking [Google](http://www.google.com/) or [Wolfram
Alpha](http://www.wolframalpha.com/).

<!--- Also copy and paste the hint verbatim. Don't forget the zero when you are
copy and pasting -->

## Answer ##

### Overview ###

Convert the number in the problem from base 16 to base 10.

<!--- This is for advanced users who want a phrase like 'inject SQL into this
variable', or 'do a buffer overflow on this input variable'.* -->

### Details ###

Wolfram alpha has base conversion built
in. [Here](http://www.wolframalpha.com/input/?i=base+conversion&a=*MC.~-_*ExamplePage-&f2=23&f=BaseConversion.numToConvert%5Cu005f23&f3=2&f=BaseConversion.toBase%5Cu005f2&a=*FVarOpt.1-_**-.***BaseConversion.fromBase---.*--)
is the help page. Following there syntax, we can put in
[`0xac06e9ba`](http://www.wolframalpha.com/input/?i=0xac06e9ba).

In a programming language like python, we use the
[`int`](https://docs.python.org/2/library/functions.html#int) function. The
first argument is the string to convert. The second argument is the base to
interpret in. Therefore, we put ```python
int('0xac06e9ba', 16)```.

### Flag ###

2886134202

<!--- Don't put anything else here, other than the verbatim answer -->
