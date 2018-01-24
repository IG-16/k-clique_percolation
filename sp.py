#!/usr/bin/python

import networkx as nx

Ipfile = raw_input("enter input file: ")
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")


f = open("shortest_path.txt", "w")

for i in G.nodes():
    length = dict(nx.single_source_shortest_path_length(G,i))
    for j in length:
        f.write(str('{} - {}:{}\n'.format(i,j,length[j])))

f.close()
