import re
FILE = 'te.asm'
FILE2 = 'ate.asm'
FILE3 = 'thir.asm'
FILE4 = 'file4.asm'
file5 = 'sy.asm'

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


# table of symbols used in assembly code, initialized to include
# standard ones
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}


def ignore(line):
    pass 

def parser(line):
    pass 

def asstobinary(line):
    pass
def addtotable(line):
    pass 


def assemble(file):
    pass 


class Parser:
    def __init__(self, file):
        self.file = file 
        self.command_type =  None 
        self.running_number  = 0 
        self.ram_number = 16 
        self.table = SymbolTable()


        try:
            with open(file, 'r') as f:
                self.source_code = f.read()

            self.removeWaste()

        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
            sys.exit(1)
        self.removeWaste()
        # print(self.source_code)
    def removeWaste(self):
        lines = self.source_code.split('\n')
        cleaned_lines = [line.strip() for line in lines if not line.strip().startswith("//") and line.strip() != ""]
        self.source_code = '\n'.join(cleaned_lines)


    def hasMoreCommands(self):
        lines = self.source_code.split('\n')
        for line in lines:
            if line.strip() != "":
                print("T")
                return True
        print("F")

        return False
    def commandType(self):
        lines = self.source_code.split('\n')
        command_types = []

        for line in lines:
            if line.startswith('@'):
                command_types.append("A_COMMAND")
            elif line.startswith('('):
                command_types.append("L_COMMAND")
            else:
                command_types.append("C_COMMAND")

        return command_types

    def destination(self):
        self.command_types = self.commandType()
        results = []  # to store results for each C_COMMAND

        for i, command_type in enumerate(self.command_types):
            if command_type == "C_COMMAND":
                # Extract destination and computation parts separately
                parts = self.source_code.split('\n')
                dest_comp_parts = parts[i].split('=')
                print("dest parts", dest_comp_parts)

                if len(dest_comp_parts) == 2:
                    dest_mnemonic = dest_comp_parts[0].strip()
                    comp_mnemonic = dest_comp_parts[1].strip().split(';')[0].strip()
                    result = dest.get(dest_mnemonic, "000")
                    results.append(result)
                else:
                    results.append("0000000000")  # dest and comp are optional in C_COMMAND
            else:
                continue  # for non-C_COMMAND lines

        return results
    def computaion(self):
        results  = []
        for i , command_type in enumerate(self.command_types):
            if command_type == "C_COMMAND":
                parts = self.source_code.split('\n')
                dest_comp_parts = parts[i].split('=')
                print("comp parts: ", dest_comp_parts)
                if len(dest_comp_parts) == 2:
                    comp_part = dest_comp_parts[1].strip()
                    result = comp.get(comp_part, "0000000")
                    print("computation parts: ", comp_part)
                    results.append(result)
                else:
                    results.append(None) 
            else:
                continue
        return results 

    



        
    def jump(self):
        results = []

        for i, command_type in enumerate(self.command_types):
            if command_type == "C_COMMAND":
                parts = self.source_code.split("\n")
                dest_comp_jump_parts = parts[i].split('=')
                print("jump parts : ", dest_comp_jump_parts)
                if len(dest_comp_jump_parts) == 2:
                    comp_jump_part = dest_comp_jump_parts[1].strip()
                    jump_parts = comp_jump_part.split(';')

                    if len(jump_parts) == 2:
                        jump_part = jump_parts[1].strip()
                        print("jump part: ", jump_part)
                        results.append(jump_part)
                    else:
                        continue  # No jump part
                else:
                    continue  # No jump part

            else:
                continue  # For non-C_COMMAND lines

        return results
                


    def final(self):
        self.command_types = self.commandType()
        results = []  # to store results for each C_COMMAND

        lines = self.source_code.split('\n')

        for i, command_type in enumerate(self.command_types):
            if command_type == "C_COMMAND":
                # Extract destination, computation, and jump parts separately using regular expressions
                instruction = lines[i].split('//')[0].strip()  # Remove comments
                match = re.match(r'(?:(?P<dest>[AMD]+)=)?(?P<comp>[^;]+)(?:;(?P<jump>[A-Z]+))?', instruction)
                dest_mnemonic = match.group('dest') if match.group('dest') else None
                comp_mnemonic = match.group('comp')
                jump_mnemonic = match.group('jump') if match.group('jump') else "null"  # Default to "null" if no jump

                dest_code = dest.get(dest_mnemonic, "000")
                comp_code = comp.get(comp_mnemonic, "0000000")
                jump_code = jump.get(jump_mnemonic, "000")

                # Pad each part to the required length
                dest_code = dest_code.rjust(3, '0')
                comp_code = comp_code.rjust(7, '0')
                jump_code = jump_code.rjust(3, '0')

                result = "111" + comp_code + dest_code + jump_code
                print(result)
                results.append(result)

            elif command_type == "A_COMMAND":
                instruction = lines[i].split('//')[0].strip()
                symbol = instruction[1:]
                # print("symbol: ", symbol)
                # results.append(("@", symbol))
                if symbol.isdigit():
                    symbol_value = int(symbol)
                elif symbol in table:
                    symbol_value = table[symbol]
                else:
                    # Handle the case when the symbol is neither a number nor in the table
                    print("Error: Invalid symbol", symbol)
                    # continue
                    # You might want to add proper error handling or raise an exception here

                binary_num = bin(symbol_value)[2:]
                padded_binary = binary_num.rjust(15, '0')
                result = "0" + padded_binary
                print(result)
                results.append(result)


            else:
                continue
        return results
    def first_pass(self):
        self.command_types = self.commandType()
        lines = self.source_code.split('\n')
        results = []  # to store results for each C_COMMAND

        for i, command_type in enumerate(self.command_types):
            if command_type == "A_COMMAND":
                self.running_number += 1

            elif command_type == "C_COMMAND":
                self.running_number += 1 
            elif command_type == "L_COMMAND":
                match = re.match(r'\((?P<label>\w+)\)', lines[i])
                if match:
                    label = match.group('label')
                    print(label)
                    if not self.table.contains(label):
                        res = self.running_number 
                        self.table.addEntry(label, res)
                        print(self.table())
                        print("\n")
            else:
                continue
    def second_pass(self):
        self.command_types = self.commandType()
        lines = self.source_code.split('\n')
        results = []  # to store results for each C_COMMAND

        for i, command_type in enumerate(self.command_types):
             if command_type == "A_COMMAND":
                # self.running_number += 1 
                instruction = lines[i].split('//')[0].strip()
                symbol = instruction[1:]
                if not self.table.contains(symbol=symbol) and not symbol[0].isdigit():
                    print(symbol)
                    self.table.addEntry(symbol, self.ram_number)
                    self.ram_number += 1 
                    print(self.table())
                elif not self.table.contains(symbol=symbol) and symbol.isdigit():
                    print(symbol)
                    self.table.addEntry(symbol, int(symbol))
                    self.ram_number += 1 
                    print(self.table())
                else :
                    continue


        

class Code:
    @staticmethod
    def desti(mnemonic: str) -> str:
        if mnemonic in dest:
            return dest[mnemonic]
        else:
            raise ValueError(f"Invalid mnemonic: {mnemonic}")
    @staticmethod       
    def compu(mnemonic : str )-> str:
        if mnemonic in comp: 
            return comp[mnemonic]
        else:
            raise ValueError(f"Invalid mnemonic: {mnemonic}")
    def jumpp(mnemonic : str)-> str:
        if mnemonic in str: 
            return jump[mnemonic]
        else:
            raise ValueError(f"Invalid mnemonic: {mnemonic}")

class SymbolTable:
    def __init__(self):
        self.table = table 

    def addEntry(self, symbol: str, address: int):  
         self.table[symbol] =  address
        
    def contains(self, symbol: str):
        return symbol in self.table

    def getAddress(self, symbol: str):
        return self.table.get(symbol, None)
    
    def __call__(self):
        return self.table 
    

# p = Parser(FILE2)
# p.hasMoreCommands()   

# try:
#     binary_code = Code.desti("MD")
#     print(binary_code)
# except ValueError as e:
#     print(e)
# p = Parser(FILE4)

# p.hasMoreCommands()
# print(p.commandType())    
# # print(p.destination())
# # print(p.computaion())
# # print(p.jump())
# # print(p.final())
# # p.final()
# p.first_pass()
# p.second_pass()
# p.final()
import sys
def main():
    if len(sys.argv) != 2:
        print("Usage: python your_script.py filename.asm")
        sys.exit(1)

    filename = sys.argv[1]
    print(filename)
    with open(filename, 'r') as f:
        source_code = f.read()
        print(source_code)

    parser = Parser(filename)
    parser.first_pass()
    parser.second_pass()
    parser.final()

    output_filename = filename.replace(".asm", ".hack")
    with open(output_filename, 'w') as output_file:
        for code_line in parser.final():
           print("code line: ", code_line)
           output_file.write(code_line + '\n')

    print(f"Assembly completed. Output saved to {output_filename}")

if __name__ == "__main__":
    main()