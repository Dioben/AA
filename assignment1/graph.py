import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import argparse
import json

def generateGraph(vertices=5,edgelimit=15,seed=93391):
    if vertices>81:
        raise ValueError("9x9 Grid cannot fit this many vertices")
    if edgelimit<vertices-1:
        raise ValueError("Not enough edges to connect all nodes")
    if edgelimit>vertices*(vertices-1)/2:
        raise ValueError("This generator does not allow for repeated vertices")


    random.seed(seed) 
    graph= nx.Graph()

    #create nodes and assign positions
    positions = [(x,y) for x in range(1,9) for y in range(1,9)]
    random.shuffle(positions)
    assignments = {}

    edges = {}
    covered = set()

    for x in range(1,vertices+1):
        try:
            position = positions.pop(0)
        except:
            raise ValueError("Generation has run out of valid positions, too many nodes for grid or bad seed")
        positions = removeAdjacent(positions,position)
        assignments[x]={"pos":position}

    graph.add_nodes_from(assignments)
    nx.set_node_attributes(graph,assignments)

    #ensure connectivity, as far as I can tell will always spawn N-1 edges
    components = list(nx.connected_components(graph))
    while len(components)!=1:
        edge = (random.choice(sorted(components[0])),random.choice(sorted(components[1]))) #sorting for consistent generation
        graph.add_edge(edge[0],edge[1])
        edges[edge]= {"weight":eucdist(assignments[edge[0]]['pos'],assignments[edge[1]]['pos']),"color":"black"}
        components = list(nx.connected_components(graph))
    
    if len(edges)<edgelimit:
        possedges = {(x,y) for x in graph.nodes for y in graph.nodes if x<y}
        possedges=possedges.difference(edges.keys())
        possedges=sorted(possedges)
        for _ in range(edgelimit-len(edges)):
            index = random.randint(0,len(possedges)-1)
            edge = possedges.pop(index)
            graph.add_edge(edge[0],edge[1])
            edges[edge]= {"weight":eucdist(assignments[edge[0]]['pos'],assignments[edge[1]]['pos']),"color":"black"}
    #complement if necessary
    nx.set_edge_attributes(graph,edges)
    return graph
    


def eucdist(p1,p2):
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def removeAdjacent(array,position):
    vectors = [(1,0),(0,1),(1,1),(-1,1)]
    for x in vectors:
        if (position[0]+x[0],position[1]+x[1]) in array:
            array.remove((position[0]+x[0],position[1]+x[1]))
        if (position[0]-x[0],position[1]-x[1]) in array:
            array.remove((position[0]-x[0],position[1]-x[1]))
    return array


def generateDrawings(graph):
    pos=nx.get_node_attributes(graph,'pos')
    weights = {x:round(y,2) for x,y in nx.get_edge_attributes(graph,"weight").items()}
    weightlist = [.5*weights[x] for x in graph.edges()]#halved because I think it'll look better
    colors = [graph.edges[x]['color'] for x in graph.edges()]
    subax1 = plt.subplot(121)
    subax1.set_xlim(1,9)
    subax1.set_ylim(1,9)
    subax1.set_xticks(range(1,10))
    subax1.set_yticks(range(1,10))
    subax1.grid(which="both")
    subax1.set_axisbelow(True)

    nx.draw_networkx(graph,pos,width=weightlist, with_labels=True,font_weight='bold')
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=weights,font_size=7)
    
    subax2 = plt.subplot(122)
    subax2.set_xlim(1,9)
    subax2.set_ylim(1,9)
    subax2.set_xticks(range(1,10))
    subax2.set_yticks(range(1,10))
    subax2.grid(which="both")
    subax2.set_axisbelow(True)

    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_labels(graph,pos,font_weight="bold")
    nx.draw_networkx_edges(graph,pos,width=weightlist,edge_color=colors)
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=weights,font_size=7)
    plt.show()

if __name__ =="__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--seed",help="Graph generation seed",type=int,default=93391)
    parser.add_argument("--nodes",help="node count",type=int, default=5)
    parser.add_argument("--edges",help="edge count",type=int, default=10)
    parser.add_argument("--output",help="output file",default="graph.json")
    args = parser.parse_args()
    graph = generateGraph(args.nodes,args.edges,args.seed)

    graph_export = nx.readwrite.node_link_data(graph)
    
    f = open(args.output,"w")
    f.write(json.dumps(graph_export))
    f.close()

