from ast import arguments
from curses.ascii import isdigit
from multiprocessing.sharedctypes import Value
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
            
            elif candidato == "return":
                # print("print")
                self.actual = Token(candidato, "RETURN")
            
            elif candidato == "void":
                # print("print")
                self.actual = Token(candidato, "TYPE")

            else:
                # print("ident: ", candidato)
                self.actual = Token(candidato, "IDENT")
            return self.actual

        else:
            raise ValueError


class Parser:
    tokens = None

    def parseProgram():
        nodeBlock = Block("", [])
        while Parser.tokens.actual.type != "EOF":
            nodeBlock.children.append(Parser.parseDeclaration())
        return nodeBlock

    def parseDeclaration():
        

        if Parser.tokens.actual.type == "TYPE":
            NodeFuncDec = FuncDec(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "IDENT":
                NodeVar = VarDec(Parser.tokens.actual.value, [])
                NodeVar.children.append(Identifier(
                    Parser.tokens.actual.value, []))
                NodeFuncDec.children.append(NodeVar)
                Parser.tokens.selectNext()


                if Parser.tokens.actual.type == "OPEN_PAR":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.type == "CLOSE_PAR":
                        Parser.tokens.selectNext()
                        nodeBlock =Parser.parseBlock()
                        NodeFuncDec.children.append(nodeBlock)

                    elif Parser.tokens.actual.type == "TYPE":
                        NodeVar = VarDec(Parser.tokens.actual.value, [])
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.type == "IDENT":
                            NodeVar.children.append(Identifier(
                                Parser.tokens.actual.value, []))
                            NodeFuncDec.children.append(NodeVar)
                            Parser.tokens.selectNext()

                            while Parser.tokens.actual.type == "COMMA":
                                Parser.tokens.selectNext()

                                if Parser.tokens.actual.type == "TYPE":
                                    NodeVar = VarDec(Parser.tokens.actual.value, [])
                                    Parser.tokens.selectNext()

                                    if Parser.tokens.actual.type == "IDENT":
                                        NodeVar.children.append(Identifier(
                                            Parser.tokens.actual.value, []))
                                        NodeFuncDec.children.append(NodeVar)
                                        Parser.tokens.selectNext()

                                    else:
                                        raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")

                                else:
                                    raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")

                            if Parser.tokens.actual.type == "CLOSE_PAR":
                                nodeBlock = Parser.parseBlock()

                            else:
                                raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")
                        else:
                            raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")
                    else:
                        raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")
                else:
                    raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")
            else:
                raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")
            
        else:
            raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")
        return NodeFuncDec


    def parseBlock():
        Node = Block("", [])
        if Parser.tokens.actual.type == "OPEN_BRACK":
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type not in ["CLOSE_BRACK", "RETURN"]:
                Node.children.append(Parser.parseStatement())
            Parser.tokens.selectNext()
        else:
            raise ValueError
        return Node

    def parseStatement():
        # print("Statement", Parser.tokens.actual.value)
        Node = None
        if Parser.tokens.actual.type == "IDENT":
            func_call = Parser.tokens.actual.value
            arguments = []
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
            elif Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "CLOSE_PAR":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "SEMI_COLON":
                        Parser.tokens.selectNext()
                        return FuncCall(func_call, [])
                    else:
                        raise Exception("FALTOU PONTO E VIRGULA NA CRIACAO") 
                else:
                    Node = Parser.parseRealExpression()
                    arguments.append(Node)
                    while Parser.tokens.actual.type == "COMMA":
                        Parser.tokens.selectNext()
                        arguments.append(Parser.parseRealExpression())
                    if Parser.tokens.actual.type == "CLOSE_PAR":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == "SEMI_COLON":
                            Parser.tokens.selectNext()
                            return FuncCall(func_call, arguments)
                        else:
                            raise Exception("FALTOU PONTO E VIRGULA OU IGUAL")
                    else:
                        raise Exception("FALTOU FECHA PARENTESES")

        if Parser.tokens.actual.type == "TYPE":
            Node = VarDec(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "IDENT":
                Node.children.append(Identifier(
                    Parser.tokens.actual.value, []))
                Parser.tokens.selectNext()
                # print("TYPE", Parser.tokens.actual.value)
                while Parser.tokens.actual.type == "COMMA":
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type != "IDENT"):
                        raise ValueError("NOT IDENTIFIER")
                    else:
                        Node.children.append(Identifier(
                            Parser.tokens.actual.value, []))
                        Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "SEMI_COLON":
                    Parser.tokens.selectNext()
                    # print(Parser.tokens.actual.value)
                    return Node
                else:
                    raise Exception("FALTOU PONTO E VIRGULA NA CRIACAO")

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            # print("210", Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                # print("384", Parser.tokens.actual.value)
                Node = Print("", [Parser.parseRealExpression()])
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

        elif Parser.tokens.actual.type == "RETURN":
            Node = Return("", [])
            Parser.tokens.selectNext()
            # print("210", Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                Node.children.append(Parser.parseStatement())
                # print("276", Parser.tokens.actual.value)
                if Parser.tokens.actual.type == "CLOSE_PAR":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "SEMI_COLON":
                        # print("SEMI COLON")
                        Parser.tokens.selectNext()
                        return Node
                    else:
                        raise Exception("PONTO E VIRGULA DO RETURN")
                else:
                    raise Exception("FALTOU FECHA PARENTESES DO RETURN")
            else:
                raise Exception("ABRE PARENTESES DO RETURNN")

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
            value = Parser.tokens.actual.value
            arguments = []
            # Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN_PAR":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "CLOSE_PAR":
                    Parser.tokens.selectNext()
                    return FuncCall(value, [])
                else:
                    Node = Parser.parseRealExpression()
                    arguments.append(Node)
                    while Parser.tokens.actual.type == "COMMA":
                        Parser.tokens.selectNext()
                        arguments.append(Parser.parseRealExpression())
                    if Parser.tokens.actual.type == "CLOSE_PAR":
                        Parser.tokens.selectNext()
                        return FuncCall(value, arguments)
                    else:
                        raise Exception("FALTOU FECHA PARENTESES")
            else:
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
        Parser.tokens.selectNext()
        resultado = Parser.parseProgram()
        if Parser.tokens.actual.type != "EOF":
            raise ValueError
        else:
            Parser.table = SymbolTable()
            Node = FuncCall("main", [])
            resultado.children.append(Node)
            return resultado.Evaluate(Parser.table)

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

    def Evaluate(self, st):
        st.Setter(
            self.children[0], self.children[1].Evaluate(st))


class Block(Node):
    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)


class Print(Node):
    def Evaluate(self, st):
        children = self.children[0].Evaluate(st)[0]
        print(children)


class Scanf(Node):

    def Evaluate(self, st):
        return (int(input()), "INT")


class While(Node):

    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)


class If(Node):

    def Evaluate(self, st):
        # print(self.children[1].value)
        if self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)


class Identifier(Node):

    def Evaluate(self, st):
        return st.Getter(self.value)


class VarDec(Node):

    def Evaluate(self, st):
        # print("oi")
        for child in self.children:
            st.Create(child.value, self.value)


class BinOp(Node):

    def Evaluate(self, st):
        right = self.children[0].Evaluate(st)
        left = self.children[1].Evaluate(st)
        # print(right, left, "right and left")
        if right[1] == 'INT' and left[1] == 'INT':
            if self.value == "PLUS":
                return (right[0] + left[0], "INT")
            if self.value == "MINUS":
                return (right[0] - left[0], "INT")
            if self.value == "DIV":
                return (right[0]//left[0], "INT")
            if self.value == "MULT":
                return (right[0]*left[0], "INT")
            if self.value == "OR":
                return (right[0] or left[0], "INT")
            if self.value == "AND":
                return (right[0] and left[0], "INT")

        if right[1] == left[1]:
            if self.value == "EQUALIF":
                return (int(right[0] == left[0]), "INT")
            if self.value == "GREATER":
                return (int(right[0] > left[0]), "INT")
            if self.value == "LESSER":
                return (int(right[0] < left[0]), "INT")

        if self.value == "DOT":
            return (str(right[0]) + str(left[0]), "STR")


class UnOp(Node):

    def Evaluate(self, st):
        # print("UnOp")
        if self.value == "PLUS":
            return (self.children[0].Evaluate(st)[0], 'INT')
        if self.value == "MINUS":
            return (-self.children[0].Evaluate(st)[0], 'INT')
        if self.value == "NOT":
            return (not(self.children[0].Evaluate(st)[0]), 'INT')


class IntVal(Node):

    def Evaluate(self, st):
        # print(self.value)
        # print(type(self.value))
        return (self.value, 'INT')


class StrVal(Node):

    def Evaluate(self, st):
        return(self.value, 'STR')


class NoOp(Node):

    def Evaluate(self, st):
        pass


class FuncDec(Node):

    def Evaluate(self, st):
        FuncTable.Create(self.children[0].value, self)
        
class FuncCall(Node):

    def Evaluate(self, st):
        table = SymbolTable()

        tipo, declaration = FuncTable.Getter(self.value)
        values = []

        for child in range(1, len(self.children)-1):
            declaration.children[child].Evaluate(table)
            val = declaration.children[child].children[0].value
            values.append(val)

        for child in range(0, len(self.children)-1):
            arg = child.Evaluate(st)
            table.Setter(values[child], arg)

        return declaration.children[-1].Evaluate(table)
class Return(Node):

    def Evaluate(self, st):
        return self.children[0].Evaluate(st)


class FuncTable:

    funcTable = {}

    def Create(chave, tipo):
        # print("chave", chave)
        if chave in FuncTable.funcTable:
            raise Exception("VARIAVEL DEFINIDA DUAS VEZES")
        else:
            FuncTable.funcTable[chave] = (None, tipo)

    def Getter(chave):
        # print("chave", chave)
        if chave in FuncTable.funcTable:
            return FuncTable.funcTable[chave]
        else:
            raise Exception("FUNCAO NAO DEFINIDA")

    def Setter(chave, valor):
        if chave.value in FuncTable.funcTable:
            if valor[1] == FuncTable.funcTable[chave.value][1]:
                FuncTable.funcTable[chave.value] = valor
        else:
            raise Exception("FUNCAO NAO DEFINIDA")

class SymbolTable:

    def __init__(self):
        self.table = {}

    def Create(self, chave, tipo):
        # print("table: ", chave)
        if chave in self.table:
            raise Exception("VARIAVEL DEFINIDA DUAS VEZES")
        else:
            self.table[chave] = (None, tipo)
            # print(self.table)

    def Getter(self, chave):
        if chave in self.table:
            return self.table[chave]
        else:
            raise Exception("VARIAVEL NAO DEFINIDA")

    def Setter(self, chave, valor):
        # print(chave.value)
        if chave.value in self.table:
            if valor[1] == self.table[chave.value][1]:
                self.table[chave.value] = valor
        else:
            raise Exception("VARIAVEL NAO DEFINIDA")


arg = sys.argv[1]
Parser.run(arg)
# Parser.run("input.c")
