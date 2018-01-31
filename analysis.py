#!/usr/bin/python

from __future__ import division
import networkx as nx
import csv as csv
from itertools import combinations
from collections import Counter
from networkx.utils import not_implemented_for


@not_implemented_for('multigraph')
def _triangles_and_degree_iter(G, nodes=None):

    if nodes is None:
        nodes_nbrs = G.adj.items()
    else:
        nodes_nbrs = ((n, G[n]) for n in G.nbunch_iter(nodes))

    for v, v_nbrs in nodes_nbrs:
        vs = set(v_nbrs) - {v}
        gen_degree = Counter(len(vs & (set(G[w]) - {w})) for w in vs)
        ntriangles = sum(k * val for k, val in gen_degree.items())
        yield (v, len(vs), ntriangles, gen_degree)


@not_implemented_for('multigraph')
def _weighted_triangles_and_degree_iter(G, nodes=None, weight='weight'):
    if weight is None or G.number_of_edges() == 0:
        max_weight = 1
    else:
        max_weight = max(d.get(weight, 1) for u, v, d in G.edges(data=True))
    if nodes is None:
        nodes_nbrs = G.adj.items()
    else:
        nodes_nbrs = ((n, G[n]) for n in G.nbunch_iter(nodes))

    def wt(u, v):
        return G[u][v].get(weight, 1) / max_weight

    for i, nbrs in nodes_nbrs:
        inbrs = set(nbrs) - {i}
        weighted_triangles = 0
        seen = set()
        for j in inbrs:
            seen.add(j)
            jnbrs = set(G[j]) - seen
            wij = wt(i, j)
            weighted_triangles += sum((wij * wt(j, k) * wt(k, i)) ** (1 / 3)
                                      for k in inbrs & jnbrs)
        yield (i, len(inbrs), 2 * weighted_triangles)


@not_implemented_for('directed')
def clustering(G, nodes=None, weight=None):
    
    if weight is not None:
        td_iter = _weighted_triangles_and_degree_iter(G, nodes, weight)
        clusterc = {v: 0 if t == 0 else t / (d * (d - 1)) for
                    v, d, t in td_iter}
    else:
        td_iter = _triangles_and_degree_iter(G, nodes)
        clusterc = {v: 0 if t == 0 else t / (d * (d - 1)) for
                    v, d, t, _ in td_iter}
    if nodes in G:
        return clusterc[nodes]
    return clusterc

def _single_shortest_path_length(adj, firstlevel, cutoff):
    seen = {}                  
    level = 0                  
    nextlevel = firstlevel     

    while nextlevel and cutoff >= level:
        thislevel = nextlevel  
        nextlevel = {}         
        for v in thislevel:
            if v not in seen:
                seen[v] = level  
                nextlevel.update(adj[v])  
                yield (v, level)
        level += 1
    del seen

def single_source_shortest_path_length(G, source, cutoff=None):
    if source not in G:
        raise nx.NodeNotFound('Source {} is not in G'.format(source))
    if cutoff is None:
        cutoff = float('inf')
    nextlevel = {source: 1}
    return dict(_single_shortest_path_length(G.adj, nextlevel, cutoff))


def all_pairs_shortest_path_length(G, cutoff=None):
    length = single_source_shortest_path_length
    # TODO This can be trivially parallelized.
    for n in G:
        yield (n, length(G, n, cutoff=cutoff))


def single_source_shortest_path(G, source, cutoff=None):

    if source not in G:
        raise nx.NodeNotFound("Source {} not in G".format(source))

    def join(p1, p2):
        return p1 + p2
    if cutoff is None:
        cutoff = float('inf')
    nextlevel = {source: 1}     
    paths = {source: [source]}  
    return dict(_single_shortest_path(G.adj, nextlevel, paths, cutoff, join))



def _single_shortest_path(adj, firstlevel, paths, cutoff, join):

    level = 0   
    nextlevel = firstlevel
    while nextlevel and cutoff > level:
        thislevel = nextlevel
        nextlevel = {}
        for v in thislevel:
            for w in adj[v]:
                if w not in paths:
                    paths[w] = join(paths[v], [w])
                    nextlevel[w] = 1
        level += 1
    return paths

def shortest_path(G, source=None, target=None, weight=None):
    if source is None:
        if target is None:
            if weight is None:
                paths = dict(nx.all_pairs_shortest_path(G))
            else:
                paths = dict(nx.all_pairs_dijkstra_path(G, weight=weight))
        else:

            with nx.utils.reversed(G):
                if weight is None:
                    paths = single_source_shortest_path(G, target)
                else:
                    paths = nx.single_source_dijkstra_path(G, target,
                                                           weight=weight)
                for target in paths:
                    paths[target] = list(reversed(paths[target]))

    else:
        if target is None:
            if weight is None:
                paths = single_source_shortest_path(G, source)
            else:
                paths = nx.single_source_dijkstra_path(G, source,
                                                       weight=weight)
        else:
            if weight is None:
                paths = nx.bidirectional_shortest_path(G, source, target)
            else:
                paths = nx.dijkstra_path(G, source, target, weight)

    return paths



print "-------START------"
Ipfile = raw_input("enter input file: ")
G = nx.read_edgelist(Ipfile, nodetype=str, delimiter="\t")

Opfile ="ANALYSIS.txt"
f = open(Opfile,"w")
writer = csv.writer(f, delimiter = '\t')
my_analysis = []
clus = dict(clustering(G))
length1 = dict(all_pairs_shortest_path_length(G))
deg = dict(nx.betweenness_centrality(G))
f.write("Node\tClustering_Coefficient\tShortest_Path_Length\tShortest_Path\tBetweeness_Centrality\n")
for i in length1:
        key, value = max(length1[i].iteritems(), key=lambda x:x[1])
        writer.writerow((i,clus[i],value,shortest_path(G,i,key),deg[i]))
        my_analysis.append({i : [clus[i],value,shortest_path(G,i,key),deg[i]]})
        
print my_analysis
print "-------STOP------"
