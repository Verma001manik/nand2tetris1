// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is prssed (aney key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(INFINITE_LOOP)
    @KBD 
    D = M 
    @BLACK 
    D ; JGT
    @WHITE 
    D; JEQ
    @LOOP
    0; JMP


(BLACK)
    @R0 
    M = 1 
    @SCREEN 
    D =A 
    @arr 
    M = D 

    @24575
    D = A 
    @n
    M = D 

    @i 
    M =  0 
    (LOOP)
        @i 
        D = M 
        @n 
        D = D-M 
        @END
        D;JEQ

        @arr 
        D = M 
        @i 
        A  = D+M 
        M = 1 
        @i 
        M = M +1 

        @LOOP 
        0;JMP  

   
   
    
    @INFINITE_LOOP
    0 ; JMP 

(WHITE)
    @R1 
    M = 1 
    @INFINITE_LOOP
    0; JMP 
(END)
    @INFINITE_LOOP
    0;JMP