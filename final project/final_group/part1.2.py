class Node:
    def __init__(self, vertex, cost):
        self.vertex = vertex
        self.cost = cost

    # Operator overloading for min heap
    def __lt__(self, other):
        return self.cost < other.cost
    

class Graph:
    def __init__(self):
        self.adjacency = {}

    def addEdge(self, source, destination, weight):
        if source not in self.adjacency:
            self.adjacency[source] = []

        if destination not in self.adjacency:
            self.adjacency[destination] = []

        self.adjacency[source].append(Node(destination, weight))
        self.adjacency[destination].append(Node(source, weight))
        
    

    def bellmanFord(self, startVertex, vertexList, k):
        distanceFromSource = {vertex: float('inf') for vertex in vertexList}
        distanceFromSource[startVertex] = 0
        result = {}

        for _ in range(k):
            for vertex in vertexList:
                for neighbourNode in self.adjacency[vertex]:
                    neighbour = neighbourNode.vertex
                    neighbourDistance = neighbourNode.cost

                    if distanceFromSource[vertex] + neighbourDistance < distanceFromSource[neighbour]:
                        distanceFromSource[neighbour] = distanceFromSource[vertex] + neighbourDistance
                        result[neighbour] = (result.get(vertex, ([], float('inf')))[0] + [neighbour], distanceFromSource[neighbour])

        for vertex in vertexList:
            path = result.get(vertex, ([], float('inf')))[0]
            result[vertex] = (path, distanceFromSource[vertex])

        return result


#Testing
vertexList = ["A", "B", "C", "D", "E"]

graph = Graph()
graph.addEdge("A", "B", 7)
graph.addEdge("A", "E", 1)
graph.addEdge("B", "C", 3)
graph.addEdge("B", "E", 8)
graph.addEdge("C", "D", 6)
graph.addEdge("C", "E", 2)
graph.addEdge("D", "E", 7)

startVertex = input("Please enter the start vertex: ")
k = int(input("Input k - the number of relaxation limits: "))

if k >= len(vertexList) - 1:
    k = len(vertexList) - 2

resultBellmanFord = graph.bellmanFord(startVertex, vertexList, k)

print("\n\nsource is: ", startVertex, ". showing distance from source")
print("Vertex\tDistance\tPath")
for vertex in vertexList:
    path, distance = resultBellmanFord.get(vertex, ([], 0))
    print(f"{vertex}\t{distance}\t\t{' '.join(map(str, path)) if path else '-'}")
