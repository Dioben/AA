import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import argparse
import json

def generateGraph(vertices=5,edges=15,seed=93391):   
    if vertices>81:
        raise ValueError("9x9 Grid cannot fit this many vertices")
    if edges<vertices-1:
        raise ValueError("Not enough edges to connect all nodes")
    random.seed(seed) 
    graph= nx.generators.random_graphs.dense_gnm_random_graph(vertices,edges,seed)
    positions = [(x,y) for x in range(1,9) for y in range(1,9)]
    random.shuffle(positions)
    assignments = {}
    for x in graph.nodes():
        try:
            position = positions.pop(0)
        except:
            raise ValueError("Generation has run out of valid positions, too many nodes for grid or bad seed")
        positions = removeAdjacent(positions,position)
        assignments[x]={"pos":position}
    nx.set_node_attributes(graph,assignments)

    weights = {} 
    for edge in graph.edges():
        weights[edge] = {"weight":eucdist(graph.nodes[edge[0]]['pos'],graph.nodes[edge[1]]['pos']), "color":"black"}
    nx.set_edge_attributes(graph,weights)
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


