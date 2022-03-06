import sys

arg = sys.argv[1]
size = len(arg)

i = 0
total = 0
num = ""
arg_cleaned = ""
sinal = ''
primeiro = True


while i != size:
    if arg[i] != " ":
        arg_cleaned += arg[i]
    i += 1

i = 0
while i != size:
    if arg[i] == '+':
        valor = int(num)
        total += valor
        num = ""
        sinal = arg[i]
    elif arg[i] == '-':
        if primeiro == True:
            valor = int(num)
            total += valor
            num = ""
        else:
            valor = int(num)
            total -= valor
            num = ""
        primeiro = False
        sinal = arg[i]
    else:
        num += arg[i]
    i += 1

if sinal == '-':
    valor = int(num)
    total -= valor
else:
    valor = int(num)
    total += valor

print(total)
