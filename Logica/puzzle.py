from Logica.logic import *

# Pessoas e casas
pessoas = ["Gilderoy", "Pomona", "Minerva", "Horace"]
casas = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

# Lista de símbolos
simbolos = []
conhecimento = E()

# Criar todos os símbolos pessoa+casa
for pessoa in pessoas:
    for casa in casas:
        simbolos.append(Simbolo(f"{pessoa}{casa}"))

# Cada pessoa pertence a uma casa
for pessoa in pessoas:
    conhecimento.add(Ou(
        Simbolo(f"{pessoa}Gryffindor"),
        Simbolo(f"{pessoa}Hufflepuff"),
        Simbolo(f"{pessoa}Ravenclaw"),
        Simbolo(f"{pessoa}Slytherin")
    ))

# Cada pessoa em apenas uma casa
for pessoa in pessoas:
    for c1 in casas:
        for c2 in casas:
            if c1 != c2:
                conhecimento.add(
                    Implicacao(Simbolo(f"{pessoa}{c1}"), Nao(Simbolo(f"{pessoa}{c2}")))
                )

# Apenas uma pessoa por casa
for casa in casas:
    for p1 in pessoas:
        for p2 in pessoas:
            if p1 != p2:
                conhecimento.add(
                    Implicacao(Simbolo(f"{p1}{casa}"), Nao(Simbolo(f"{p2}{casa}")))
                )

# Conhecimentos adicionais:
# Gilderoy está em Gryffindor ou Ravenclaw
conhecimento.add(Ou(Simbolo("GilderoyGryffindor"), Simbolo("GilderoyRavenclaw")))

# Pomona NÃO está em Slytherin
conhecimento.add(Nao(Simbolo("PomonaSlytherin")))

# Minerva está em Gryffindor
conhecimento.add(Simbolo("MinervaGryffindor"))

# Checar o modelo
for simbolo in simbolos:
    if verificar_modelo(conhecimento, simbolo):
        print(f"{simbolo}: SIM")
    elif not verificar_modelo(conhecimento, Nao(simbolo)):
        print(f"{simbolo}: TALVEZ")
