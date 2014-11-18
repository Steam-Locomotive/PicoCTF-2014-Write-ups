## Towers of Toast - 90 (Reverse Engineering) ##
####Writeup by NielsKornerup####

Created: 2014-11-13 08:55:29

Last modified: [2014-11-17 20:58:07](https://github.com/Oksisane/PicoCTF-2014-Writeups/commits/master/reverse_engineering/towers_of_toast.md)

### Problem ###

 Everyone loves the [Tower of Hanoi](https://en.wikipedia.org/wiki/Towe r_of_Hanoi) puzzle. Well it appears the Toaster Bot wants you to play an essentially identical game called "Towers of Toast". The game doesn't seem to be working though... Can you win anyway? Perhaps by loading a winning saved game? Download the Java code [here](https://picoctf.com/problem-static/reversing/towers-of-toast/Main.java).

### Hint ###

Remember that all numbers have a unique set of [Prime Factors](http://www.mathsisfun.com/prime-factorization.html).

## Answer ##

### Overview ###

To solve this problem, open up the Java program and change the code so that the default load state is the winning one. Then load this game state to win the game and get the flag.

### Details ###

If you try and run the Java program, it will ask you to create a new game or load an old one. If you type new, then you will be given a random set of disks and the program will break down, saying "Sorry, the game is broken :(", but it will give you a set of save numbers. If you try to load a game with your set of save numbers, it will recreate the board and quit the program unless your entered the winning game state, in which case you will receive the flag. To solve this problem, we will modify the Java program so that it gives you the game state for the winning board.

To do this, we will want to change the new game method so that it gives us a winning game state (where all blocks are on the first post). If you look at the Java code for the new game method, it uses a random number to assign rings to random posts. All we need to do is change it so that all the rings go to the first post. If you look at the Java code for the ring distribution:

```java
for (int i = 0; i < GAME_SIZE; i++) {
	int pole = rand.nextInt(3);
	if (pole == 0) { pole1.add(BigInteger.valueOf(i)); }
	else if (pole == 1) { pole2.add(BigInteger.valueOf(i)); }
	else { pole3.add(BigInteger.valueOf(i)); }
}
```

This code runs through all the rings and adds them to random posts. If we change the code so that regardless of the value of pole, the rings will be added to pole1, then the program will return the save state that we desire. To do this, we replace that code with this:

```java
for (int i = 0; i < GAME_SIZE; i++) {
	int pole = rand.nextInt(3);
	if (pole == 0) { pole1.add(BigInteger.valueOf(i)); }
	else if (pole == 1) { pole1.add(BigInteger.valueOf(i)); }
	else { pole1.add(BigInteger.valueOf(i)); }
}
```

Now if you recompile the code and run it, then you should get a winning board configuration. Just load this game state, and you will receive the flag.


### Flag ###

166589903787325219380851695350896256250980509594874862046961683989710
