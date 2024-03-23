import sys
import random
# file = 'f1.vm'
# with open(file, 'r') as f :
    # con = f.readlines()
output = 'out.asm'
import sys
label_counter = 0
def parser(instruction):
    items = instruction.strip().split(" ")
    command = items[0]
    # print(command)

    if command == "push":
        segment, index = items[1], int(items[2])
        tup = ('C_PUSH', (command, (segment, index)))
    elif command == "pop":
        segment, index = items[1], int(items[2])
        tup = ('C_POP', (command, (segment, index)))
    elif command == "add":
        tup = ('C_ARITHMETIC', ('add', None))
    elif command == "sub":
        tup = ('C_ARITHMETIC', ('sub', None))
    elif command == "neg":
        tup = ('C_ARITHMETIC', ('neg', None))
    elif command == "eq":
        tup = ('C_ARITHMETIC', ('eq', None))
    elif command == "gt":
        tup = ('C_ARITHMETIC', ('gt', None))
    elif command == "lt":
        tup = ('C_ARITHMETIC', ('lt', None))
    elif command == "and":
        tup = ('C_ARITHMETIC', ('and', None))
    elif command == "or":
        tup = ('C_ARITHMETIC', ('or', None))
    elif command == "not":
        tup = ('C_ARITHMETIC', ('not', None))
    elif command== "goto":#done
        lab = items[1]
        # print("lab: ", lab)
        # print("goto:",items[0],items)

        tup = ('C_GOTO', (command,(lab)))

    elif command == "if-goto":#done 
        lab = items[1]
        tup = ('C_IF', (command, (lab)))
        # print("if goto :",items[1])
        # print("if got: ", tup[1][1])
    
    elif command =="label":#done 
        lab = items[1]
        tup = ('C_LABEL', (command, (lab)))
        # print("labe: ",tup[1][1] )
        # print("label:", items[0],items)
    elif command == "call": #done
        
        tup = ('C_CALL', (command,(items[1], items[2])))
        # inn_tup = tup[1]
        # print("call tup : ", inn_tup)
        # print("call tup:",inn_tup[1][1])
        # print("items:", items)

    elif command == "function":
        tup = ('C_RETURN', (command, None))
        tup = ('C_FUNCTION', (command, (items[1], items[2])))
        # print("function:",tup[1][1][0], tup[1][1][1])
    elif command == "return":#done 
        tup = ('C_RETURN', (command, None))
        # print("return:", items[0],items)

    
    else:
        raise ValueError(f"Invalid command: {command}")
    return tup

def remove_comments(linelist):
    newList = []
    for line in linelist:
        if (line.strip().startswith('//')):
            continue 
        elif "//" in line:
            removedComments = line.split('//')[0].strip()
            newList.append(removedComments)
        elif line == "\n":
            continue
        else:
            newList.append(line.strip())
    return newList

def generate_arithmetic(command):
    counterJmp=str(random.randint(0,10000)) # get a random integer which we use to create unique conditional jump location
    if command == "add":
        result = '@SP\n'+'M=M-1\n'+'A=M'+'D=M\n'+'A=A-1\n'+'M=D+M'
    elif command == 'sub':
        result = '@SP\n'+'M=M-1\n'+'A=M'+'D=M\n'+'A=A-1\n'+'M=D-M'
    elif command == 'neg':
        result = '@SP\n'+'M=M-1\n'+'A=M'+'M = -M\n'+'@SP\n'+'M = M+1'
    elif command == "and":
        result = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D&M'
    elif command == 'or':
        result = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D|M'
    elif command  == "not":
        result = '@SP\n'+'M=M-1\n'+'A=M'+'M = -M\n'+'@SP\n'+'M = M+1'
    elif command =='eq': #Conditional jump checks for equality and jumps if equal. Handles stack pointer accordignly
        result='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JEQ'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    elif command =='gt': #Conditional jump checks for equality and jumps if greater than zero. Handles stack pointer accordignly
        result='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JGT'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    elif command =='lt': #Conditional jump checks for equality and jumps if less than zero. Handles stack pointer accordignly
        result='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JLT'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    # Return a representation of Hack Assembly instruction(s) which implement the passed in command
    return result 

def generateMemoryAccess(command,segment, index):
    if command =="push": #Push opperation adds an element to the top of the stack.
        if segment =="constant":
            retStr = '@'+str(index)+'\n'+'D=A\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='local': 
            retStr = '@LCL\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='argument': #We save the value at @ARG+offset and push it on the stack
            retStr = '@ARG\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='this': #Get the value at @THIS+offset and push it on top of the stack
            retStr = '@THIS\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='that': #Get the value at @THAT+offset and push it on top of the stack
            retStr = '@THAT\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='pointer': #pointer is mapped to locations 3-4 on RAM. Therefore 'push pointer i' is translated to assembly code that accesses RAM location 3+i.
            retStr = '@R3\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='temp': #temp is mapped to locations 5-12 on RAM. Therefore 'push temp i' is translated to assembly code that accesses RAM location 5+i.
            retStr = '@R5\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='static': #We represent each variable J in file F as a symbol F.J. We store the value at that address in D register and then push it on stack.
            retStr = '@'+str((sys.argv[1].split('.'))[0])+'.'+str(index)+'\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
    elif command =="pop": #Pop opperation removes the top element from the stack.
        if segment =="local": # Store the value of the @LCL+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@LCL\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='argument': #Store the value of the @ARG+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@ARG\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='this': #Store the value of the @THIS+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@THIS\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='that': #Store the value of the @THAT+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@THAT\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='pointer': #Store the address of the desired offset in R13 register. Retrieve the value from top of the stack and put it inside the saved address location.
            retStr='@SP\n'+'M=M-1\n'+'@R3\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='temp':  #Store the address of the desired offset in R13 register. Retrieve the value from top of the stack and put it inside the saved address location.
            retStr='@SP\n'+'M=M-1\n'+'@R5\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='static': #Take the top element from the stack and put it inside the location of @F.J
            retStr = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'@'+str((sys.argv[1].split('.'))[0])+'.'+str(index)+'\n'+'M=D'
    # Return a representation of Hack Assembly instruction(s) which implement the passed in command
    return retStr
def generate_init():
    # //write bootstrap code 
    pass 

def generate_labeL(label):
    result = f'({label})'
    return result 
    

def generate_goto(label):
    result = '@'+label +'\n'+'0;JMP'
    return result

    pass 
def generate_if(label):
    result = '@SP\n'+'AM=M-1\n'+'D=M\n'+'@'+label+'\n'+'D;JNE\n'
    return result 
    
def generate_call(function_name, num_args):
    global label_counter  # Assuming label_counter is defined globally
    return_label = function_name + "$ret." + str(label_counter)
    label_counter += 1

    output = (
        f"@{return_label}\n"
        "D=A\n"
        "@SP\n"
        "A=M\n"
        "M=D\n"
        "@SP\n"
        "M=M+1\n"
        "@LCL\n"
        "D=M\n"
        "@SP\n"
        "A=M\n"
        "M=D\n"
        "@SP\n"
        "M=M+1\n"
        "@ARG\n"
        "D=M\n"
        "@SP\n"
        "A=M\n"
        "M=D\n"
        "@SP\n"
        "M=M+1\n"
        "@THIS\n"
        "D=M\n"
        "@SP\n"
        "A=M\n"
        "M=D\n"
        "@SP\n"
        "M=M+1\n"
        "@THAT\n"
        "D=M\n"
        "@SP\n"
        "A=M\n"
        "M=D\n"
        "@SP\n"
        "M=M+1\n"
        f"@{num_args}\n"
        "D=A\n"
        "@SP\n"
        "D=M-D\n"
        "@ARG\n"
        "M=D\n"
        "@SP\n"
        "D=M\n"
        "@LCL\n"
        "M=D\n"
        f"@{function_name}\n"
        "0;JMP\n"
        f"({return_label})\n"
    )

    return output

def generate_return():  
    output = (
        "@LCL\n"
        "D=M\n"
        "@R13\n"
        "M=D\n"
        "@5\n"
        "A=D-A\n"
        "D=M\n"
        "@R14\n"
        "M=D\n"
        "@SP\n"
        "AM=M-1\n"
        "D=M\n"
        "@ARG\n"
        "A=M\n"
        "M=D\n"
        "@ARG\n"
        "D=M+1\n"
        "@SP\n"
        "M=D\n"
    )
    for segment in ["THAT", "THIS", "ARG", "LCL"]:
        output += (
            f"@R13\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{segment}\n"
            "M=D\n"
        )
    output += (
        "@R14\n"
        "A=M\n"
        "0;JMP\n"
    )
    return output


# def generate_call(function_name, num_args):
#     global label_counter  # Assuming label_counter is defined globally
#     return_label = function_name + "$ret." + str(label_counter)
#     label_counter += 1

#     output = [
#         # Push return address
#         "@" + return_label + "\n",
#         "D=A\n",
#         "@SP\n",
#         "A=M\n",
#         "M=D\n",
#         "@SP\n",
#         "M=M+1\n",
#         # Push LCL, ARG, THIS, and THAT
#         "@LCL\n",
#         "D=M\n",
#         "@SP\n",
#         "A=M\n",
#         "M=D\n",
#         "@SP\n",
#         "M=M+1\n",
#         "@ARG\n",
#         "D=M\n",
#         "@SP\n",
#         "A=M\n",
#         "M=D\n",
#         "@SP\n",
#         "M=M+1\n",
#         "@THIS\n",
#         "D=M\n",
#         "@SP\n",
#         "A=M\n",
#         "M=D\n",
#         "@SP\n",
#         "M=M+1\n",
#         "@THAT\n",
#         "D=M\n",
#         "@SP\n",
#         "A=M\n",
#         "M=D\n",
#         "@SP\n",
#         "M=M+1\n",
#         # ARG = SP - 5 - num_args
#         "@SP\n",
#         "D=M\n",
#         "@5\n",
#         "D=D-A\n",
#         f"@{num_args}\n",
#         "D=D-A\n",
#         "@ARG\n",
#         "M=D\n",
#         # LCL = SP
#         "@SP\n",
#         "D=M\n",
#         "@LCL\n",
#         "M=D\n",
#         # Jump to function_name
#         f"@{function_name}\n",
#         "0;JMP\n",
#         # (return_label)
#         f"({return_label})\n"
#     ]

#     return "".join(output)


# def generate_return():  
#     result = '@LCL\n'+'D=M\n'+'@R13\n'+'M=D\n'+'@5\n'+'A=D-A\n'+'D=M\n'+'@R14\n'+'M=D\n'+'@SP\n'+'AM=M-1\n'+'D=M\n'+'@ARG\n'+'A=M\n'+'M=D\n'+'@ARG\n'+'D=M+1\n'+'@SP\n'+'M=D\n'
#     for segment in ["THAT", "THIS", "ARG", "LCL"]:
#         result.append("@R13")
#         result.append("AM=M-1")
#         result.append("D=M")
#         result.append("@" + segment)
#         result.append("M=D")
#     result.append("@R14")
#     result.append("A=M")
#     result.append("0;JMP")
#     return result 
# def generate_return():  
#     result = ['@LCL\n', 'D=M\n', '@R13\n', 'M=D\n', '@5\n', 'A=D-A\n', 'D=M\n', '@R14\n', 'M=D\n', '@SP\n', 'AM=M-1\n', 'D=M\n', '@ARG\n', 'A=M\n', 'M=D\n', '@ARG\n', 'D=M+1\n', '@SP\n', 'M=D\n']
#     for segment in ["THAT", "THIS", "ARG", "LCL"]:
#         result.append("@R13")
#         result.append("AM=M-1")
#         result.append("D=M")
#         result.append("@" + segment)
#         result.append("M=D")
#     result.append("@R14")
#     result.append("A=M")
#     result.append("0;JMP")
#     return result 



def generate_function(functionName , numLocals):
    numLocals = int(numLocals)
    # result = '('+functionName +')\n'
    result = ['(' + functionName + ')\n']

    # print("num locals", numLocals)
    for _ in range(numLocals):
        r = generateMemoryAccess("push","constant", 0)
        result.append(r)

    return result 
 



def code(instructiotype, instargs):
    if instructiotype== "C_ARITHMETIC":
        assembly = generate_arithmetic(instargs[0])
    elif instructiotype== "C_PUSH":
        assembly = generateMemoryAccess(instargs[0], (instargs[1])[0],(instargs[1])[1] )
    elif instructiotype== "C_POP":
        assembly = generateMemoryAccess(instargs[0], (instargs[1])[0],(instargs[1])[1] )
    elif instructiotype== "C_LABEL":#done
        assembly = generate_labeL(instargs[0])
    elif instructiotype == "C_RETURN": #done
        assembly = generate_return()
    elif instructiotype == "C_CALL":#done
        
        # print("inn : call L: ", instargs[1][0], instargs[1][1])

        assembly = generate_call(instargs[1][0],instargs[1][1])

    elif instructiotype == "C_GOTO": #done 
        assembly = generate_goto((instargs[1])[1])
        # print("c_goto : ", {instargs[0], (instargs[1])[0]})
    elif instructiotype =="C_IF":#done 
        # print("c_if : ", {instargs[0], (instargs[1])[0]})
        assembly = generate_if((instargs[1])[1])
        
    elif instructiotype == "C_FUNCTION":
        # print("c_function ",(instargs[1])[1],instargs[1][0])
        assembly = generate_function( (instargs[1])[0],instargs[1][1])
    return assembly



def main():
    fileinput = open(sys.argv[1], 'r')
    outputfile = (sys.argv[1].split("."))[0] + ".asm"
    outFile = open(outputfile, 'w')

    readinput = fileinput.readlines()
    readinput = remove_comments(readinput)
    
    for instruction in readinput:
        instructiontype, instructionargs = parser(instruction)
        assembly_code = code(instructiotype=instructiontype, instargs=instructionargs)
        
        if isinstance(assembly_code, str):  # Check if assembly_code is a string
            outFile.write(assembly_code + '\n')  # Write the assembly code to the output file
        else:
            outFile.write('')  # If assembly_code is not a string, write an empty string
 # Write the assembly code to the output file

    fileinput.close()
    outFile.close()



if __name__ =="__main__":
    main()
# file1 = 'dum.vm'
# f = open(file1, 'r') 
# inp = f.readlines()
# inp = remove_comments(inp)
# for ins in inp:
#     print(ins)
#     i1 , i2  = parser(ins)
