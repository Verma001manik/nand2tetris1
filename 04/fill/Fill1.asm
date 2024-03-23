// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@R0
D = M
@n
M = D
@i
M = 0

@SCREEN
D = A
@address
M = D

(INFINITE_LOOP)
    @KBD
    D = M
      // Jump to CHECK_KEY if D (KBD) is 0 (no key pressed)
    @BLACK
    D;JMP  // If key is pressed, jump to BLACK
    @INFINITE_LOOP
    0;JMP  // If no key is pressed, continue checking

(BLACK)
    @R3
    M = 1
    (LOOP)
        @i
        D = M
        @n
        D = D - M
        @END
        D;JGT

        @address
        A = M
        M = -1

        @i
        M = M + 1
        @32
        D = A
        @address
        M = M + 1
        @LOOP
        0;JMP

    @INFINITE_LOOP
    0;JMP

(WHITE)
    @R1
    M = 1
    @INFINITE_LOOP
    0;JMP

(END)
    @INFINITE_LOOP
    0;JMP
