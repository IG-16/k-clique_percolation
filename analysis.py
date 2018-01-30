#!/usr/bin/python

import networkx as nx
import csv as csv

print "-------START------"
Ipfile = raw_input("enter input file: ")
#G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")
G=nx.karate_club_graph()
Opfile ="ANALYSIS.txt"
f = open(Opfile,"w")
writer = csv.writer(f, delimiter = '\t')
my_analysis = []
clus = dict(nx.clustering(G)) #clustering coefficient
length1 = dict(nx.all_pairs_shortest_path_length(G)) #shortest_path
deg = dict(nx.betweenness_centrality(G))
f.write("Node\tClustering_Coefficient\tShortest_Path_Length\tShortest_Path\tBetweeness_Centrality\n")
for i in length1:
        key, value = max(length1[i].iteritems(), key=lambda x:x[1])
        writer.writerow((i,clus[i],value,nx.shortest_path(G,i,key),deg[i]))
        my_analysis.append({i : [clus[i],value,nx.shortest_path(G,i,key),deg[i]]})    
#print my_analysis
print "-------STOP------"
