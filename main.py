import sys


class Token:
    def _init_(self, value, type):
        self.type = type
        self.value = value


class Tokenizer:
    def _init_(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
        if self.position >= len(self.origin):
            self.actual = Token(" ", "EOF")
            return self.actual

        if self.origin[self.position] == ' ':
            self.position += 1
            while self.origin[self.position] == ' ':
                self.position += 1
            if self.origin[self.position].isdigit():
                raise ValueError

        if self.origin[self.position] == '+':
            self.position += 1
            self.actual = Token('+', "PLUS")
            return self.actual

        elif self.origin[self.position] == '-':
            self.position += 1
            self.actual = Token('-', "MINUS")
            return self.actual

        elif self.origin[self.position].isdigt():
            candidato += self.origin[self.position]
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
        Parser.tokens.selectNext()
        resultado = None
        if Parser.tokens.actual.type == "INT":
            resultado = Parser.tokens.actual
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
                if Parser.tokens.actual.type == "PLUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        resultado += Parser.tokens.actual
                    else:
                        raise ValueError
                if Parser.tokens.actual.type == "MINUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        resultado -= Parser.tokens.actual
                    else:
                        raise ValueError
                Parser.tokens.selectNext()
            return resultado
        else:
            raise ValueError

    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()


arg = sys.argv[1]
print(Parser.run(arg))
