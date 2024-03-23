// Initialization
@R0
D = M  
@END
D;JEQ

 // Load value from R0 into D
@R1
D = M 
@END
D;JEQ
  // Load value from R1 into D
@R2
M = 0   // Initialize the result (sum) in R2 to 0
@i 
M = 1   // Initialize the loop counter in R3 to 1
@n
M = D   // Copy the value from R1 (multiplier) to R4

// Multiplication Loop
(LOOP)
    @i 
    D = M   // Load the loop counter into D
    @n

    D = D-M
       // Subtract the loop counter from the multiplier    
    @STOP
    D; JGT     // If D is greater than 0, continue the loop; otherwise, jump to STOP

    @R0
    D = M       // Load the value from R0 into D
    @R2
    D = D + M   // Add the value from R0 to the result in R2
    @R2
    M = D       // Store the result back in R2

    @i 
    M = M + 1   // Increment the loop counter
    @LOOP
    0; JMP      // Jump back to the beginning of the loop

(STOP)
    // The multiplication loop stops here
    
     

// End
    // You can add code here to handle the result in R2
    // For example, you can print or store the result.

(END)
    @R2 
    M = 0
    @END 
    0; JMP      // Unconditional jump to END