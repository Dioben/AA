import argparse
import json
import networkx as nx
from graph import generateDrawings
import itertools
import math
import time

def greedy(graph):
    seen = 0
    sortededges = sorted(graph.edges(),key=lambda x:graph.edges[x]['weight'])
    sortededges_as_tuples = [(x,) for x in sortededges]
    states = sortededges_as_tuples[:]
    done = False
    while not done: #will always choose shortest length solution, could also choose best one if I used bisection.insort
        solution = states.pop(0)
        most_costly_edge = solution[-1]
        seen+=1
        states+=[solution + x for x in sortededges_as_tuples[sortededges.index(most_costly_edge)+1:]] #there is no point adding cheaper edges as that state has already been added
        captured_nodes = set()
        for edge in solution:#compute nodes we have attached to
            captured_nodes.add(edge[0])
            captured_nodes.add(edge[1])

        missing_edges = set(graph.edges()).difference(solution) #edges we must be adjacent to
        for edge in list(missing_edges):
            if edge[0] in captured_nodes or edge[1] in captured_nodes: #check for adjacency
                missing_edges.remove(edge)
            if not missing_edges:
                done = True
    for edge in solution:#just for graphic purposes
        graph.edges[edge]['color']="red"
    return graph,solution,seen,seen+len(states)

def exhaustive(graph):
    seen = 0
    adds = 0
    best_cost = math.inf
    best_solution = None
    for x in range(1,len(graph.edges())+1):#all length possibilities
        for item in  itertools.combinations(graph.edges(),x):#all possible arrangements
            seen+=1
            total_weight = 0
            captured_nodes = set()

            for edge in item:
                captured_nodes.add(edge[0])
                captured_nodes.add(edge[1])
                adds+=1
                total_weight+=graph.edges[edge]['weight']
            
            if total_weight<best_cost:#is it actually worth checking whether this is a valid solution?
                missing_edges = set(graph.edges()).difference(item)
                for edge in list(missing_edges):
                    if edge[0] in captured_nodes or edge[1] in captured_nodes:
                        missing_edges.remove(edge)

                if not missing_edges:
                    best_cost = total_weight
                    best_solution = item

    for edge in best_solution:#just for graphic purposes
        graph.edges[edge]['color']="red"
    return graph,best_solution,seen,adds


if __name__ =="__main__":
    parser= argparse.ArgumentParser()
    
    parser.add_argument("--input",help="input file",default="graph.json")
    parser.add_argument('--graph', dest='graph', action='store_true')
    parser.add_argument('--no-graph', dest='graph', action='store_false')
    parser.set_defaults(graph=True)
    parser.add_argument('--greedy', dest='strat', action='store_true')
    parser.add_argument('--exhaustive', dest='strat', action='store_false')
    parser.set_defaults(strat=True)

    args = parser.parse_args()

    f = open(args.input,"r")
    graphmap = json.loads(f.read())
    f.close()
    graph = nx.readwrite.node_link_graph(graphmap)

    if args.strat:
        timedelta = time.time()
        graph,solution,seen,adds = greedy(graph)
        timedelta = time.time() - timedelta
    else:
        timedelta = time.time()
        graph,solution,seen,adds = exhaustive(graph)
        timedelta = time.time() - timedelta
    print(seen,adds,timedelta)
    if args.graph:
        generateDrawings(graph)
    