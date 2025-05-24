import termcolor
from Logica.logic import *

# Símbolos: suspeitos
mustard = Simbolo("CoronelMostarda")
plum = Simbolo("ProfessorPlum")
scarlet = Simbolo("SrtaScarlet")
personagens = [mustard, plum, scarlet]

# Símbolos: cômodos 
salao = Simbolo("SalaoDeBaile")
cozinha = Simbolo("Cozinha")
biblioteca = Simbolo("Biblioteca")
comodos = [salao, cozinha, biblioteca]

# Símbolos: armas
faca = Simbolo("Faca")
revolver = Simbolo("Revolver")
chave_inglesa = Simbolo("ChaveInglesa")
armas = [faca, revolver, chave_inglesa]

# Todos os símbolos
simbolos = personagens + comodos + armas


def checar_conhecimento(conhecimento):
    for simbolo in simbolos:
        if verificar_modelo(conhecimento, simbolo):
            termcolor.cprint(f"{simbolo}: SIM", "green")
        elif not verificar_modelo(conhecimento, Nao(simbolo)):
            print(f"{simbolo}: TALVEZ")


# Há uma pessoa, um cômodo e uma arma
conhecimento = E(
    Ou(*personagens),
    Ou(*comodos),
    Ou(*armas)
)

# Cartas que sabemos que NÃO estão envolvidas
conhecimento.add(E(
    Nao(mustard),
    Nao(cozinha),
    Nao(revolver)
))

# Informação incerta (uma das três não está envolvida, mas não sabemos qual)
conhecimento.add(Ou(
    Nao(scarlet),
    Nao(biblioteca),
    Nao(chave_inglesa)
))

# Outras exclusões
conhecimento.add(Nao(plum))
conhecimento.add(Nao(salao))

# Verificar resultado
checar_conhecimento(conhecimento)
