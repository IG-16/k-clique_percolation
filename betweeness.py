#!/usr/bin/python

import networkx as nx
import operator


print "-------START------"
def num_spaths(G):
    n_spaths = dict.fromkeys(G, 0.0)
    spaths = dict(nx.all_pairs_shortest_path(G))

    for source in G:
        for path in spaths[source].values():
            for node in path[1:]:
                n_spaths[node] += 1
    print str(n_spaths)
    return n_spaths

#G= nx.karate_club_graph()
Ipfile = raw_input("enter input file: ")
print "Loading Graph."
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")

Opfile ="betweeness_new.txt"
f = open(Opfile,"w")
#clus = dict(nx.betweenness_centrality(G,normalized=True))
clus= dict(num_spaths(G))
for key, value in clus.iteritems():
    f.write('%s\t%s\n' % (key,value))
f.close()

print "-------STOP------"