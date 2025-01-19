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

    def dijkstra(self, startVertex, vertexList, k):
        relaxations = {vertex: 0 for vertex in vertexList}
        distanceFromSource = {vertex: float('inf') for vertex in vertexList}
        result = {}
        weightedList = []

        weightedList.append(Node(startVertex, 0))
        distanceFromSource[startVertex] = 0

        while weightedList:
            # Find the minimum cost vertex
            minNode = min(weightedList, key=lambda x: x.cost)
            weightedList.remove(minNode)
            curVertex = minNode.vertex
            cost = minNode.cost

            for neighbourNode in self.adjacency[curVertex]:
                neighbour = neighbourNode.vertex
                neighbourDistance = neighbourNode.cost

                if relaxations[neighbour] >= k:
                    continue

                # path relaxation
                if distanceFromSource[curVertex] + neighbourDistance < distanceFromSource[neighbour]:
                    distanceFromSource[neighbour] = distanceFromSource[curVertex] + neighbourDistance
                    weightedList.append(Node(neighbour, distanceFromSource[neighbour]))

                    relaxations[neighbour] += 1

                    # path
                    newPath = result.get(curVertex, ([], None))[0][:]
                    newPath.append(neighbour)
                    result[neighbour] = (newPath, distanceFromSource[neighbour])

        for vertex in vertexList:
            if vertex != startVertex and vertex not in result:
                result[vertex] = ([], -1)

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

result = graph.dijkstra(startVertex, vertexList, k)

print("source is: ", startVertex, ". showing distance from source")
print("Vertex\tDistance\tPath")
for vertex in vertexList:
    path, distance = result.get(vertex, ([], 0))
    print(f"{vertex}\t{distance}\t\t{' '.join(map(str, path)) if path else '-'}")
