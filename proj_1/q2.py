import numpy as np
from numpy import random
import random
import pandas as pd
from math import sqrt
import networkx as nx
import heapq

from collections import deque

G_inicial = nx.Graph()

# inicializando manualmente as cidades (vérticies) e
# os respectivos custos entre elas (arestas).

G_inicial.add_weighted_edges_from([
        ("Arad", "Sibiu", 140),
        ("Arad", "Timisoara", 118),
        ("Arad", "Zerind", 75),
        ("Bucharest", "Fagaras", 211),
        ("Bucharest", "Giurgiu", 90),
        ("Bucharest", "Pitesti", 101),
        ("Bucharest", "Urziceni", 85),
        ("Craiova", "Dobreta", 120),
        ("Craiova", "Pitesti", 138),
        ("Craiova", "Rimnicu_Vilcea", 146),
        ("Dobreta", "Mehadia", 75),
        ("Eforie", "Hirsova", 86),
        ("Fagaras", "Sibiu", 99),
        ("Hirsova", "Urziceni", 98),
        ("Iasi", "Neamt", 87),
        ("Iasi", "Vaslui", 92),
        ("Lugoj", "Mehadia", 70),
        ("Lugoj", "Timisoara", 111),
        ("Oradea", "Zerind", 71),
        ("Oradea", "Sibiu", 151),
        ("Pitesti", "Rimnicu_Vilcea", 97),
        ("Rimnicu_Vilcea", "Sibiu", 80),
        ("Urziceni", "Vaslui", 142)
    ])

    # Plotando para conferir
nx.draw(G_inicial, with_labels=True)

# Caso as cidades possuam as coordenadas de latitude e longitude
# a heurística poderá ser calculada através da distância euclidiana.
# Porém, para simplificar o exercício, é fornecida uma tabela
# (um dicionário)  com os valores das estimativas de distâncias.


# Estimativa das distâncias de todas as cidades com destino 
# para Bucharest

Estimation = {
        "Arad": 366,
        "Bucharest": 0,
        "Craiova": 160,
        "Dobreta": 242,
        "Eforie": 161,
        "Fagaras": 178,
        "Giurgiu": 77,
        "Hirsova": 151,
        "Iasi": 226,
        "Lugoj": 244,
        "Mehadia": 241,
        "Neamt": 234,
        "Oradea": 380,
        "Pitesti": 98,
        "Rimnicu_Vilcea": 193,
        "Sibiu": 253,
        "Timisoara": 329,
        "Urziceni": 80,
        "Vaslui": 199,
        "Zerind": 374
}

# Calcula custo total de um caminho
def calcula_custo_caminho(G, caminho):
    custo = 0.0
    for i in range(len(caminho)-1):
        u, v = caminho[i], caminho[i+1]
        custo += G[u][v]['weight']
    return custo

    # calcula custo do caminho da cidade origem até a cidade atual
def calcula_custo_g(G, caminho_origem_atual):
    return calcula_custo_caminho(G, caminho_origem_atual)

# No futuro, a funcao abaixo será substituída apropriadamente
# para os cálculos das estimativas euclidianas
def estima_custo_h(cidade_atual):
    # destino == 'Bucharest':
    return Estimation[cidade_atual]

# Exemplo
estima_custo_h('Zerind')

# Implementação do algoritmo BFS

def BFS(G_inicial, s):

    G = G_inicial.copy()

    # INICIALIZACAO
    for v in G.nodes() - {s}:
        G.nodes[v]['cor'] = 'branco'
        G.nodes[v]['dis'] = np.inf

    G.nodes[s]['cor'] = 'cinza'
    G.nodes[s]['dis'] = 0

    # Fila (append (right), popleft)
    Q = deque()
    Q.append(s)
    passos = 0

    while len(Q) != 0:
        u = Q.popleft()
        passos += 1

        for v in G.neighbors(u):
            if G.nodes[v]['cor'] == 'branco':
                G.nodes[v]['cor'] = 'cinza'
                G.nodes[v]['dis'] = G.nodes[u]['dis'] + 1
                G.nodes[v]['pre'] = u

                Q.append(v)

        G.nodes[u]['cor'] = 'preto'

        #print(u, G.nodes[u]['dis'], G.nodes[u]['cor'])

    # Grafo G retornado contem as informações de distância
    # e cores desde o nó origem a todos os demais nós
    
    return G, passos

#----------------------------------------------------------------

def caminho_minimo_BFS(G, s, t):

    L = [t]
    u = t
    while u != s:
        u = G.nodes[u]['pre']
        L.append(u)

    L.reverse()

    return L

################################
# ------------ UCS ------------#
################################

# Implemente aqui o algoritmo UCS (Custo Uniforme)
# f(n) = g(n)

def UCS(G_inicial, s, t):
    G = G_inicial.copy()

    # INICIALIZAÇÃO
    for v in G.nodes() - {s}:
        G.nodes[v]['cor'] = 'branco'
        G.nodes[v]['dis'] = np.inf

    G.nodes[s]['cor'] = 'cinza'
    G.nodes[s]['dis'] = 0

    # Fila de prioridade com base no custo g(n) de cada nó:
    Q = []
    heapq.heappush(Q, (0, s))
    passos = 0 # Var para calcular qtde de expansões.

    t_encontrado = False  # Verificar se target (t) com menor custo foi encontrado
    menor_custo_t = np.inf  # Menor custo conhecido para (t)

    while len(Q) != 0:
        custo, u = heapq.heappop(Q) # Pop da fila o nó com menor custo
        passos += 1
       # Interromper se encontrar target 
        if u == t:
            t_encontrado = True
            break                  
       # Interromper se g(n) encontrado for maior ou igual ao menor g(n) conhecido
        if custo >= menor_custo_t:
            break                  

        # Para cada nó vizinho de u: 
        for v in G.neighbors(u):
            # Se ainda não visitado: marcar como visitado; calcular g(n); marcar predecessor e adicionar na fila de prio. 
            if G.nodes[v]['cor'] == 'branco':
                G.nodes[v]['cor'] = 'cinza'
                G.nodes[v]['dis'] = G.nodes[u]['dis'] + G.edges[u, v]['weight']
                G.nodes[v]['pre'] = u
                heapq.heappush(Q, (G.nodes[v]['dis'], v))
            # Se já visitado: calcular g(n) pelo novo caminho, comparar com g(n) anterior e adicionar menor na fila de prio e na var de predecessores.
            elif G.nodes[v]['cor'] == 'cinza':
                custo_conhecido = G.nodes[v]['dis']
                novo_custo = G.nodes[u]['dis'] + G.edges[u, v]['weight']
                if novo_custo < custo_conhecido:
                    G.nodes[v]['dis'] = novo_custo
                    G.nodes[v]['pre'] = u
                    heapq.heappush(Q, (G.nodes[v]['dis'], v))

        G.nodes[u]['cor'] = 'preto'
        #print(u, G.nodes[u]['dis'], G.nodes[u]['cor'])
        

    return G, passos

#----------------------------------------------------------------

def caminho_minimo_UCS(G, s, t):
    L = [t]
    u = t
    while u != s:
        u = G.nodes[u]['pre']
        L.append(u)

    L.reverse()

    return L


################################
# ------------ A*  ------------#
################################

# Implemente aqui o algoritmo A-star
# f(n) = g(n) + h(n)

def ASTAR(G_inicial, s, t):
    G = G_inicial.copy()

    # INICIALIZAÇÃO
    for v in G.nodes() - {s}:
        G.nodes[v]['cor'] = 'branco'
        G.nodes[v]['dis'] = np.inf

    G.nodes[s]['cor'] = 'cinza'
    G.nodes[s]['dis'] = 0

    # Fila de prioridade com base no custo g(n) de cada nó:
    Q = []
    heapq.heappush(Q, (0, s))
    passos = 0 # Var para calcular qtde de expansões.

    t_encontrado = False  # Verificar se target (t) com menor custo foi encontrado
    menor_custo_t = np.inf  # Menor custo conhecido para (t)

    while len(Q) != 0:
        custo, u = heapq.heappop(Q) # Pop da fila o nó com menor custo
        passos += 1
       # Interromper se encontrar target 
        if u == t:
            t_encontrado = True
            break                  
       # Interromper se g(n) encontrado for maior ou igual ao menor g(n) conhecido
        if custo >= menor_custo_t:
            break                  

        # Para cada nó vizinho de u: 
        for v in G.neighbors(u):
            #heuristica = 
            # Se ainda não visitado: marcar como visitado; calcular g(n); marcar predecessor e adicionar na fila de prio. 
            if G.nodes[v]['cor'] == 'branco':
                G.nodes[v]['cor'] = 'cinza'
                G.nodes[v]['dis'] = G.nodes[u]['dis'] + G.edges[u, v]['weight'] + Estimation[v]
                G.nodes[v]['pre'] = u
                heapq.heappush(Q, (G.nodes[v]['dis'], v))
            # Se já visitado: calcular g(n) + f(n) pelo novo caminho, comparar com g(n) + f(n) anterior e adicionar menor na fila de prio e na var de predecessores.
            elif G.nodes[v]['cor'] == 'cinza':
                custo_conhecido = G.nodes[v]['dis']
                novo_custo = G.nodes[u]['dis'] + G.edges[u, v]['weight'] + Estimation[v]
                if novo_custo < custo_conhecido:
                    G.nodes[v]['dis'] = novo_custo
                    G.nodes[v]['pre'] = u
                elif novo_custo >= custo_conhecido:
                    G.nodes[v]['dis'] = novo_custo
                    G.nodes[v]['pre'] = u
                    heapq.heappush(Q, (G.nodes[v]['dis'], v))
                    
                
        G.nodes[u]['cor'] = 'preto'
        #print(u, G.nodes[u]['dis'], G.nodes[u]['cor'])

    return G, passos

#----------------------------------------------------------------

def caminho_minimo_ASTAR(G, s, t):
    L = [t]
    u = t
    while u != s:
        u = G.nodes[u]['pre']
        L.append(u)

    L.reverse()

    return L

origem = 'Arad'
destino = 'Bucharest'

#----------------------------------------------------------------

# BFS
G, passos = BFS(G_inicial, origem)
caminho = caminho_minimo_BFS(G, origem, destino)

custo = calcula_custo_caminho(G, caminho)

print(f'Custo: {custo}\t->\tCaminho mais raso: {caminho}')
print(f'Nós expandidos: {passos}')

# Chame aqui apropriadamente os algoritmos para resolver o problema

# UCS
G, passos = UCS(G_inicial, origem, destino)
caminho = caminho_minimo_UCS(G, origem, destino)

custo = calcula_custo_caminho(G, caminho)

print(f'Custo: {custo}\t->\tCaminho mais barato: {caminho}')
print(f'Nós expandidos: {passos}')

# A-star
G, passos = ASTAR(G_inicial, origem, destino)
caminho = caminho_minimo_ASTAR(G, origem, destino)

custo = calcula_custo_caminho(G, caminho)

print(f'Custo: {custo}\t->\tCaminho mais barato c/ heurística: {caminho}')
print(f'Nós expandidos: {passos}')
