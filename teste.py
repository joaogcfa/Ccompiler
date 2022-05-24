from curses.ascii import isdigit
from multiprocessing.sharedctypes import Value
from select import select
import sys

class Asm:
    code = open("cabecalho.asm").read()
    
    def write(cmd):
        Asm.code += (cmd + '\n')

    def dump():
        rodape = open("rodape.asm").read()
        Asm.code += (rodape)
        program = open("program.asm", 'w')
        program.write(Asm.code)

Asm.write("comando")
Asm.write("comando2")
Asm.dump()
print(Asm.code)