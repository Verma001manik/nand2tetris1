file = 'f1.vm'
output = 'out.asm'
class Parser:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            content = f.read()
        self.commands = self.removeWaste(content).split("\n")
        self.index = -1
        self.command_type = ""
        self.advance()

    def removeWaste(self, input_string):
        lines = input_string.split('\n')
        cleaned_lines = []
        for line in lines:
            if not line.lstrip().startswith('//'):
                cleaned_lines.append(line.strip())
        return '\n'.join(cleaned_lines)

    def initialize_current_command(self):
        self.current_command = self.commands[self.index]

    def hasMoreCommands(self):
        return len(self.commands) > self.index

    def advance(self):
        if self.index < len(self.commands) - 1:
            self.index += 1
        self.initialize_current_command()
        return self.current_command

    def commandType(self):
        arithmetic_cmds = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']

        while self.hasMoreCommands():
            words = self.current_command.split()
            command = words[0] if words else ""

            if command == "push":
                self.command_type = "C_PUSH"
                break
            elif command == "pop":
                self.command_type = "C_POP"
                break
            elif command in arithmetic_cmds:
                self.command_type = "C_ARITHMETIC"
                break
            else:
                self.advance()

        return self.command_type

    def arg1(self):
        """Return the first argument of the current command."""

        if self.command_type != "":
            words = self.current_command.split()
            if self.command_type == "C_ARITHMETIC":
                return self.current_command.split()[0]
            elif len(words) >= 2:
                return int(words[1]) if words[1].isdigit() else words[1]
            else:
                raise ValueError("Invalid command format.")

    def arg2(self):
        """Return the second argument of the current command."""

        if self.command_type != "":
            words = self.current_command.split()
            if len(words) >= 3:
                return int(words[2]) if words[2].isdigit() else words[2]
            else:
                raise ValueError("Invalid command format.")

# Test the parser
file = 'f1.vm'
parser = Parser(file)


# print("Command type:", parser.commandType())
# print("Arg1:", parser.arg1())
# print("Arg2:", parser.arg2())
class CodeWriter:
    def __init__(self, filename ):
        self.file = open(filename, 'w')
        self.result_string = ''
       
    def setFileName(self , filename):
        print("Translation of new vm file is started")
    def arithematic(self, command: str):
        if command == "add":
            

    def writePushpop(self,command):
        pass
    
    
    def _write_comment(self, comment):
        return self.output_filename.write(f'//{comment}')
    def close(self):
        self.file.close()

# print(p.advance())
# # print(p)
# print(p.advance())
# print(p.advance())
cw = CodeWriter(output)
print(cw)
