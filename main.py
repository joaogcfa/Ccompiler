from curses.ascii import isdigit
from select import select
import sys


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
                Node = Assignment("", [Node, Parser.parseExpression()])
            if Parser.tokens.actual.type == "SEMI_COLON":
                # print("SEMI COLON")
                Parser.tokens.selectNext()
                return Node
            else:
                raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            # print("210", Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                # print("147", Parser.tokens.actual.value)
                Node = Print("", [Parser.parseExpression()])
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
                    Node = If("", [Node, Parser.parseStatement()])
                    return Node
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
            raise ValueError

    def parseExpression():
        # print("EXPRESSION", Parser.tokens.actual.value)
        # print("Expression")
        Node = Parser.parseTerm()
        # print("BACK TO EXPRESSION", Parser.tokens.actual.value)

        while Parser.tokens.actual.type in ["PLUS", "MINUS", "OR"]:
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
            else:
                raise ValueError("ERRO NO EXPRESSION")
        return Node

    def parseRealExpression():
        # print("EXPRESSION", Parser.tokens.actual.value)
        # print("Expression")
        Node = Parser.parseExpression()
        # print("BACK TO EXPRESSION", Parser.tokens.actual.value)

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
                # print("Minus")
                Parser.tokens.selectNext()
                # resultado -= Parser.parseTerm()
                Node = BinOp("GREATER", [Node, Parser.parseExpression()])
            else:
                raise ValueError("NO IF CONDITIONS CORRECT OR FOUND")
        return Node

    def parseTerm():
        # print("Term", Parser.tokens.actual.value)
        Node = Parser.parseFactor()

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
        return resultado.Evaluate()


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


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate():
        pass


class Assignment(Node):

    def Evaluate(self):
        SymbolTable.Setter(
            self.children[0], self.children[1].Evaluate())


class Block(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()


class Print(Node):
    def Evaluate(self):
        children = self.children[0].Evaluate()
        print(children)


class Scanf(Node):

    def Evaluate(self):
        return int(input())


class While(Node):

    def Evaluate(self):
        while self.children[0].Evaluate():
            self.children.children[1].Evaluate()


class If(Node):

    def Evaluate(self):
        if self.children[0].Evaluate():
            self.children[1].Evaluate()
        elif len(self.children) > 2:
            self.children[2].Evaluate()


class Identifier(Node):

    def Evaluate(self):
        return SymbolTable.Getter(self.value)


class BinOp(Node):

    def Evaluate(self):
        right = self.children[0].Evaluate()
        left = self.children[1].Evaluate()
        # print(right, left, "right and left")
        if self.value == "PLUS":
            return right + left
        if self.value == "MINUS":
            return right - left
        if self.value == "DIV":
            return right//left
        if self.value == "MULT":
            return right*left
        if self.value == "EQUALIF":
            return right == left
        if self.value == "GREATER":
            return right > left
        if self.value == "LESSER":
            return right < left
        if self.value == "OR":
            return right or left
        if self.value == "AND":
            return right and left


class UnOp(Node):

    def Evaluate(self):
        # print("UnOp")
        if self.value == "PLUS":
            return self.children[0].Evaluate()
        if self.value == "MINUS":
            return -self.children[0].Evaluate()
        if self.value == "NOT":
            return not(self.children[0].Evaluate())


class IntVal(Node):

    def Evaluate(self):
        # print(self.value)
        # print(type(self.value))
        return self.value


class NoOp(Node):

    def Evaluate(self):
        pass


class SymbolTable:

    table = {}

    def Getter(chave):
        # print("chave: ", chave)
        # print("chave com valor: ", SymbolTable.table[chave])
        if chave in dict.keys(SymbolTable.table):
            return SymbolTable.table[chave]
        else:
            raise Exception("VARIAVEL NAO DEFINIDA")

    def Setter(chave, valor):
        SymbolTable.table[chave.value] = valor
        # print("table", SymbolTable.table)


arg = sys.argv[1]
Parser.run(arg)
# Parser.run("input.c")
# print(Parser.run("/* a */ 1 /* b */"))
