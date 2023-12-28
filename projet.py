#!/usr/bin/env python3
import time
import matplotlib.pyplot as plt
from enum import Enum
chemin = "graphs/JoliGraphe50/JoliGraphe50"
iteratif = False
affichage = False
verbose = False

class Color(Enum):
    """
    Classe permettant de définir nos 5 couleurs et le fait qu'un sommet ne possède pas de couleur
    """
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    WHITE = "white"
    BLACK = "black"
    NO_COLOR = "yellow"

class Vertex:
    """
    Classe représentant un sommet permettant de garder dans un seul et même endroit la couleur, les voisins et les coordonnées d'un sommet (les coordonnées peuvent ne pas exister)
    """
    def __init__(self,color,voisins,coord=None):
        self.color = color
        self.voisins = voisins
        self.coord = None

class Point:
    """
    Classe définissant un point avec ses 2 coordonnées x et y
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y

def initGraph(file):
    """
    Effectue la lecture du fichier .graphe et créer le graphe sous forme de dictionnaire avec comme clé le numéro du sommet et la valeur un objet de classe Vertex\n
    file = le chemin du fichier . graphe à lire
    """
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
    """
    Récupère un sommet de degré <= 5 s'il existe, renvoie None sinon\n
    graph = Le graphe pour lequel on récupère le sommet
    """
    for v in graph:
        if (len(graph[v].voisins) <= 5):
            return v
    return None

def brique3(graph,v,colA,colB):
    """
    Echange les couleur colA et colB de la composante connexe ou se trouve le sommet v dans le graphe graph\n
    graph = le graphe dans lequel on effectue le traitement\n
    v = le numéro du sommet appartenant à la composante connexe à traiter\n
    colA, colB = les 2 couleurs qui vont être échangées
    """
    colorV = graph[v].color
    if colorV == colA or colorV == colB:
        #On récupère le graphe contenant uniquement les sommets de couleurs colA et colB
        graphBicol = graphBicolor(graph,colA,colB)
        #On parcours le graphe bicolore à partir du sommet v pour obtenir sa composante connexe
        compConnexe = BFS(graphBicol,v)
        #On échange les couleurs
        for v in compConnexe:
            if compConnexe[v].color == colA:
                compConnexe[v].color = colB
            elif compConnexe[v].color == colB:
                compConnexe[v].color = colA

def brique4_5(graph,v):
    """
    Renvoie une couleur non utilisée par les voisins de v dans graph (si elle existe)\n
    graph = le graphe dans lequel on effectue le traitement\n
    v = le sommet dont on cherche une couleur disponible
    """
    possibility = [color for color in enumerate(Color) if color != Color.NO_COLOR]
    if (len(graph[v].voisins) <= 5):
        #Pour chaque voisins on retire la possibilité de couleur correspondant à la couleur du voisin
        for neighbor in graph[v].voisins:
            if graph[neighbor].color in possibility:
                possibility.remove(graph[neighbor].color)
        #S'il y a une possibilité, on retourne la première
        if len(possibility) > 0:
            return possibility[0]
    return Color.NO_COLOR

def brique6(graph,v):
    """
    Effectue le traitement de la brique 6 sur graph pour le sommet v\n
    graph = le graphe dans lequel on effectue le traitement\n
    v = le sommet dont on cherche la couleur
    """
    possibility = [color for color in enumerate(Color) if color != Color.NO_COLOR]
    for neighbor in graph[v].voisins:
        if graph[neighbor].color in possibility:
            possibility.remove(graph[neighbor].color)
    #Si les voisins utilisent toutes les couleurs disponible
    if len(possibility) == 0:
        #On créer un graphe sans v
        graphMinusX = graph.copy()
        graphMinusX = removeVertex(graphMinusX,v)
        compsConnexe = {}
        #On récupère toutes les composantes connexes des voisins de x
        for neighbor in graph[v].voisins:
            compsConnexe[neighbor] = BFS(graphMinusX,neighbor)
        for u in compsConnexe:
            compConnexe = compsConnexe[u]
            #Pour chaque voisins de x
            for neighbor in graph[v].voisins:
                #S'il on trouve 2 sommets qui ne sont pas dans la même composante connexe
                if not compConnexe[neighbor]:
                    colA = graph[u].color
                    colB = neighbor[u].color
                    #On inverse, dans la composante connexe, les couleux correspondant au 2 sommets
                    brique3(compConnexe,u,colA,colB)
                    return colA
    return Color.NO_COLOR

def coloring_rec(graph):
    """
    Effectue l'algorithme de coloration récursif sur graph\n
    graph = le graphe à colorier
    """
    #Si le graphe n'est pas vide
    if len(graph.keys()) > 0:
        x = brique1(graph)
        graphMinusX = graph.copy()
        graphMinusX = removeVertex(graphMinusX,x)
        #On fait un appel récursif sur G-x
        coloring_rec(graphMinusX)
        #On applique la brique 4 et 5
        b4_5 = brique4_5(graph,x)
        if b4_5 == None:
            #Si la brique4 et 5 ne renvoie pas de couleur on applique la brique 6
            b6 = brique6(graph,x)
            graph[x].color = b6
        else:
            graph[x].color = b4_5

def brique7(graph):
    """
    Trie les sommets par nombre de voisins croissant afin que la brique 7 soit respectée
    """
    sorted_list = sorted(graph, key=lambda x: len(graph[x].voisins))
    return sorted_list

def coloring_it(graph):
    """
    Effectue l'algorithme de coloration itératif sur graph\n
    graph = le graphe à colorier
    """
    list_order = brique7(graph)
    #Pour i de (n-1 à 0)
    for i in range(len(graph)-1, -1, -1):
        v = list_order[i]
        #On récupère les voisins de v qui ont un indice j supérieur à i dans liste_order
        neighbor = list(filter(lambda x: x in graph[v].voisins, list_order[i:]))
        graphDegenere = graph.copy()
        #On retire les sommets qui ne font pas parti des n-i derniers éléments
        for j in range(i):
            graphDegenere = removeVertex(graphDegenere,list_order[j])
        graphDegenere[v].voisins = neighbor
        #On applique la brique 4 et 5
        b4_5 = brique4_5(graphDegenere,v)
        if b4_5 == Color.NO_COLOR:
            #Si la brique 4 et 5 ne renvoie pas de couleur on applique la brique 6
            b6 = brique6(graphDegenere,v)
            graph[v].color = b6
        else:
            graph[v].color = b4_5

def checkColoring(graph):
    """
    Vérifie si un graphe est bien colorié\n
    graph = le graphe à vérifier
    """
    for v in graph:
        for neighbor in graph[v].voisins:
            #Chaque sommet doit avoir une couleur différente de ses voisins et une couleur différente de Color.NO_COLOR
            if graph[v].color == graph[neighbor].color or graph[v].color[1] == Color.NO_COLOR:
                return False
    return True

def BFS(graph,v):
    """
    Effectue l'algorithme du Breadth-First Search (parcours en largeur)\n
    graph = le graphe à parcourir\n
    v = le point de départ du parcours
    """
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
    """
    Récupère le sous-graphe de graph contenant uniquement les sommet de couleur colA ou colB\n
    graph = le graphe d'origine\n
    colA, colB = les couleurs pour lesquels on va garder les sommets
    """
    res = {}
    for v in graph.keys():
        if graph[v].color == colA or graph[v].color == colB:
            res[v] = graph[v]
    return res

def removeVertex(graph,v):
    """
    Retire un sommet de graph ainsi que toutes ses apparitions dans la liste des voisins d'un autre sommet\n
    graph = graphe dans lequel on retire le sommet\n
    v = le sommet à retirer
    """
    if v in graph:
        for neighbor in graph[v].voisins:
            if v in graph[neighbor].voisins:
                graph[neighbor].voisins.remove(v)
        del graph[v]
    return graph

def afficheGraphTerminal(graph):
    """
    Affiche la coloration de graph dans le terminal\n
    graph = le graphe dont la coloration doit être affichée
    """
    print(len(graph))
    for v in graph:
        print(v,": ",graph[v].color[1].value)

def sauvegarderColoration(graph):
    """
    Sauvegarde dans un fichier .colors la coloration de graph\n
    graph = le graph dont on veut sauvegarder la coloration
    """
    res = ""
    for v in graph:
        res += str(v) + ": " + str(graph[v].color[1].value) + "\n"
    with open(chemin + ".colors", 'w') as fichier:
        fichier.write(res)

def initCoord(graph,file):
    """
    Effectue la lecture du fichier .graphe et modifie graph pour définir l'attribut coord\n
    graph = le graph correspondant au fichier . coords\n
    file = le chemin du fichier . coords à lire
    """
    with open(file,'r') as graphFile:
        nbVertices = int(graphFile.readline())
        for i in range(nbVertices):
            ligne = [x.strip() for x in graphFile.readline().split(':')]
            num = int(ligne[0])
            coord = [int(x) for x in ligne[1].strip('(').strip(')').split(',')]
            x = coord[0]
            y = coord[1]
            graph[i].coord = Point(x,y)
        graphFile.close()
    return graph

def affichageGraphWindow(graph):
    """
    Dessine graph dans une fenêtre extérieur à l'aide de la librairie matplotlib. Les sommets non coloriés apparaissent de couleur Color.NO_COLOR\n
    graph = le graphe à dessiner
    """
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