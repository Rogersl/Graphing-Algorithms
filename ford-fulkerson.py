'''
Logan Rogers
CS5200 HW 9 part 1
Ford-Fulkerson problem

Tested on python 2.7.6

Ran into an issue with random graph results:
    - may seemingly get stuck (Ford-Fulkerson convergence issue)

I am unsure of how to resolve the issue as I could find nothing on doing so.
Google could not save me.

There is a test case commented out to prove that Ford-Fulkerson algorithm
does run correctly on proper input.

Max flow = 0 if source disconnected from sink (randomness)

Please comment out 'operation_loop' calls (in main()) to see that the program can
work for given n (in case it gets stuck on the way).
'''

import random
import time

class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v  
        self.capacity = w

#container for edges, vertices, path, and maxflow functions for the
#flow network
class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}
 
    def add_vertex(self, vertex):
        self.adj[vertex] = []
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u, v, w=0):
        edge = Edge(u,v,w)
        redge = Edge(v,u,0)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    #Find path from source to sink, getting residual capacity as well
    def find_path(self, source, sink, path):
        if source == sink:
            return path
        for edge in self.get_edges(source):
            residual_capacity = edge.capacity - self.flow[edge]
            if residual_capacity > 0 and edge not in path:
                result = self.find_path(edge.sink, sink, path + [edge]) 
                if result != None:
                    return result
 
    #Compute max flow given FlowNetwork, source and sink
    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            residual_capacities = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residual_capacities)
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])
        return sum(self.flow[edge] for edge in self.get_edges(source))

'''
Graph generation function
Adds vertices based on number input for 'vertices'
Adds edges randomly based on 'probability'
Returns the random graph for use in driver function
'''
def generate_graph(vertices, probability):
    min_cap = 10     #min capacity
    max_cap = 50     #max capacity

    #add vertices to vertex list
    g = FlowNetwork()
    [g.add_vertex(v) for v in range(vertices+1)]

    #add random edges with random weights based on probability
    for i in range(vertices):
        for j in range(vertices):
            if random.randint(0,100) <= probability*100 and j < i:
                random_weight = random.randint(min_cap, max_cap)
                g.add_edge(i,j,random_weight)

    return g

'''
Main operation function
Runs the Ford-Fulkerson algorithm on 10 graphs of increasing density
for the given number of vertices.
Outputs max flow of each graph and execution time for each graph.
'''
def operation_loop(vertices):
    graph = FlowNetwork()

    #loop through edge probability 0.3 - 0.8
    for loop in range(11):
        probability = 0.3 + 0.05*loop          #edge creation probability
        graph = generate_graph(vertices, probability)   #get new graph
        source = random.randint(0, vertices)    #random starting point
        sink = random.randint(0, vertices)      #random end point

        #Ensure sink comes before source
        while(sink >= source):
            sink = random.randint(0, vertices)

        start = time.clock()                    #starting time
        flow = graph.max_flow(source, sink)
        print 'Max flow of random graph size = %s with probability %s: %s' %(vertices, probability, flow)
        end = time.clock()                      #end time
        exec_time = end - start                      #get elapsed run time
        print 'Execution time of graph size = %s with probability %s: %s' %(vertices, probability, exec_time)
        print '\n'

'''
Main driver function
We were asked to create 10 random graphs for each vertex count = 10,20,30,40,50
so we loop through 5 times, increasing vertex count in 10s.  We were also asked to
genereate each graph with different density, so we update the edge creation
probability by 0.05 10 times (starting at 0.40) each time we create a new graph.
Sink and source are also determined randomly for each graph.
This gives us 50 graphs satisfying the requirements.
'''
def main():
    graph = FlowNetwork()
    '''
    #Test case, result should be 5
    [g.add_vertex(v) for v in "sopqrt"]

    g.add_edge('s', 'o', 3)
    g.add_edge('s', 'p', 3)
    g.add_edge('o', 'p', 2)
    g.add_edge('o', 'q', 3)
    g.add_edge('p', 'r', 2)
    g.add_edge('r', 't', 3)
    g.add_edge('q', 'r', 4)
    g.add_edge('q', 't', 2)

    print(g.max_flow('s', 't'))
    ''' 
    
    #Each call runs 10 graphs of increasing density on n-vertex graphs
    #Formatted this way to allow commenting out should issues arise.
    operation_loop(10)
    operation_loop(20)
    operation_loop(30)
    operation_loop(40)
    operation_loop(50)
    
if __name__ == '__main__':
    main()
