#!/usr/bin/python
import networkx as nx

Ipfile = raw_input("enter input file: ")
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")


f=open("clustering.txt","w")
f.write(str(nx.clustering(G)))
f.close()
