## Cyborg Secrets - 80 (Reverse Engineering) ##
####writeup by Oksisane

### Problem ###

You found a password protected binary on the cyborg relating to its defensive security systems. Find the password and get the shutdown code! You can find it on the shell server at `/home/cyborgsecrets/cyborg-defense` or you can download it [here](https://picoctf.com/problem-static/reversing/cyborg-secrets/cyborg_defense).

### Hint ###

I wonder if they hardcoded the password string.

## Answer ##

### Overview ###

Open the given program in a text editor (such as [Notepad ++](http://notepad-plus-plus.org/)) or disassembler (such as [Hex-Rays IDA](https://www.hex-rays.com/products/ida/)) to find the password in plaintext, then input it into the program to get the flag.

### Details ###

The hint indicates that the password is hardcoded into the program. Opening the program with a text editor or disassembler reveals the debug admin password `2manyHacks_Debug_Admin_Test`. To get the flag we input this into the program running on the shell, using the command `./cyborg_defence 2manyHacks_Debug_Admin_Test` (where the `./cyborg_defence` executes the cyborg_defence program).

### Flag ###

403-shutdown-for-what

