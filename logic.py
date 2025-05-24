import itertools

class Sentenca():

    def avaliar(self, modelo):
        """Avalia a sentença lógica."""
        raise Exception("nada para avaliar")

    def formula(self):
        """Retorna a fórmula em string representando a sentença lógica."""
        return ""

    def simbolos(self):
        """Retorna um conjunto com todos os símbolos da sentença lógica."""
        return set()

    @classmethod
    def validar(cls, sentenca):
        if not isinstance(sentenca, Sentenca):
            raise TypeError("deve ser uma sentença lógica")

    @classmethod
    def parentetizar(cls, s):
        """Coloca parênteses em uma expressão, se necessário."""
        def balanceada(s):
            """Verifica se uma string tem parênteses balanceados."""
            contagem = 0
            for c in s:
                if c == "(":
                    contagem += 1
                elif c == ")":
                    if contagem <= 0:
                        return False
                    contagem -= 1
            return contagem == 0
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanceada(s[1:-1])
        ):
            return s
        else:
            return f"({s})"


class Simbolo(Sentenca):

    def __init__(self, nome):
        self.nome = nome

    def __eq__(self, outro):
        return isinstance(outro, Simbolo) and self.nome == outro.nome

    def __hash__(self):
        return hash(("simbolo", self.nome))

    def __repr__(self):
        return self.nome

    def avaliar(self, modelo):
        try:
            return bool(modelo[self.nome])
        except KeyError:
            raise Exception(f"variável {self.nome} não está no modelo")

    def formula(self):
        return self.nome

    def simbolos(self):
        return {self.nome}


class Nao(Sentenca):
    def __init__(self, operando):
        Sentenca.validar(operando)
        self.operando = operando

    def __eq__(self, outro):
        return isinstance(outro, Nao) and self.operando == outro.operando

    def __hash__(self):
        return hash(("nao", hash(self.operando)))

    def __repr__(self):
        return f"Nao({self.operando})"

    def avaliar(self, modelo):
        return not self.operando.avaliar(modelo)

    def formula(self):
        return "¬" + Sentenca.parentetizar(self.operando.formula())

    def simbolos(self):
        return self.operando.simbolos()


class E(Sentenca):
    def __init__(self, *conjuntos):
        for c in conjuntos:
            Sentenca.validar(c)
        self.conjuntos = list(conjuntos)

    def __eq__(self, outro):
        return isinstance(outro, E) and self.conjuntos == outro.conjuntos

    def __hash__(self):
        return hash(("e", tuple(hash(c) for c in self.conjuntos)))

    def __repr__(self):
        return f"E({', '.join(str(c) for c in self.conjuntos)})"

    def adicionar(self, conjuncao):
        Sentenca.validar(conjuncao)
        self.conjuntos.append(conjuncao)

    def avaliar(self, modelo):
        return all(c.avaliar(modelo) for c in self.conjuntos)

    def formula(self):
        if len(self.conjuntos) == 1:
            return self.conjuntos[0].formula()
        return " ∧ ".join([Sentenca.parentetizar(c.formula()) for c in self.conjuntos])

    def simbolos(self):
        return set.union(*[c.simbolos() for c in self.conjuntos])


class Ou(Sentenca):
    def __init__(self, *disjuntos):
        for d in disjuntos:
            Sentenca.validar(d)
        self.disjuntos = list(disjuntos)

    def __eq__(self, outro):
        return isinstance(outro, Ou) and self.disjuntos == outro.disjuntos

    def __hash__(self):
        return hash(("ou", tuple(hash(d) for d in self.disjuntos)))

    def __repr__(self):
        return f"Ou({', '.join(str(d) for d in self.disjuntos)})"

    def avaliar(self, modelo):
        return any(d.avaliar(modelo) for d in self.disjuntos)

    def formula(self):
        if len(self.disjuntos) == 1:
            return self.disjuntos[0].formula()
        return " ∨ ".join([Sentenca.parentetizar(d.formula()) for d in self.disjuntos])

    def simbolos(self):
        return set.union(*[d.simbolos() for d in self.disjuntos])


class Implicacao(Sentenca):
    def __init__(self, antecedente, consequente):
        Sentenca.validar(antecedente)
        Sentenca.validar(consequente)
        self.antecedente = antecedente
        self.consequente = consequente

    def __eq__(self, outro):
        return (isinstance(outro, Implicacao)
                and self.antecedente == outro.antecedente
                and self.consequente == outro.consequente)

    def __hash__(self):
        return hash(("implica", hash(self.antecedente), hash(self.consequente)))

    def __repr__(self):
        return f"Implicacao({self.antecedente}, {self.consequente})"

    def avaliar(self, modelo):
        return (not self.antecedente.avaliar(modelo)
                or self.consequente.avaliar(modelo))

    def formula(self):
        antecedente = Sentenca.parentetizar(self.antecedente.formula())
        consequente = Sentenca.parentetizar(self.consequente.formula())
        return f"{antecedente} => {consequente}"

    def simbolos(self):
        return set.union(self.antecedente.simbolos(), self.consequente.simbolos())


class Bicondicional(Sentenca):
    def __init__(self, esquerda, direita):
        Sentenca.validar(esquerda)
        Sentenca.validar(direita)
        self.esquerda = esquerda
        self.direita = direita

    def __eq__(self, outro):
        return (isinstance(outro, Bicondicional)
                and self.esquerda == outro.esquerda
                and self.direita == outro.direita)

    def __hash__(self):
        return hash(("bicondicional", hash(self.esquerda), hash(self.direita)))

    def __repr__(self):
        return f"Bicondicional({self.esquerda}, {self.direita})"

    def avaliar(self, modelo):
        return ((self.esquerda.avaliar(modelo) and self.direita.avaliar(modelo)) or
                (not self.esquerda.avaliar(modelo) and not self.direita.avaliar(modelo)))

    def formula(self):
        esquerda = Sentenca.parentetizar(str(self.esquerda))
        direita = Sentenca.parentetizar(str(self.direita))
        return f"{esquerda} <=> {direita}"

    def simbolos(self):
        return set.union(self.esquerda.simbolos(), self.direita.simbolos())


def verificar_modelo(base_conhecimento, consulta):
    """Verifica se a base de conhecimento implica a consulta."""

    def verificar_todos(base, consulta, simbolos, modelo):
        """Verifica se a base implica a consulta, dado um modelo específico."""
        if not simbolos:
            if base.avaliar(modelo):
                return consulta.avaliar(modelo)
            return True
        else:
            restantes = simbolos.copy()
            p = restantes.pop()

            modelo_verdadeiro = modelo.copy()
            modelo_verdadeiro[p] = True

            modelo_falso = modelo.copy()
            modelo_falso[p] = False

            return (verificar_todos(base, consulta, restantes, modelo_verdadeiro) and
                    verificar_todos(base, consulta, restantes, modelo_falso))

    simbolos = set.union(base_conhecimento.simbolos(), consulta.simbolos())
    return verificar_todos(base_conhecimento, consulta, simbolos, dict())
