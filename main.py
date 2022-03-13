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
        if self.position >= len(self.origin):
            self.actual = Token("", "EOF")
            return self.actual

        if self.origin[self.position] == ' ':
            self.position += 1
            while self.origin[self.position] == ' ':
                self.position += 1
            # if self.origin[self.position].isdigit():
            #     raise ValueError

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

        else:
            raise ValueError


class Parser:
    tokens = None

    def parseExpression():
        resultado = Parser.parseTerm()

        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                resultado += Parser.parseTerm()
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                resultado -= Parser.parseTerm()
            else:
                raise ValueError
        return resultado

    def parseTerm():

        resultado = None
        if Parser.tokens.actual.type == "INT":
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()

            while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
                if Parser.tokens.actual.type == "MULT":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        resultado *= Parser.tokens.actual.value
                        print(resultado)
                    else:
                        # print("1")
                        raise ValueError
                elif Parser.tokens.actual.type == "DIV":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        resultado /= Parser.tokens.actual.value
                    else:
                        # print("2")
                        raise ValueError
                else:
                    # print("3")
                    raise ValueError
                Parser.tokens.selectNext()
            return resultado
        else:
            # print("4")
            raise ValueError

    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        return Parser.parseExpression()


# class PrePro:
#     def filter():
#         return code


arg = sys.argv[1]
print(Parser.run(arg))
