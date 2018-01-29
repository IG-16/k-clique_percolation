#!/usr/bin/python

import networkx as nx

print "-------START------"
Ipfile = raw_input("enter input file: ")
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")
Opfile ="ANALYSIS.txt"
f = open(Opfile,"w")
my_analysis = []
clus = dict(nx.clustering(G)) #clustering coefficient
length1 = dict(nx.all_pairs_shortest_path_length(G)) #shortest_path
deg = dict(nx.betweenness_centrality(G))
f.write("Node\t\tClustering_Coefficient\t\tShortest_Path_Length\t\t\t\tShortest_Path\t\t\t\t\t\t\t\t\t\tDegree_Centrality\n")
for i in length1:
        key, value = max(length1[i].iteritems(), key=lambda x:x[1])
        f.write('%s\t\t\t\t\t\t%s\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t%d\t\t\t\t\t\t\t\t%s\t\t\t\t\t\t\t\t\t\t\t%s\n' % (i,clus[i],value,nx.shortest_path(G,i,key),deg[i]))
        my_analysis.append({i : [clus[i],value,nx.shortest_path(G,i,key),deg[i]]})
print my_analysis
print "-------STOP------"
