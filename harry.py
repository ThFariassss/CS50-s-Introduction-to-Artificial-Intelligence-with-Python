from logic import *

chuva = Simbolo("chuva")
hagrid = Simbolo("hagrid")
dumbledore = Simbolo("dumbledore")

conhecimento = E(
    Implicacao(Nao(chuva), hagrid),
    Ou(hagrid, dumbledore),
    Nao(E(hagrid, dumbledore)),
    dumbledore
)

print(verificar_modelo(conhecimento, chuva))
