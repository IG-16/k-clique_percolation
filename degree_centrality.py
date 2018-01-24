#!/usr/bin/python

import networkx as nx

print "-------START------"
Ipfile = raw_input("enter input file: ")
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")
Opfile ="degree.txt"
f = open(Opfile,"w")
deg = dict(nx.degree_centrality(G))
for key, value in deg.iteritems():
    f.write('%s\t%s\n' % (key,value))
f.close()

print "-------STOP------"
