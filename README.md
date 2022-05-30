# Statys dos testes

![git status](http://3.129.230.99/svg/joaogcfa/JoaoCompiler)



V2.4:
BLOCK = "{", { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGNMENT | PRINT), ";" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "printf", "(", EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
