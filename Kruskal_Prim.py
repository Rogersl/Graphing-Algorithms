#Logan Rogers

#Created and tested on Python 2.7.6

import random
import time
from operator import itemgetter
from collections import defaultdict
from heapq import *

#--------------------------------------------------------------
# Make "random" graph of user input size
#--------------------------------------------------------------
edge_prob = 50          # % probability for an edge (u,v) to be created
max_base_weight = 20    #random weight x, set weight from 0-x
weight_variance = 5     #weight variance y, sets weights = 0-x + 0-y

n = input('Enter number of graph vertices n: ')
nodes = []
edges = []
for i in range(n):
    nodes.append(i)

#Create random edges using edge_prob.  Check for x < y so that we can copy 
#to other half (x > y), becuase this is an undirected graph.
for x in range(n):
    for y in range(n):
        if x < y and random.randint(01,10) <= edge_prob:
            w = random.randint(1,max_base_weight) + random.randint(1,weight_variance)
            edges.append((x, y, w))
            edges.append((y, x, w))

#--------------------------------------------------------------
#Prim Code
#--------------------------------------------------------------
def prim(nodes, edges):
    connected_edges = defaultdict(list)
    for edge in edges:
        node1, node2, weight = edge
        connected_edges[node1].append((weight, node1, node2))
        connected_edges[node2].append((weight, node1, node2))
 
    mst = []
    used = set([nodes[0]])
    potential_edges = connected_edges[nodes[0]][:]
    heapify(potential_edges)
 
    while potential_edges:
        weight, node1, node2 = heappop(potential_edges)
        if node2 not in used:
            used.add(node2)
            mst.append((node1, node2, weight))
 
            for edge in connected_edges[node2]:
                if edge[2] not in used:
                    heappush(potential_edges, edge)
    return mst

#--------------------------------------------------------------
#Kruskal Code
#--------------------------------------------------------------
#Define set operations
class DisjointSet(dict):
    #add item to tree
    def add(self, item):
        self[item] = item
 
    #find tree which item belongs to
    def find(self, item):
        parent = self[item]
 
        while self[parent] != parent:
            parent = self[parent]
 
        self[item] = parent
        return parent
    
    #join 2 trees
    def union(self, item1, item2):
        self[item2] = self[item1]
 
def kruskal(nodes, edges):
    forest = DisjointSet()
    mst = []
    for node in nodes:
        forest.add(node)
 
    forest_tree_count = len(nodes) - 1
 
    for edge in sorted(edges, key=itemgetter(2)):
        node1, node2, _ = edge
        tree1 = forest.find(node1)
        tree2 = forest.find(node2)
        if tree1 != tree2:
            mst.append(edge)
            forest_tree_count -= 1
            if forest_tree_count == 0:
                return mst
         
            forest.union(tree1, tree2)

#--------------------------------------------------------------
# Execute functions, calculate runtime, output results
#--------------------------------------------------------------

kruskal_start = time.clock()
kruskal_mst = kruskal(nodes, edges)
kruskal_end = time.clock()

prim_start = time.clock()
prim_mst = prim(nodes, edges)
prim_end = time.clock()

print 'Nodes: '
for node in nodes:
    print node

print 'Edges: '
for edge in edges:
    print edge

print '\nKruskal MST contains: '
for edge in kruskal_mst:
    print 'Edge(u, v, weight): ' + str(edge)

print '\nPrim MST contains: '
for edge in prim_mst:
    print 'Edge(u, v, weight): ' + str(edge)

print 'Kruskal Execution Time ' + str(kruskal_end - kruskal_start) + 's'
print 'Prim Execution Time ' + str(prim_end - prim_start) + 's'