import random

class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d

#Assumes G represents its nodes as integers 0,1,...,(n-1)
def unknown(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

#TEST CASES 

#TEST CASE 1 WITH NEGATIVE EDGE WEIGHTS AND WITHOUT A CYCLE.  

graph1 = DirectedWeightedGraph()
nodes = [0, 1, 2, 3]
for node in nodes:
    graph1.add_node(node)


graph1.add_edge(0, 1, 2)
graph1.add_edge(1, 2, -3)
graph1.add_edge(2, 3, 1)
graph1.add_edge(3, 0, -1)
graph1.add_edge(0, 2, 4)  
graph1.add_edge(1, 3, 5)
graph1.add_edge(2, 0, -2)  
graph1.add_edge(3, 1, -1)


print("Graph 1 Adjacency List:")
print(graph1.adj)
print("Graph 1 Weights:")
print(graph1.weights)


shortest_paths1 = unknown(graph1)
print("Shortest paths matrix for Graph 1 (No Negative Cycle and No Inf):")
for row in shortest_paths1:
    print(row)

#TEST CASE 2 WITH NEGATIVE EDGE WEIGHTS AND WITH A NEGATIVE CYCLE.
    

graph2 = DirectedWeightedGraph()
nodes = [0, 1, 2, 3]
for node in nodes:
    graph2.add_node(node)


graph2.add_edge(0, 1, 6)
graph2.add_edge(1, 2, 3)
graph2.add_edge(2, 0, -10)  # Negative cycle here
graph2.add_edge(2, 3, 2)
graph2.add_edge(3, 1, 1)


shortest_paths2 = unknown(graph2)


print("Graph 2 Adjacency List:")
print(graph2.adj)
print("Graph 2 Weights:")
print(graph2.weights)
print("Shortest paths matrix for Graph 2 (With Negative Cycle):")
for row in shortest_paths2:
    print(row)


