import random
import heapq
import time

from collections import deque
from viewer import MazeViewer
from math import inf, sqrt




def gera_labirinto(n_linhas, n_colunas, inicio, goal):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que 50% do labirinto esteja ocupado
    numero_de_obstaculos = int(0.50 * n_linhas * n_colunas)
    for _ in range(numero_de_obstaculos):
        linha = random.randint(0, n_linhas-1)
        coluna = random.randint(0, n_colunas-1)
        labirinto[linha][coluna] = 1

    # remove eventuais obstaculos adicionados na posicao
    # inicial e no goal
    labirinto[inicio.y][inicio.x] = 0
    labirinto[goal.y][goal.x] = 0

    return labirinto


class Celula:
    def __init__(self, y, x, anterior):
        self.y = y
        self.x = x
        self.anterior = anterior

    def __lt__(self, other):
        # Comparação baseada nas coordenadas (x, y)
        if self.y < other.y:
            return True
        elif self.y == other.y:
            return self.x < other.x
        else:
            return False

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __hash__(self):
        return hash((self.y, self.x))


def distancia(celula_1, celula_2):
    dx = celula_1.x - celula_2.x
    dy = celula_1.y - celula_2.y
    return sqrt(dx ** 2 + dy ** 2)


def esta_contido(lista, celula):
    for elemento in lista:
        if (elemento.y == celula.y) and (elemento.x == celula.x):
            return True
    return False


def custo_caminho(caminho):
    if len(caminho) == 0:
        return inf

    custo_total = 0
    for i in range(1, len(caminho)):
        custo_total += distancia(caminho[i].anterior, caminho[i])

    return custo_total


def obtem_caminho(goal):
    caminho = []

    celula_atual = goal
    while celula_atual is not None:
        caminho.append(celula_atual)
        celula_atual = celula_atual.anterior

    # o caminho foi gerado do final para o
    # comeco, entao precisamos inverter.
    caminho.reverse()

    return caminho


def celulas_vizinhas_livres(celula_atual, labirinto):
    # generate neighbors of the current state
    vizinhos = [
        Celula(y=celula_atual.y-1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+1, anterior=celula_atual),
    ]

    # seleciona as celulas livres
    vizinhos_livres = []
    for v in vizinhos:
        # verifica se a celula esta dentro dos limites do labirinto
        if (v.y < 0) or (v.x < 0) or (v.y >= len(labirinto)) or (v.x >= len(labirinto[0])):
            continue
        # verifica se a celula esta livre de obstaculos.
        if labirinto[v.y][v.x] == 0:
            vizinhos_livres.append(v)

    return vizinhos_livres


######################################
#--------------- BFS ----------------#
######################################

def breadth_first_search(labirinto, inicio, goal, viewer):
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    tempo_inicial_BFS = time.time()

    
    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):
        
        # seleciona o no mais antigo para ser expandido
        no_atual = fronteira.popleft()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        #viewer.pause()

    tempo_BFS = time.time() - tempo_inicial_BFS

    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    

    return caminho, custo, expandidos, tempo_BFS


######################################
#--------------- DFS ----------------#
######################################

def depth_first_search(labirinto, inicio, goal, viewer):
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    tempo_inicial_DFS = time.time()

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):
        
        # seleciona o no mais antigo para ser expandido
        no_atual = fronteira.pop()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        #viewer.pause()

    tempo_DFS = time.time() - tempo_inicial_DFS

    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    


    return caminho, custo, expandidos, tempo_DFS


######################################
#--------------- UCS ----------------#
######################################


def uniform_cost_search(labirinto, inicio, goal, viewer):
    # nós gerados e que podem ser expandidos (vermelhos)
    fronteira = []
    # nós já expandidos (amarelos)
    expandidos = set()

    # adiciona o nó inicial na fronteira
    heapq.heappush(fronteira, (0, inicio))  # (custo, nó)

    # dicionário para armazenar o custo acumulado de cada nó
    custo_acumulado = {inicio: 0}

    # variável para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    tempo_inicial_UCS = time.time()

    # Repete enquanto não encontramos o goal e ainda
    # existem nós para serem expandidos na fronteira. Se
    # acabarem os nós da fronteira antes do goal ser encontrado,
    # então ele não é alcançável.
    while fronteira and goal_encontrado is None:

        # seleciona o nó de menor custo para ser expandido
        custo_atual, no_atual = heapq.heappop(fronteira)

        # verifica se o nó atual já foi expandido
        if no_atual not in expandidos:
            # adiciona o nó atual aos nós expandidos
            expandidos.add(no_atual)

            # busca os vizinhos do nó atual
            vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

            # para cada vizinho, verifica se é necessário atualizar o custo acumulado
            for v in vizinhos:
                custo_novo = custo_acumulado[no_atual] + 1  # Custo unitário entre nós adjacentes
                if v.y == goal.y and v.x == goal.x:
                    goal_encontrado = v
                    break
                    # encerra o loop interno
                else:
                    if v not in custo_acumulado or custo_novo < custo_acumulado[v]:
                        custo_acumulado[v] = custo_novo
                        heapq.heappush(fronteira, (custo_novo, v))

                
            #viewer.update(generated=[n for (_, n) in fronteira], expanded=expandidos)
            #viewer.pause()

    tempo_UCS = time.time() - tempo_inicial_UCS       

    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)
    

    return caminho, custo, expandidos, tempo_UCS


######################################
#--------------- A*  ----------------#
######################################

def heuristica(no_atual, goal):
    return distancia(no_atual, goal)


def a_estrela(labirinto, inicio, goal, viewer):
    fronteira = []  # nós gerados e que podem ser expandidos (vermelhos)
    expandidos = set()  # nós já expandidos (amarelos)

    heapq.heappush(fronteira, (heuristica(inicio, goal), inicio))  # (prioridade, nó)

    custo_acumulado = {inicio: 0}  # dicionário para armazenar o custo acumulado de cada nó
    goal_encontrado = None  # variável para armazenar o goal quando ele for encontrado.

    tempo_inicial_A = time.time()

    while fronteira and goal_encontrado is None:
        _, no_atual = heapq.heappop(fronteira)

        if no_atual not in expandidos:
            expandidos.add(no_atual)

            if no_atual == goal:
                goal_encontrado = no_atual
                break

            vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

            for v in vizinhos:
                if v not in expandidos:
                    custo_novo = custo_acumulado[no_atual] + 1
                    if v.y == goal.y and v.x == goal.x:
                        goal_encontrado = v
                        break
                    else:
                        if v not in custo_acumulado or custo_novo < custo_acumulado[v]:
                            custo_acumulado[v] = custo_novo
                            prioridade = custo_novo + heuristica(v, goal)
                            heapq.heappush(fronteira, (prioridade, v))

            #viewer.update(generated=[n for (_, n) in fronteira], expanded=expandidos)

    tempo_A = time.time() - tempo_inicial_A

    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)

    return caminho, custo, expandidos, tempo_A

#-------------------------------


def main():
    while True:
        SEED = 42  # coloque None no lugar do 42 para deixar aleatorio
        random.seed(SEED)
        N_LINHAS  = 30
        N_COLUNAS = 30
        INICIO = Celula(y=0, x=0, anterior=None)
        GOAL   = Celula(y=N_LINHAS-1, x=N_COLUNAS-1, anterior=None)


        """
        O labirinto sera representado por uma matriz (lista de listas)
        em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
        """
        labirinto = gera_labirinto(N_LINHAS, N_COLUNAS, INICIO, GOAL)

        viewer = (labirinto, INICIO, GOAL)

        #----------------------------------------
        # BFS Search
        #----------------------------------------
        #viewer._figname = "BFS"
        caminho, custo_total, expandidos, tempo_BFS = \
                breadth_first_search(labirinto, INICIO, GOAL, viewer)

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"BFS:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
            f"\tTempo de execução: {(tempo_BFS)}.\n"

        )

        #viewer.update(path=caminho)
        #viewer.pause()


        #----------------------------------------
        # DFS Search
        #----------------------------------------
        #viewer._figname = "DFS"
        caminho, custo_total, expandidos, tempo_DFS = \
                depth_first_search(labirinto, INICIO, GOAL, viewer)

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"DFS:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tTempo de execução: {(tempo_DFS)}.\n\n"

        )

        #viewer.update(path=caminho)
        #viewer.pause()

        #----------------------------------------
        # A-Star Search
        #----------------------------------------
        #viewer._figname = "A*"
        caminho, custo_total, expandidos, tempo_A = \
                a_estrela(labirinto, INICIO, GOAL, viewer)

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"A*:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
            f"\tTempo de execução: {(tempo_A)}.\n"

        )

        #viewer.update(path=caminho)
        #viewer.pause()        

        #----------------------------------------
        # Uniform Cost Search (Obs: opcional)
        #----------------------------------------
        #viewer._figname = "UCS"
        caminho, custo_total, expandidos, tempo_UCS = \
                uniform_cost_search(labirinto, INICIO, GOAL, viewer)

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"UCS:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
            f"\tTempo de execução: {(tempo_UCS)}.\n"

        )

        #viewer.update(path=caminho)
        #viewer.pause()


    print("OK! Pressione alguma tecla pra finalizar...")
    input()


if __name__ == "__main__":
    main()
