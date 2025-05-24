import sys

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent  
        self.action = action

class StackFrontier():
    def __init__(self, ):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Fronteira vazia")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Fronteira vazia")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node 

class Maze():
    def __init__(self, filename):
        # Lê o arquivo e define a altura e a largura do labirinto
        with open(filename) as f:
            contents = f.read()
        
        # Verifica se há exatamente um ponto de início
        if contents.count("A") != 1:
            raise Exception("O labirinto deve ter exatamente um ponto de início")

        # Verifica se há exatamente um ponto de chegada
        if contents.count("B") != 1:
            raise Exception("O labirinto deve ter exatamente um ponto de chegada")

        # Determina a altura e a largura do labirinto
        contents = contents.splitlines()
        self.height = len(contents)
        self.widht = len(contents[0])  # <-- Corrigir: estava faltando no código original

        # Armazena onde há paredes
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.widht):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)    
                except IndexError:
                    # Se o índice estiver fora do intervalo, adiciona False à linha
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")  # Parede
                elif (i, j) == self.start:
                    print("A", end="")  # Início
                elif (i, j) == self.goal:
                    print("B", end="")  # Fim
                elif solution is not None and (i, j) in solution:
                    print("*", end="")  # Caminho da solução
                else:
                    print(" ", end="")  # Espaço livre
            print()
        print()

    def neighbors(self, state):
        row, col = state
        # Todas as ações possíveis
        candidates = [
            ("cima", (row - 1, col)),
            ("baixo", (row + 1, col)),
            ("esquerda", (row, col - 1)),
            ("direita", (row, col + 1))
        ]
        # Garante que as ações são válidas
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def solve(self):
        """Encontra uma solução para o labirinto, se existir."""
        # Conta o número de estados explorados
        self.num_explored = 0

        # Inicializa a fronteira com apenas a posição inicial
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Inicializa o conjunto de estados explorados como vazio
        self.explored = set()

        # Continua o loop até encontrar a solução
        while True:
            # Se não há mais elementos na fronteira, não há solução
            if frontier.empty():
                raise Exception("Sem solução")

            # Escolhe um nó da fronteira
            node = frontier.remove()
            self.num_explored += 1

            # Se o nó é o objetivo, então encontramos a solução
            if node.state == self.goal:
                actions = []
                cells = []
                # Segue os pais dos nós para obter o caminho
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Marca o nó como explorado
            self.explored.add(node.state)

            # Adiciona vizinhos à fronteira
            for action, state in self.neighbors(node.state):
                # Se o estado ainda não foi explorado e não está na fronteira
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    m = Maze(sys.argv[1])
    print("\nLabirinto lido:\n")
    m.print()
    print("\nResolvendo labirinto...\n")
    m.solve()
    print("\nSolução encontrada:\n")
    m.print()

