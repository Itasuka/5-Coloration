from enum import Enum
path = "graphs/JoliGraphe50/JoliGraphe50.graphe"
colors = ["red","blue","green","black","white"]

class Color(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    BLACK = "black"
    WHITE = "white"
    NO_COLOR = None

class Vertex:
    def __init__(self,color,voisins,x=0,y=0):
        self.color = color
        self.voisins = voisins
        self.x = 0
        self.y = 0


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
    return -1

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
                possibility.remove(graph[neighbor])
        if len(possibility) > 0:
            return possibility[0]
    return Color.NO_COLOR

def brique6(graph,x):
    possibility = [color for color in enumerate(Color) if color != Color.NO_COLOR]
    for neighbor in graph[x].voisins:
        if graph[neighbor].color in possibility:
            possibility.remove(graph[neighbor].color)
    if len(possibility) == 0:
        return
    return

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
    
graph = initGraph(path)
print(brique1(graph))
brique3(graph,0,Color.RED,Color.BLUE)
print(brique4_5(graph,1))