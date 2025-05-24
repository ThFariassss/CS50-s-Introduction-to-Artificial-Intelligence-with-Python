# =========================
# Lógica do Problema de Cores e Posições
# =========================
from logic import *
cores = ["vermelho", "azul", "verde", "amarelo"]
simbolos = []

for i in range(4):
    for cor in cores:
        simbolos.append(Simbolo(f"{cor}{i}"))

conhecimento = E()

# Cada cor deve ocupar uma posição
for cor in cores:
    conhecimento.adicionar(Ou(
        Simbolo(f"{cor}0"),
        Simbolo(f"{cor}1"),
        Simbolo(f"{cor}2"),
        Simbolo(f"{cor}3")
    ))

# Cada cor em no máximo uma posição
for cor in cores:
    for i in range(4):
        for j in range(4):
            if i != j:
                conhecimento.adicionar(Implicacao(
                    Simbolo(f"{cor}{i}"), Nao(Simbolo(f"{cor}{j}"))
                ))

# Cada posição com no máximo uma cor
for i in range(4):
    for c1 in cores:
        for c2 in cores:
            if c1 != c2:
                conhecimento.adicionar(Implicacao(
                    Simbolo(f"{c1}{i}"), Nao(Simbolo(f"{c2}{i}"))
                ))

# Pelo menos dois pares corretos
conhecimento.adicionar(Ou(
    E(Simbolo("vermelho0"), Simbolo("azul1"), Nao(Simbolo("verde2")), Nao(Simbolo("amarelo3"))),
    E(Simbolo("vermelho0"), Simbolo("verde2"), Nao(Simbolo("azul1")), Nao(Simbolo("amarelo3"))),
    E(Simbolo("vermelho0"), Simbolo("amarelo3"), Nao(Simbolo("azul1")), Nao(Simbolo("verde2"))),
    E(Simbolo("azul1"), Simbolo("verde2"), Nao(Simbolo("vermelho0")), Nao(Simbolo("amarelo3"))),
    E(Simbolo("azul1"), Simbolo("amarelo3"), Nao(Simbolo("vermelho0")), Nao(Simbolo("verde2"))),
    E(Simbolo("verde2"), Simbolo("amarelo3"), Nao(Simbolo("vermelho0")), Nao(Simbolo("azul1")))
))

# Pares incorretos
conhecimento.adicionar(E(
    Nao(Simbolo("azul0")),
    Nao(Simbolo("vermelho1")),
    Nao(Simbolo("verde2")),
    Nao(Simbolo("amarelo3"))
))

# Descobre os símbolos verdadeiros
for simbolo in simbolos:
    if verificar_modelo(conhecimento, simbolo):
        print(f"{simbolo} é verdadeiro")