# import sys


# class Token:
#     def _init_(self, value, type):
#         self.type = type
#         self.value = value


# class Tokenizer:
#     def _init_(self, origin):
#         self.origin = origin
#         self.position = 0
#         self.actual = None

#     def selectNext(self):
#         if self.position >= len(self.origin):
#             self.actual = Token(" ", "EOF")
#             return self.actual

#         if self.origin[self.position] == ' ':
#             self.position += 1
#             while self.origin[self.position] == ' ':
#                 self.position += 1
#             if self.origin[self.position].isdigit():
#                 raise ValueError

#         if self.origin[self.position] == '+':
#             self.position += 1
#             self.actual = Token('+', "PLUS")
#             return self.actual

#         elif self.origin[self.position] == '-':
#             self.position += 1
#             self.actual = Token('-', "MINUS")
#             return self.actual

#         elif self.origin[self.position].isdigt():
#             candidato += self.origin[self.position]
#             self.position += 1
#             isInt = True
#             while isInt:
#                 if self.position == len(self.origin):
#                     isInt = False
#                 elif self.origin[self.position].isdigit():
#                     candidato += self.origin[self.position]
#                     self.position += 1
#                 else:
#                     isInt = False

#             self.actual = Token(int(candidato), "INT")
#             return self.actual

#         else:
#             raise ValueError


# class Parser:
#     tokens = None

#     def parseExpression():
#         Parser.tokens.selectNext()
#         resultado = None
#         if Parser.tokens.actual.type == "INT":
#             resultado = Parser.tokens.actual
#             Parser.tokens.selectNext()
#             while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
#                 if Parser.tokens.actual.type == "PLUS":
#                     Parser.tokens.selectNext()
#                     if Parser.tokens.actual.type == "INT":
#                         resultado += Parser.tokens.actual
#                     else:
#                         raise ValueError
#                 if Parser.tokens.actual.type == "MINUS":
#                     Parser.tokens.selectNext()
#                     if Parser.tokens.actual.type == "INT":
#                         resultado -= Parser.tokens.actual
#                     else:
#                         raise ValueError
#                 Parser.tokens.selectNext()
#             return resultado
#         else:
#             raise ValueError

#     def run(code):
#         Parser.tokens = Tokenizer(code)
#         return Parser.parseExpression()


# arg = sys.argv[1]
# print(Parser.run(arg))


import sys


class Token:

    def _init_(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:

    def _init_(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
        if self.position >= len(self.origin):
            self.actual = Token('EOF', '-')
            return self.actual

        if self.origin[self.position] == ' ':
            self.position += 1
            while self.origin[self.position] == ' ':
                self.position += 1
            if self.origin[self.position].isdigit():
                sys.stderr.write("Invalid input")

        if self.origin[self.position] == '+':
            self.position += 1
            self.actual = Token('PLUS', '+')
            return self.actual

        elif self.origin[self.position] == '-':
            self.position += 1
            self.actual = Token('MINUS', '-')
            return self.actual

        elif self.origin[self.position].isdigit():
            candidato = self.origin[self.position]
            self.position += 1
            index_in_range = True
            while index_in_range:
                if self.position == len(self.origin):
                    index_in_range = False
                elif self.origin[self.position].isdigit():
                    candidato += self.origin[self.position]
                    self.position += 1
                else:
                    index_in_range = False

            self.actual = Token('INT', candidato)
            return self.actual


class Parser:

    token = None

    def ParseExpression():
        Parser.token.selectNext()
        if Parser.token.actual.type == 'INT':
            resultado = int(Parser.token.actual.value)
            Parser.token.selectNext()
            while Parser.token.actual.type == 'PLUS' or Parser.token.actual.type == 'MINUS':
                if Parser.token.actual.type == 'PLUS':
                    Parser.token.selectNext()
                    if Parser.token.actual.type == 'INT':
                        resultado += int(Parser.token.actual.value)
                    else:
                        sys.stderr.write("Invalid input")
                if Parser.token.actual.type == 'MINUS':
                    Parser.token.selectNext()
                    if Parser.token.actual.type == 'INT':
                        resultado -= int(Parser.token.actual.value)
                    else:
                        sys.stderr.write("Invalid input")
                Parser.token.selectNext()
            return resultado
        else:
            sys.stderr.write("Invalid input")

    def run(code):
        Parser.token = Tokenizer(code)
        return Parser.ParseExpression()


arguments = sys.argv[1]
print(Parser.run(arguments))
