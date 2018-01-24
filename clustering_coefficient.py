#!/usr/bin/python

import networkx as nx

print "-------START------"
Ipfile = raw_input("enter input file: ")
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")
Opfile ="clustering.txt"
f = open(Opfile,"w")
clus = dict(nx.clustering(G))
for key, value in clus.iteritems():
    f.write('%s\t%s\n' % (key,value))
f.close()

print "-------STOP------"
