print("finally building the compiler....")


KEYWORDS = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
SYMBOLS = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&amp;','|','&lt;','&gt;','=','~']
import re 
class Tokenizer:
    def __init__(self,filename):
        self.filename =  open(filename, 'r')
        self.source = self.filename.readlines()
        self.source = self.remove_comments(self.source)
        self.tokens = []
        self.maketokens()
        self.current_token = None 
        

        # for token in self.source:
        #     # print(token)
        #     # tok = re.findall(r'\w+|;|{|}', token)
        #     pattern = '|'.join(map(re.escape, SYMBOLS))
        #     pattern = f'\\w+|{pattern}'
        #     words = re.findall(pattern, token)
        #     print(words)
    def curToken(self):
        return self.current_token
        
    def maketokens(self):

        for tok in self.source:
            tokens = []
            KEYWORDS = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
            SYMBOLS = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
            INTEGER_CONST_PATTERN = r'\d+'
            STRING_CONST_PATTERN = r'"[^"\n]*"'
            IDENTIFIER_PATTERN = r'\w+'

            # Construct regular expression pattern to match keywords, symbols, integer constant, string constant, and identifier
            pattern = '|'.join(map(re.escape, SYMBOLS + KEYWORDS))
            pattern += f'|{INTEGER_CONST_PATTERN}|{STRING_CONST_PATTERN}|{IDENTIFIER_PATTERN}'

            # Use regular expression to split the sentence into tokens
            for tok in self.source:
                self.tokens.extend(re.findall(pattern, tok))

            return self.tokens

            # tokens = re.findall(pattern, tok)

            # # Print each token
            # for token in tokens:
            #     print(token) 


           
    def remove_comments(self,linelist):
        newList = []
        for line in linelist:
            if (line.strip().startswith('//') or (line.strip().startswith('/**')) or (line.strip().startswith('/*'))):
                continue 
            elif "//" in line:
                removedComments = line.split('//')[0].strip()
                newList.append(removedComments)
            elif line == "\n":
                continue
            else:
                newList.append(line.strip())
        return newList
    def hasMoreTokens(self):
        if len(self.tokens) !=0 :
            return True 
        return False 
    
             
    


    def advance(self):
        if self.hasMoreTokens():
            self.current_token = self.tokens.pop(0)
            print("curr tok:",self.current_token)
            # return self.tokens.pop(0)
            return self.current_token
        else:
            return None 

    def tokentype(self, token):

        if token in KEYWORDS:
            self.tk = token  
            print("token type: keyword", token)

            return 'keyword'
            
            
        elif token in SYMBOLS:
            self.tk = token
            print("token type: symbol", token)
            return 'symbol'
        elif re.match(r'\d+', token):  # Integer constant pattern
            self.tk = token
            print("token type: integer", token)
            return 'int_const'
        
        elif re.match(r'"[^"\n]*"', token):  # String constant pattern
            self.tk = token
            print("token type:string", token)
            return 'string_const'
        
        elif re.match(r'\w+', token):  # Identifier pattern
            self.tk = token
            print("token type: identifier", token)
            return 'identifier'
        

    def keyword(self, token):
        if self.tokentype(token) =='keyword':
            if token in KEYWORDS:
                print("successfully retured by keyword: ", token)
                return token
            else:
                print("keyword didnt return anything: ",token)
        
            

    def symbol(self,token):
        if self.tokentype(token) == 'symbol':
            if token in SYMBOLS: 
                print("successfully retured by  symbol: ", token)
                return token
            else:
                print("nothing returned by symbol: ",token)


    def identifier(self,token):
        if self.tokentype(token) == token:
            print("successfully retured by  identifier: ", token)
            return token
    
    def intval(self,token):
        if self.tokentype(token) == 'int_const':
            try:
                intval = int(token)
                print("succesffuly returned by intval: ", intval)
                return intval
            except ValueError:
                print("unsuccessfully returned by intval", token)
                
            

    def stringval(self, token):
        if self.tokentype(token) == 'string_const':
            if (token.startswith("'") and token.endswith("'") ) or (token.startswith('"') and token.endswith('"')):
                stringval = token[1:-1] 
                print("successfully returned by stringval", stringval)
                return stringval
            

class CompilationEngine:
    def __init__(self,input):
        self.inp = open(input, 'r')
        self.tokenizer = Tokenizer(input)
        self.result = []
        
    
    def compileClass(self, token):
        self.result.append("<class>\n  ") 
        
        if self.tokenizer.tokentype(token) == 'keyword':
            self.result.append("<keyword>\n" + token + "\n</keyword>")
            
            
            self.result.append("\n</class>")
        else:
            return None 
        
        return ''.join(self.result)


    
    def compileClassVarDec(self):
        pass 
    def compileSubroutine(self):
        pass 
    def compileParameterList(self):
        pass 
    def compileVardec(self):
        pass 
    def compileStatements(self):
        pass 
    def compileDo(self):
        pass 
    
    def compileLet(self):
        pass 
    def compileWhile(self,token):
        if self.tokenizer.tokentype(token) == 'keyword' :
            if self.tokenizer.keyword(token) == 'while':
                result = "<"+"whileStatement"+"</whileStatement>"
                return result 
        
    def compileReturn(self):
        pass 
    def compileIf(self):
        pass 
    def compileExpression(self):
        pass 
    def compileTerm(self):
        pass 
    def compileExpressionList(self):
        pass 
    
file  = 'Main.jack' 
file1 = 'SquareGame.jack'
file2 = 'whi.jack'
file3 = 'xyz.jack'
tk = Tokenizer(file2)
a = tk.maketokens()
c = CompilationEngine(file2)
print(a)
for i in a :
    if tk.tokentype(i) == 'keyword':
        print(c.compileClass(i))
# while  tk.hasMoreTokens() !=False:
#     tk.advance()

