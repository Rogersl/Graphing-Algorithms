#Logan Rogers

#Created and tested in Python 2.7.6

import random

#--------------------------------------------------------------
# Make "random" graph of user input size,
# one with all positive weights, and one with some negative
#--------------------------------------------------------------
edge_prob = 40          	# % probability for an edge (u,v) to be created
max_base_weight = 15    	#random weight x, set weight from 0-x
weight_variance = 3     	#weight variance y, sets weights = 0-x + 0-y
negative_max_weight = -3	#lowest possible weight
inf = 999999				#value to mark distance as infinity
inf_check = 9999			#value to check against for unconnected paths

n = input('Enter number of graph vertices n: ')

positive_graph = [[inf for x in range(n)] for y in range(n)]
negative_graph = [[inf for x in range(n)] for y in range(n)]

for x in range(n):
	for y in range(n):
		if x == y:
			positive_graph[x][y] = 0
			negative_graph[x][y] = 0
		elif random.randint(0,100) <= edge_prob:
			positive_weight = random.randint(1,max_base_weight) + random.randint(0,weight_variance)
			negative_weight = random.randint(negative_max_weight,max_base_weight) + random.randint(-weight_variance, weight_variance)
			positive_graph[x][y] = positive_weight
			negative_graph[x][y] = negative_weight


#--------------------------------------------------------------
# Floyd-Warshall Code
#--------------------------------------------------------------
def floydWarshall(graph):
	#create distance matrix
	dist = [[0 for x in range(n)] for y in range(n)]

	#create parent matrix
	parent = [[inf for x in range(n)] for y in range(n)]

	#initialize dist and parent matrices
	for i in range(n):
		for j in range(n):
			dist[i][j] = graph[i][j]
			if i == j:
				parent[i][j] = inf
			if graph[i][j] != inf:
				parent[i][j] = i
			else:
				parent[i][j] = inf

	for k in range(n):
		for i in range(n):
			for j in range(n):
				if dist[i][k] + dist[k][j] < dist[i][j]:
					dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
					parent[i][j] = parent[k][j]

	for i in range(n):
		if dist[i][i] < 0:
			print '\nGraph contains a negative cycle'
			break

	printSolution(dist)

#--------------------------------------------------------------
# Transitive Closure Code
#--------------------------------------------------------------
def transitiveClosure(graph):
	#make transitive_closure matrix
	transitive_closure = [[0 for x in range(n)] for y in range(n)]
	has_path = 1
	no_path = 0

	for i in range(n):
		for j in range(n):
			if i == j:
				transitive_closure[i][j] = has_path
			if graph[i][j] != inf:
				transitive_closure[i][j] = has_path
			else:
				transitive_closure[i][j] = no_path

	for k in range(n):
		for i in range(n):
			for j in range(n):
				transitive_closure[i][j] = transitive_closure[i][j] or (transitive_closure[i][k] and transitive_closure[k][j])

	printSolution(transitive_closure)


# A utility function to print the solution
def printSolution(matrix):
	print '\nPrinting matrix: '
	for i in range(n):
		for j in range(n):
			if(matrix[i][j] > inf_check):
				print "%s\t" %("INF"),
			else:
				print "%d\t" %(matrix[i][j]),
			if j == n-1:
				print ""
	print '\n'

#--------------------------------------------------------------
# Execute functions, output results
#--------------------------------------------------------------
print 'Positive Graph: '
printSolution(positive_graph)
print 'Negative Graph: '
printSolution(negative_graph)

print '\nRunning Floyd-Warshall on graph with all positive weights.  Distance Matrix: '
floydWarshall(positive_graph)

print '\nRunning Floyd-Warshall on graph with (potentially) some negative weights.  Distance Matrix: '
floydWarshall(negative_graph)

print '\nRunning Transitive Closure on graph with all positive weights: '
transitiveClosure(positive_graph)

print '\nRunning Transitive Closure on graph with some (potentially) negative weights: '
transitiveClosure(negative_graph)

print '\nThe time complexity of both the Floyd-Warshall program and the' \
	' Transitive Closure program are O(|V|^3)'