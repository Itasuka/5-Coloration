#!/usr/bin/env python3
import time
import matplotlib.pyplot as plt
from enum import Enum
chemin = "graphs/JoliGraphe50/JoliGraphe50"
iteratif = False
affichage = False
verbose = False

class Color(Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    WHITE = "white"
    BLACK = "black"
    NO_COLOR = None

class Vertex:
    def __init__(self,color,voisins,coord=None):
        self.color = color
        self.voisins = voisins
        self.coord = None

class Coordonnee:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def initGraph(file):
    graph = {}
    with open(file,'r') as graphFile:
        nbVertices = int(graphFile.readline())
        for i in range(nbVertices):
            ligne = [x.strip() for x in graphFile.readline().split(':')]
            num = int(ligne[0])
            color = Color.NO_COLOR
            voisins = [int(x) for x in ligne[1].strip('[').strip(']').split(',')]
            vertex = Vertex(color,voisins)
            graph[num] = vertex
        graphFile.close()
    return graph

def brique1(graph):
    for v in graph:
        if (len(graph[v].voisins) <= 5):
            return v
    return None

def brique3(graph,v,colA,colB):
    colorV = graph[v].color
    if colorV == colA or colorV == colB:
        graphBicol = graphBicolor(graph,colA,colB)
        compConnexe = BFS(graphBicol,v)
        for v in compConnexe:
            if compConnexe[v].color == colA:
                compConnexe[v].color = colB
            elif compConnexe[v].color == colB:
                compConnexe[v].color = colA

def brique4_5(graph,v):
    possibility = [color for color in enumerate(Color) if color != Color.NO_COLOR]
    if (len(graph[v].voisins) <= 5):
        for neighbor in graph[v].voisins:
            if graph[neighbor].color in possibility:
                possibility.remove(graph[neighbor].color)
        if len(possibility) > 0:
            return possibility[0]
    return Color.NO_COLOR

def brique6(graph,x):
    possibility = [color for color in enumerate(Color) if color != Color.NO_COLOR]
    for neighbor in graph[x].voisins:
        if graph[neighbor].color in possibility:
            possibility.remove(graph[neighbor].color)
    if len(possibility) == 0:
        graphMinusX = graph.copy()
        del graphMinusX[x]
        compsConnexe = {}
        for neighbor in graph[x].voisins:
            compsConnexe[neighbor] = BFS(graphMinusX,neighbor)
        for u in compsConnexe:
            compConnexe = compsConnexe[u]
            for neighbor in graph[x].voisins:
                if not compConnexe[neighbor]:
                    colA = graph[u].color
                    colB = neighbor[u].color
                    brique3(compConnexe,u,colA,colB)
                    return colA
    return Color.NO_COLOR

def coloring_rec(graph):
    if len(graph.keys()) > 0:
        x = brique1(graph)
        graphMinusX = graph.copy()
        graphMinusX = removeVertex(graphMinusX,x)
        coloring_rec(graphMinusX)
        b4_5 = brique4_5(graph,x)
        if b4_5 == None:
            b6 = brique6(graph,x)
            graph[x].color = b6
        else:
            graph[x].color = b4_5

def brique7(graph):
    sorted_list = sorted(graph, key=lambda x: len(graph[x].voisins), reverse=False)
    return sorted_list

def coloring_it(graph):
    list_order = brique7(graph)
    for i in range(len(graph)-1, -1, -1):
        v = list_order[i]
        neighbor = list(filter(lambda x: x in graph[v].voisins, list_order[i:]))
        graphDegenere = graph.copy()
        for j in range(i):
            graphDegenere = removeVertex(graphDegenere,list_order[j])
        graphDegenere[v].voisins = neighbor
        b4_5 = brique4_5(graphDegenere,v)
        if b4_5 == Color.NO_COLOR:
            b6 = brique6(graphDegenere,v)
            graph[v].color = b6
        else:
            graph[v].color = b4_5

def checkColoring(graph):
    for v in graph:
        for neighbor in graph[v].voisins:
            if graph[v].color == graph[neighbor].color:
                return False
    return True

def BFS(graph,v):
    compConnexe = {}
    f = [v]
    while f:
        u = f.pop(0)
        for neighbor in graph[u].voisins:
            if neighbor not in compConnexe:
                f.append(neighbor)
                compConnexe[neighbor] = graph[neighbor]
    return compConnexe

def graphBicolor(graph,colA,colB):
    res = {}
    for v in graph.keys():
        if graph[v].color == colA or graph[v].color == colB:
            res[v] = graph[v]
    return res

def removeVertex(graph,v):
    if v in graph:
        for neighbor in graph[v].voisins:
            if v in graph[neighbor].voisins:
                graph[neighbor].voisins.remove(v)
        del graph[v]
    return graph

def afficheGraphTerminal(graph):
    print(len(graph))
    for v in graph:
        print(v,": ",graph[v].color[1].value)

def sauvegarderColoration(graph):
    res = ""
    for v in graph:
        res += str(v) + ": " + str(graph[v].color[1].value) + "\n"
    with open(chemin + ".colors", 'w') as fichier:
        fichier.write(res)

def initCoord(graph,file):
    with open(file,'r') as graphFile:
        nbVertices = int(graphFile.readline())
        for i in range(nbVertices):
            ligne = [x.strip() for x in graphFile.readline().split(':')]
            num = int(ligne[0])
            coord = [int(x) for x in ligne[1].strip('(').strip(')').split(',')]
            x = coord[0]
            y = coord[1]
            graph[i].coord = Coordonnee(x,y)
        graphFile.close()
    return graph

def affichageGraphWindow(graph):
    fig, ax = plt.subplots()
    for v in graph:
        x = graph[v].coord.x
        y = graph[v].coord.y
        color = graph[v].color[1].value
        circle = plt.Circle((x,y),0.5,facecolor=color,linestyle="-",edgecolor="black",zorder=1)
        ax.add_artist(circle)

        for neighbor in graph[v].voisins:
            xn = graph[neighbor].coord.x
            yn = graph[neighbor].coord.y
            ax.plot((x,xn),(y,yn),color='black',linestyle='-',linewidth=0.5,zorder=0)
    
    ax.set_aspect('equal',adjustable='datalim')
    ax.set_xlim(min(x.coord.x for x in graph.values())-2, max(x.coord.x for x in graph.values())+2)
    ax.set_ylim(min(y.coord.y for y in graph.values())-2, max(y.coord.y for y in graph.values())+2)

    plt.show()
    

def _parseArgs():
    """
    Parses arguments when this library is used as a main.

    :return: A list of args is returned
    """
    import argparse
    parser = argparse.ArgumentParser(prog='projet.py',
                                     description='Recherche la 5-coloration d\'un graphe planaire')
    parser.add_argument('-c', type=str, nargs=1, required=False,
                        help='C le chemin où trouver les fichiers .graphe et .coords (si disponible)')
    parser.add_argument('-i', action="store_true", 
                        help='Pour faire la 5-coloration en itératif (récursif de base)')
    parser.add_argument('-a', action="store_true", 
                        help='Pour afficher le graphe si le fichier .coords est disponible')
    parser.add_argument("-v", action="store_true", help="Affichage du résultat dans le terminal")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    import os.path
    args = _parseArgs()
    chemin = args.c[0] if args.c else "graphs/JoliGraphe50/JoliGraphe50"
    iteratif = args.i
    affichage = args.a
    verbose  = args.v
    start_time = 0
    if not os.path.exists(chemin + ".graphe"):
        print("Le chemin du fichier .graphe n'est pas valide")
        exit()
    if affichage and not os.path.exists(chemin + ".coords"): 
        print("Aucun fichier .coords trouvé, donc l'affichage sera désactivé")
        affichage = False
        
    #temps pour la coloration récursive
    if (not iteratif):
        graph = initGraph(chemin + ".graphe")
        start_time = time.time()
        coloring_rec(graph)
        print("Temps pour compiler en récursif: " + str(time.time()-start_time))
    
    #temps pour la coloration itérative
    if(iteratif):
        graph = initGraph(chemin + ".graphe")
        start_time = time.time()
        coloring_it(graph)
        print("Temps pour compiler en itératif: " + str(time.time()-start_time))

    #affichage du graph dans le terminal
    if verbose:
        afficheGraphTerminal(graph)

    sauvegarderColoration(graph)
    print("La coloration est " + ("bonne" if checkColoring(graph) else "mauvaise"))
    
    #affichage du graph sur matplotlib
    if(affichage):
        initCoord(graph,chemin + ".coords")
        affichageGraphWindow(graph)