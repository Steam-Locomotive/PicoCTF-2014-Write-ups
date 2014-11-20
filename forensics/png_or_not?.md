## PNG or Not? - 100 (Forensics) ##
####Writeup by NielsKornerup

Created: 2014-11-08 12:24:40

Last modified: 2014-11-09 23:28:11



### Problem ###

On a corner of the bookshelf, you find a small CD with an [image file](https://picoctf.com/problem-static/forensics/png-or-not/image.png) on it. It seems that this file is more than it appears, and some data has been hidden within. Can you find the hidden data? 

### Hint ###

The PNG file format has a marker for the end of the image.

## Answer ##

### Overview ###

Extract flag.txt from the image.

### Details ###

Using [this source](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html), you can find the specifications for a PNG file. A PNG file starts with an IHDR and ends with an IEND. Now save the image and open it in a text editor. You will notice that there is an IEND tag, and a few characters past this, you can find 7z, which is a file compression system. Look a little farther ahead into the file, and you will notice that flag.txt is in this file. Putting these two things together, install 7z (if you are using Linux, you can sudo apt-get install it) and use it to extract flag.txt from image.png using: 

```bash
7z x image.png
```

This will extract flag.txt, which can then be viewed by opening the file or using something like nano. The contents of this file are the flag.

### Flag ###

    EKSi7MktjOpvwesurw0v
