from curses.ascii import isdigit
from multiprocessing.sharedctypes import Value
from select import select
import sys
from traceback import print_tb


class Token:
    def __init__(self, value, type):
        self.type = type
        self.value = value


class Tokenizer:

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):

        if self.position < len(self.origin) and self.origin[self.position] in [' ', "\n"]:
            self.position += 1
            while self.position < len(self.origin) and self.origin[self.position] in [' ', "\n"]:
                self.position += 1

        if self.position == len(self.origin):
            self.actual = Token("", "EOF")
            return self.actual

        elif self.position > len(self.origin):
            raise Exception("eof passou")

        if self.origin[self.position] == '+':
            self.position += 1
            self.actual = Token('+', "PLUS")
            return self.actual

        elif self.origin[self.position] == '-':
            self.position += 1
            self.actual = Token('-', "MINUS")
            return self.actual

        elif self.origin[self.position] == '*':
            self.position += 1
            self.actual = Token('*', "MULT")
            return self.actual

        elif self.origin[self.position] == '/':
            self.position += 1
            self.actual = Token('/', "DIV")
            return self.actual

        elif self.origin[self.position] == '(':
            self.position += 1
            self.actual = Token('(', "OPEN_PAR")
            return self.actual

        elif self.origin[self.position] == ')':
            self.position += 1
            self.actual = Token(')', "CLOSE_PAR")
            return self.actual

        elif self.origin[self.position] == '{':
            self.position += 1
            self.actual = Token('{', "OPEN_BRACK")
            return self.actual

        elif self.origin[self.position] == '}':
            self.position += 1
            self.actual = Token('}', "CLOSE_BRACK")
            return self.actual

        elif self.origin[self.position] == ';':
            self.position += 1
            self.actual = Token(';', "SEMI_COLON")
            return self.actual

        elif self.origin[self.position] == '=':
            self.position += 1
            if self.origin[self.position] == "=":
                self.position += 1
                self.actual = Token('==', "EQUALIF")
            else:
                self.actual = Token('=', "EQUALS")
            return self.actual

        elif self.origin[self.position] == '>':
            self.position += 1
            self.actual = Token('>', "GREATER")
            return self.actual

        elif self.origin[self.position] == '<':
            self.position += 1
            self.actual = Token('<', "LESSER")
            return self.actual

        elif self.origin[self.position] == '|':
            self.position += 1
            if self.origin[self.position] == "|":
                self.position += 1
                self.actual = Token('||', "OR")
            else:
                raise Exception("FALTOU A SEGUNDA BARRA")
            return self.actual

        elif self.origin[self.position] == '&':
            self.position += 1
            if self.origin[self.position] == "&":
                self.position += 1
                self.actual = Token('&&', "AND")
            else:
                raise Exception("FALTOU O SEGUNDO AND")
            return self.actual

        elif self.origin[self.position] == '!':
            self.position += 1
            self.actual = Token('!', "NOT")
            return self.actual

        elif self.origin[self.position] == '.':
            self.position += 1
            self.actual = Token('.', "DOT")
            return self.actual

        elif self.origin[self.position] == ',':
            self.position += 1
            self.actual = Token(',', "COMMA")
            return self.actual

        elif self.origin[self.position].isdigit():
            candidato = self.origin[self.position]
            self.position += 1
            isInt = True
            while isInt:
                if self.position == len(self.origin):
                    isInt = False
                elif self.origin[self.position].isdigit():
                    candidato += self.origin[self.position]
                    self.position += 1
                else:
                    isInt = False
            self.actual = Token(int(candidato), "INT")
            return self.actual

        elif self.origin[self.position] == '"':
            self.position += 1
            candidato = self.origin[self.position]
            self.position += 1
            isStr = True
            while isStr:
                # print(self.origin[self.position])
                if self.position == len(self.origin):
                    isStr = False
                elif self.origin[self.position] == '"':
                    isStr = False
                    self.position += 1
                else:
                    candidato += self.origin[self.position]
                    self.position += 1
            # print("candidato: ", candidato)
            self.actual = Token(str(candidato), "STR")
            return self.actual

        elif self.origin[self.position].isalpha():
            candidato = self.origin[self.position]
            self.position += 1
            isChar = True
            while isChar:
                if self.position == len(self.origin):
                    isChar = False
                elif self.origin[self.position].isalpha() or self.origin[self.position] == '_' or self.origin[self.position].isdigit():
                    candidato += self.origin[self.position]
                    self.position += 1
                else:
                    isChar = False
            if candidato == "printf":
                # print("print")
                self.actual = Token(candidato, "PRINT")

            elif candidato == "scanf":
                # print("print")
                self.actual = Token(candidato, "SCANF")

            elif candidato == "while":
                # print("print")
                self.actual = Token(candidato, "WHILE")

            elif candidato == "if":
                # print("print")
                self.actual = Token(candidato, "IF")

            elif candidato == "else":
                # print("print")
                self.actual = Token(candidato, "ELSE")

            elif candidato == "int":
                # print("print")
                self.actual = Token("INT", "TYPE")

            elif candidato == "str":
                # print("print")
                self.actual = Token("STR", "TYPE")

            else:
                # print("ident: ", candidato)
                self.actual = Token(candidato, "IDENT")
            return self.actual

        else:
            raise ValueError


class Parser:
    tokens = None

    def parseBlock():
        Node = Block("", [])
        # print(Parser.tokens.actual.value)
        if Parser.tokens.actual.type == "OPEN_BRACK":
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type != "CLOSE_BRACK":
                # print(Parser.tokens.actual.value)
                Node.children.append(Parser.parseStatement())
            Parser.tokens.selectNext()
        else:
            raise ValueError
        return Node

    def parseStatement():
        # print("Statement", Parser.tokens.actual.value)
        Node = None
        if Parser.tokens.actual.type == "IDENT":
            Node = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "EQUALS":
                Parser.tokens.selectNext()
                Node = Assignment("", [Node, Parser.parseRealExpression()])
                # print("Statement", Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "SEMI_COLON":
                # print("SEMI COLON")
                Parser.tokens.selectNext()
                return Node
            else:
                raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")

        if Parser.tokens.actual.type == "TYPE":
            Node = VarDec(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "IDENT":
                Node.children.append(Identifier(
                    Parser.tokens.actual.value, []))
                Parser.tokens.selectNext()
                # print(Parser.tokens.actual.value)
                while Parser.tokens.actual.type == "COMMA":
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type != "IDENT"):
                        raise ValueError("NOT IDENTIFIER")
                    else:
                        Node.children.append(Identifier(
                            Parser.tokens.actual.value, []))
                        Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "SEMI_COLON":
                    # print("SEMI COLON")
                    Parser.tokens.selectNext()
                    return Node
                else:
                    raise Exception("FALTOU PONTO E VIRGULA NA CRIACAO")

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            # print("210", Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                Node = Print("", [Parser.parseRealExpression()])
                # print("276", Parser.tokens.actual.value)
                if Parser.tokens.actual.type == "CLOSE_PAR":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "SEMI_COLON":
                        # print("SEMI COLON")
                        Parser.tokens.selectNext()
                        return Node
                    else:
                        raise Exception("PONTO E VIRGULA DO PRINT")
                else:
                    raise Exception("FALTOU FECHA PARENTESES DO PRINT")
            else:
                raise Exception("ABRE PARENTESES DO PRINT")

        elif Parser.tokens.actual.type == "WHILE":
            Parser.tokens.selectNext()
            # print("145", Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                # print("147", Parser.tokens.actual.value)
                Node = Parser.parseRealExpression()
                if Parser.tokens.actual.type == "CLOSE_PAR":
                    Parser.tokens.selectNext()
                    Node = While("", [Node, Parser.parseStatement()])
                    return Node
                else:
                    raise Exception("FALTOU FECHA PARENTESES DO WHILE")
            else:
                raise Exception("FALTOU ABRE PARENTESES DO WHILE")

        elif Parser.tokens.actual.type == "IF":
            Parser.tokens.selectNext()
            # print("145", Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                # print("147", Parser.tokens.actual.value)
                Node = Parser.parseRealExpression()
                # print("AAAAAA", Parser.tokens.actual.value)
                if Parser.tokens.actual.type == "CLOSE_PAR":
                    Parser.tokens.selectNext()
                    Node1 = If("", [Node, Parser.parseStatement()])
                    if Parser.tokens.actual.type == "ELSE":
                        Parser.tokens.selectNext()
                        Node2 = If("", [Node, Node1, Parser.parseStatement()])
                        return Node2
                    else:
                        return Node1
                else:
                    raise Exception("FALTOU FECHA PARENTESES DO IF")
            else:
                raise Exception("FALTOU ABRE PARENTESES DO IF")

        if Parser.tokens.actual.type == "SEMI_COLON":
            # print("SEMI_COLON DE NADA")
            Parser.tokens.selectNext()
            Node = NoOp("", [])
            return Node
        else:
            return Parser.parseBlock()

    def parseExpression():
        # print("EXPRESSION", Parser.tokens.actual.value)
        # print("Expression")
        Node = Parser.parseTerm()
        # print("BACK TO EXPRESSION", Parser.tokens.actual.value)

        while Parser.tokens.actual.type in ["PLUS", "MINUS", "OR", "DOT"]:
            if Parser.tokens.actual.type == "PLUS":
                # print("Plus")
                Parser.tokens.selectNext()
                # resultado += Parser.parseTerm()
                Node = BinOp("PLUS", [Node, Parser.parseTerm()])
            elif Parser.tokens.actual.type == "MINUS":
                # print("Minus")
                Parser.tokens.selectNext()
                # resultado -= Parser.parseTerm()
                Node = BinOp("MINUS", [Node, Parser.parseTerm()])

            elif Parser.tokens.actual.type == "OR":
                # print("Minus")
                Parser.tokens.selectNext()
                # resultado -= Parser.parseTerm()
                Node = BinOp("OR", [Node, Parser.parseTerm()])

            elif Parser.tokens.actual.type == "DOT":
                # print("DOT")
                Parser.tokens.selectNext()
                # resultado -= Parser.parseTerm()
                Node = BinOp("DOT", [Node, Parser.parseTerm()])
            else:
                raise ValueError("ERRO NO EXPRESSION")
        return Node

    def parseRealExpression():
        # print("REAL EXPRESSION", Parser.tokens.actual.value)
        # print("Expression")
        Node = Parser.parseExpression()
        # print("BACK TO REAL EXPRESSION", Parser.tokens.actual.value)

        while Parser.tokens.actual.type in ["EQUALIF", "LESSER", "GREATER"]:
            if Parser.tokens.actual.type == "EQUALIF":
                # print("Plus")
                Parser.tokens.selectNext()
                # resultado += Parser.parseTerm()
                Node = BinOp("EQUALIF", [Node, Parser.parseExpression()])

            elif Parser.tokens.actual.type == "LESSER":
                # print("Minus")
                Parser.tokens.selectNext()
                # resultado -= Parser.parseTerm()
                Node = BinOp("LESSER", [Node, Parser.parseExpression()])

            elif Parser.tokens.actual.type == "GREATER":
                # print("GREATER")
                Parser.tokens.selectNext()
                # resultado -= Parser.parseTerm()
                Node = BinOp("GREATER", [Node, Parser.parseExpression()])
            else:
                raise ValueError("NO IF CONDITIONS CORRECT OR FOUND")
        return Node

    def parseTerm():
        # print("Term", Parser.tokens.actual.value)
        Node = Parser.parseFactor()
        # print("Term back", Parser.tokens.actual.value)
        while Parser.tokens.actual.type in ["MULT", "DIV", "AND"]:
            if Parser.tokens.actual.type == "MULT":
                # print("Mult")
                Parser.tokens.selectNext()
                # resultado *= Parser.parseFactor()
                Node = BinOp("MULT", [Node, Parser.parseFactor()])
            elif Parser.tokens.actual.type == "DIV":
                # print("Div")
                Parser.tokens.selectNext()
                # resultado //= Parser.parseFactor()
                Node = BinOp("DIV", [Node, Parser.parseFactor()])

            elif Parser.tokens.actual.type == "AND":
                # print("Div")
                Parser.tokens.selectNext()
                # resultado //= Parser.parseFactor()
                Node = BinOp("AND", [Node, Parser.parseFactor()])
            else:
                raise ValueError("ERRO NO TERM")
        return Node

    def parseFactor():
        # print("Factor")
        Node = None
        # print("FACTOR", Parser.tokens.actual.value)
        if Parser.tokens.actual.type == "INT":
            # print("INT")
            # resultado = Parser.tokens.actual.value
            # print("tipo: ", type(Parser.tokens.actual.value))
            Node = IntVal(Parser.tokens.actual.value, None)
            Parser.tokens.selectNext()
            # print("AFTER INT", Parser.tokens.actual.value)
        elif Parser.tokens.actual.type == "STR":
            # print("STR")
            # resultado = Parser.tokens.actual.value
            # print("tipo: ", type(Parser.tokens.actual.value))
            Node = StrVal(Parser.tokens.actual.value, None)
            Parser.tokens.selectNext()
            # print("AFTER INT", Parser.tokens.actual.value)

        elif Parser.tokens.actual.type == "IDENT":
            # print("soma2")
            # resultado = Parser.parseFactor()
            Node = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            # print("AFTER IDENT", Parser.tokens.actual.value)

        elif Parser.tokens.actual.type == "PLUS":
            # print("soma2")
            Parser.tokens.selectNext()
            # resultado = Parser.parseFactor()
            Node = UnOp("PLUS", [Parser.parseFactor()])

        elif Parser.tokens.actual.type == "MINUS":
            # print("sub2")
            Parser.tokens.selectNext()
            # resultado = -Parser.parseFactor()
            Node = UnOp("MINUS", [Parser.parseFactor()])

        elif Parser.tokens.actual.type == "NOT":
            # print("sub2")
            Parser.tokens.selectNext()
            # resultado = -Parser.parseFactor()
            Node = UnOp("NOT", [Parser.parseFactor()])

        elif Parser.tokens.actual.type == "OPEN_PAR":
            # print("par")
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.value)

            Node = Parser.parseRealExpression()
            if Parser.tokens.actual.type == "CLOSE_PAR":
                # print("fechapar")
                Parser.tokens.selectNext()
            else:
                raise ValueError

        elif Parser.tokens.actual.type == "SCANF":
            # print("par")
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.value)

            if Parser.tokens.actual.type == "OPEN_PAR":
                # print("fechapar")
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "CLOSE_PAR":
                    Parser.tokens.selectNext()
                    Node = Scanf("", [])
                else:
                    raise ValueError("FALTOU FECHAR PARENTESES DO SCANF")
            else:
                raise ValueError("FALTOU ABRIR PARENTESES DO SCANF")
        else:
            raise ValueError
        # print("resultado: ", Node)
        return Node

    def run(arg):
        file = open(arg, "r")
        code_filtrado = PrePro.filter(file.read())
        # print(code_filtrado)
        file.close()
        Parser.tokens = Tokenizer(code_filtrado)
        Parser.table = SymbolTable()
        Parser.tokens.selectNext()
        resultado = Parser.parseBlock()
        if Parser.tokens.actual.type != "EOF":
            raise ValueError
        resultado.Evaluate()
        Asm.dump()


class PrePro:
    def filter(code):
        i = 0
        comentario = False
        string = ""
        size = len(code)
        while i < size:
            if comentario == True:
                string += code[i]
            if code[i] == '/' and comentario == False:
                string = code[i]
                if code[i+1] == '*':
                    comentario = True
            if comentario == True and code[i] == '*' and code[i+1] == '/':
                string += "/"
                code = code.replace(string, "")
                comentario = False
                i = 0
                size = len(code)
            i += 1
        return code


class Asm:
    code = open("cabecalho.asm").read()
    
    def write(cmd):
        Asm.code += (cmd + '\n')

    def dump():
        rodape = open("rodape.asm").read()
        Asm.code += (rodape)
        file = sys.argv[1].replace(".c", ".asm")
        program = open("{0}".format(file), 'w')
        program.write(Asm.code)
class Node:

    id = 0
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate():
        pass
    
    def newId():
        Node.id += 1
        return Node.id


class Assignment(Node):

    def Evaluate(self):
        SymbolTable.Setter(
            self.children[0], self.children[1].Evaluate())
        Asm.write("MOV [EBP - {0}], EBX".format(SymbolTable.table[self.children[0].value][2]))



class Block(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()


class Print(Node):
    def Evaluate(self):
        children = self.children[0].Evaluate()[0]
        Asm.write("PUSH EBX ; inicio do print")
        Asm.write("CALL print ; chamada de funcao")
        Asm.write("POP EBX ; Desempilhe os argumentos")
        # print(children)


class Scanf(Node):

    def Evaluate(self):
        return (int(input()), "INT")


class While(Node):

    def Evaluate(self):
        Asm.write("LOOP_{0}:".format(self.id))
        self.children[0].Evaluate()
        Asm.write("CMP EBX, False ; verifica se o teste deu falso")
        Asm.write("JE EXIT_{0} ; e sai caso for igual a falso.".format(self.id))
        self.children[1].Evaluate()
        Asm.write("JMP LOOP_{0} ; e sai caso for igual a falso.".format(self.id))
        Asm.write("EXIT_{0}:".format(self.id))


class If(Node):

    def Evaluate(self):
        # print(self.children[1].value)
        if self.children[0].Evaluate()[0]:
            self.children[1].Evaluate()
        elif len(self.children) > 2:
            self.children[2].Evaluate()


class If(Node):
    def Evaluate(self):
        self.children[0].Evaluate()
        Asm.write("CMP EBX,  False")
        if len(self.children) > 2:
            Asm.write("JE LABEL_{0}".format(self.id))
        else:
            Asm.write("JE EXIT_{0}".format(self.id))

        self.children[1].Evaluate()
        Asm.write("JMP EXIT_{0}".format(self.id))

        if len(self.children) > 2:
            Asm.write("LABEL_{0}:".format(self.id))
            self.children[2].Evaluate()
            Asm.write("JMP EXIT_{0}".format(self.id))

        Asm.write("EXIT_{0}:".format(self.id))


class Identifier(Node):

    def Evaluate(self):
        # print(SymbolTable.Getter(self.value))
        Asm.write("MOV EBX, [EBP - {0}]".format(SymbolTable.Getter(self.value)[2]))
        return SymbolTable.Getter(self.value)


class VarDec(Node):

    def Evaluate(self):
        Asm.write("PUSH DWORD 0")
        for child in self.children:
            SymbolTable.Create(child.value, self.value)


class BinOp(Node):

    def Evaluate(self):
        right = self.children[0].Evaluate()
        Asm.write("PUSH EBX")
        left = self.children[1].Evaluate()
        Asm.write("POP EAX")
        # print(right, left, "right and left")
        if right[1] == 'INT' and left[1] == 'INT':
            if self.value == "PLUS":
                Asm.write("ADD EAX, EBX")
                Asm.write("MOV EBX, EAX")
                return (None, None)
            if self.value == "MINUS":
                Asm.write("SUB EAX, EBX")
                Asm.write("MOV EBX, EAX")
                return (None, None)
            if self.value == "DIV":
                Asm.write("IDIV EBX")
                Asm.write("MOV EBX, EAX")
                return (None, None)
            if self.value == "MULT":
                Asm.write("IMUL EBX")
                Asm.write("MOV EBX, EAX")
                return (None, None)
            if self.value == "OR":
                Asm.write("OR EAX, EBX")
                Asm.write("MOV EBX, EAX")
                return (None, None)
            if self.value == "AND":
                Asm.write("AND EAX, EBX")
                Asm.write("MOV EBX, EAX")
                return (None, None)

        if self.value == "EQUALIF":
            Asm.write("CMP EAX, EBX ; comparacao igual")
            Asm.write("CALL binop_je")
            return (None, None)
        if self.value == "GREATER":
            Asm.write("CMP EAX, EBX ; comparacao maior que")
            Asm.write("CALL binop_jg")
            return (None, None)
        if self.value == "LESSER":
            Asm.write("CMP EAX, EBX ; comparacao menor que")
            Asm.write("CALL binop_jl")
            return (None, None)

        # if self.value == "DOT":
        #     return (str(right[0]) + str(left[0]), "STR")
        


class UnOp(Node):

    def Evaluate(self):
        # print("UnOp")
        if self.value == "PLUS":
            return (self.children[0].Evaluate()[0], 'INT')
        if self.value == "MINUS":
            return (-self.children[0].Evaluate()[0], 'INT')
        if self.value == "NOT":
            return (not(self.children[0].Evaluate()[0]), 'INT')


class IntVal(Node):

    def Evaluate(self):
        # print(self.value)
        # print(type(self.value))
        cmd = "MOV EBX, " + str(self.value)
        Asm.write(cmd)
        return (self.value, 'INT')


class StrVal(Node):

    def Evaluate(self):
        return(self.value, 'STR')


class NoOp(Node):

    def Evaluate(self):
        pass


class SymbolTable:

    table = {}
    adder = 0

    def Create(chave, tipo):
        if chave in SymbolTable.table:
            raise Exception("VARIAVEL DEFINIDA DUAS VEZES")
        else:
            SymbolTable.adder += 4
            SymbolTable.table[chave] = (None, tipo, SymbolTable.adder)

    def Getter(chave):
        if chave in SymbolTable.table:
            return SymbolTable.table[chave]
        else:
            raise Exception("VARIAVEL NAO DEFINIDA")

    def Setter(chave, valor):
        if chave.value in SymbolTable.table:
            if valor[1] == SymbolTable.table[chave.value][1]:
                trinca = (valor[0], valor[1], SymbolTable.table[chave.value][2])
                SymbolTable.table[chave.value] = trinca
        else:
            raise Exception("VARIAVEL NAO DEFINIDA")


arg = sys.argv[1]
Parser.run(arg)
# Parser.run("input.c")
