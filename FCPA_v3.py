#!/usr/bin/python

from collections import defaultdict
import networkx as nx


def get_adjacent_cliques(clique,membership_dict):
    adjacent_cliques = set()
    for n in clique:
        for adj_clique in membership_dict[n]:
            if clique != adj_clique:
                adjacent_cliques.add(adj_clique)
    return adjacent_cliques


def get_fast_percolated_cliques(G,k): 
    print  "\n\n Starting Clique Finding for size "+str(k) 
    cliques = [frozenset(c) for c in nx.find_cliques(G) if len(c) >= k]

    print  "Cliques found."
    nodesToCliquesDict = defaultdict(list)
    for clique in cliques:
        for node in clique:
            nodesToCliquesDict[node].append(clique)

    print  "NodesToCliques Map built. "
    cliquesToComponents = dict()
    currentComponent = 0
    
    cliquesProcessed = 0
    for clique in cliques:
        cliquesProcessed += 1
        if cliquesProcessed % 1000 == 0:
            print "Total cliques processed: ", str(cliquesProcessed) 
            
        if not clique in cliquesToComponents:
            currentComponent += 1
            cliquesToComponents[clique] = currentComponent
            frontier = set()
            frontier.add(clique)
            componentCliquesProcessed = 0

            while len(frontier) > 0:
                currentClique = frontier.pop()
                componentCliquesProcessed+=1
                if componentCliquesProcessed % 1000 == 0:
                    print  "Component cliques processed: ", str(componentCliquesProcessed)
                    print  "Size of frontier: ", len(frontier)
                    

                for neighbour in get_adjacent_cliques(currentClique, nodesToCliquesDict):
                    if len(currentClique.intersection(neighbour)) >= (k-1):
                        cliquesToComponents[neighbour] = currentComponent
                        frontier.add(neighbour)
                        for node in neighbour:
                            nodesToCliquesDict[node].remove(neighbour)

    print "CliqueGraphComponent Built"
    componentToNodes = defaultdict(set)
    for clique in cliquesToComponents:
        componentCliqueIn = cliquesToComponents[clique]
        componentToNodes[componentCliqueIn].update(clique)

    print "Node Components Assigned. "
    return componentToNodes.values()

print "---------------START---------------"

Ipfile = raw_input("enter input file: ")
print "Loading Graph."
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")
print "Graph Loaded. "

for k in range(5,11):
    handle,extension = Ipfile.split(".")
    Opfile= handle+"_com"+str(k)+"."+extension
    f = open(Opfile, 'w')

    for c in get_fast_percolated_cliques(G, k):
        f.write(" ".join([str(x) for x in c]))
        f.write("\n")
    f.close()
print "----------------END----------------"