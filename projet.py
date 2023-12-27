path = "graphs/JoliGraphe50/JoliGraphe50.graphe"
colors = ["red","blue","green","black","white"]

def initGraph(file):
    graph = {}
    with open(file,'r') as graphFile:
        nbVertices = int(graphFile.readline())
        for i in range(nbVertices):
            ligne = [x.strip() for x in graphFile.readline().split(':')]
            num = int(ligne[0])
            voisins = [int(x) for x in ligne[1].strip('[').strip(']').split(',')]
            graph[num] = voisins
        graphFile.close()
    return graph

def brique1(graph):
    for i in range(len(graph)):
        if (len(graph[i]) <= 5):
            return i
    return -1

def brique4(graph,x,coloration):
    possibility = colors.copy()
    if (len(graph[x]) <= 4):
        for neighbor in graph[x]:
            if neighbor in coloration:
                possibility.remove(coloration[neighbor])
        if len(possibility) > 0:
            return possibility[0]
    return ""

def brique5(graph,x,coloration):
    possibility = colors.copy()
    if len(graph[x]) == 5:
        graphMinusX = graph.copy()
        del graphMinusX[x]
        for neighbor in graph[x]:
            if neighbor in coloration and coloration[neighbor] in possibility:
                possibility.remove(coloration[neighbor])
        if len(possibility) > 0:
            return possibility[0]
    return ""

graph = initGraph(path)
print(graph)
print(brique1(graph))
print(brique4(graph,1,{}))
print(brique5(graph,2,{}))