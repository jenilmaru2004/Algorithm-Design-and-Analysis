# #attempt 1 (FAILED)

# def floyd_warshall(graph):
#     """
#     Floyd-Warshall algorithm to find the shortest path between all pairs of vertices.
#     This also tracks the second-to-last vertex on the shortest path.
#     The graph is represented as a dictionary of dictionaries, where the outer dictionary holds
#     vertices u and the inner dictionary holds vertices v with the edge weight as the value.
#     """

#     # Initialize distance and next_vertex matrices
#     vertices = list(graph.keys())
#     n = len(vertices)
#     distance = {u: {v: float('inf') for v in vertices} for u in vertices}
#     next_vertex = {u: {v: None for v in vertices} for u in vertices}

#     # Set the distance from each vertex to itself to 0
#     for v in vertices:
#         distance[v][v] = 0

#     # Fill in initial distances and next vertices
#     for u in graph:
#         for v in graph[u]:
#             distance[u][v] = graph[u][v]
#             next_vertex[u][v] = u

#     # Floyd-Warshall algorithm
#     for k in vertices:
#         for i in vertices:
#             for j in vertices:
#                 if distance[i][k] + distance[k][j] < distance[i][j]:
#                     distance[i][j] = distance[i][k] + distance[k][j]
#                     next_vertex[i][j] = next_vertex[k][j]

#     # Retrieve the second-to-last vertex on the shortest path
#     second_to_last = {u: {v: None for v in vertices} for u in vertices}
#     for i in vertices:
#         for j in vertices:
#             if i != j and next_vertex[i][j] is not None:
#                 second_to_last[i][j] = next_vertex[i][j]
#                 intermediate = next_vertex[i][j]
#                 while intermediate != i:
#                     if next_vertex[i][intermediate] == i:
#                         second_to_last[i][j] = intermediate
#                         break
#                     intermediate = next_vertex[i][intermediate]

#     return distance, second_to_last


#attempt 2

# import heapq

# def dijkstra(graph, start_vertex):
#     """
#     Dijkstra's algorithm for shortest paths in a graph with non-negative weights.
#     """
#     V = len(graph)
#     distances = [float('inf')] * V
#     predecessor = [-1] * V
#     distances[start_vertex] = 0
#     pq = [(0, start_vertex)]
    
#     while pq:
#         current_distance, current_vertex = heapq.heappop(pq)
#         if current_distance > distances[current_vertex]:
#             continue
#         for neighbor, weight in enumerate(graph[current_vertex]):
#             if weight is not None and current_distance + weight < distances[neighbor]:
#                 distances[neighbor] = current_distance + weight
#                 predecessor[neighbor] = current_vertex
#                 heapq.heappush(pq, (distances[neighbor], neighbor))
                
#     return distances, predecessor

# def all_pairs_shortest_path_dijkstra(graph):
#     """
#     Compute all pairs shortest paths for a graph using Dijkstra's algorithm.
#     Suitable for graphs with only non-negative weights.
#     """
#     V = len(graph)
#     all_distances = []
#     all_predecessors = []
#     for start_vertex in range(V):
#         distances, predecessor = dijkstra(graph, start_vertex)
#         all_distances.append(distances)
#         all_predecessors.append(predecessor)
#     return all_distances, all_predecessors

# # Now let's write the Bellman-Ford based algorithm for negative weights.

# def bellman_ford(graph, start_vertex):
#     """
#     Bellman-Ford algorithm for shortest paths in a graph with negative weights.
#     """
#     V = len(graph)
#     distances = [float('inf')] * V
#     predecessor = [-1] * V
#     distances[start_vertex] = 0
    
#     for _ in range(V - 1):
#         for u in range(V):
#             for v in range(V):
#                 if graph[u][v] is not None and distances[u] + graph[u][v] < distances[v]:
#                     distances[v] = distances[u] + graph[u][v]
#                     predecessor[v] = u
    
#     # Check for negative-weight cycles
#     for u in range(V):
#         for v in range(V):
#             if graph[u][v] is not None and distances[u] + graph[u][v] < distances[v]:
#                 print("Graph contains a negative-weight cycle")
#                 return None, None
                
#     return distances, predecessor

# def all_pairs_shortest_path_bellman_ford(graph):
#     """
#     Compute all pairs shortest paths for a graph using Bellman-Ford algorithm.
#     Suitable for graphs with negative weights but no negative cycles.
#     """
#     V = len(graph)
#     all_distances = []
#     all_predecessors = []
#     for start_vertex in range(V):
#         distances, predecessor = bellman_ford(graph, start_vertex)
#         if distances is None:  # Negative cycle detected
#             return None, None
#         all_distances.append(distances)
#         all_predecessors.append(predecessor)
#     return all_distances, all_predecessors

# We will not run these functions since we do not have a specific graph to test with, and the request was only for the implementation.

#attempt 3

class MinHeap:
    def __init__(self):
        self.heap = []

    def heappush(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def heappop(self):
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        self._sift_down(0)
        return item

    def _sift_up(self, index):
        parent_index = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent_index]:
            self._swap(index, parent_index)
            index = parent_index
            parent_index = (index - 1) // 2

    def _sift_down(self, index):
        child_index = 2 * index + 1
        while child_index < len(self.heap):
            right_child = 2 * index + 2
            if right_child < len(self.heap) and self.heap[right_child] < self.heap[child_index]:
                child_index = right_child

            if self.heap[index] <= self.heap[child_index]:
                break

            self._swap(index, child_index)
            index = child_index
            child_index = 2 * index + 1

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

def dijkstra(graph, start_vertex):
    V = len(graph)
    distances = [float('inf')] * V
    predecessor = [-1] * V
    distances[start_vertex] = 0
    pq = MinHeap()
    pq.heappush((0, start_vertex))

    while len(pq.heap) > 0:
        current_distance, current_vertex = pq.heappop()
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in enumerate(graph[current_vertex]):
            if weight is not None and current_distance + weight < distances[neighbor]:
                distances[neighbor] = current_distance + weight
                predecessor[neighbor] = current_vertex
                pq.heappush((distances[neighbor], neighbor))

    return distances, predecessor

def all_pairs_shortest_path_dijkstra(graph):
    """
    Compute all pairs shortest paths for a graph using Dijkstra's algorithm.
    Suitable for graphs with only non-negative weights.
    """
    V = len(graph)
    all_distances = []
    all_predecessors = []
    for start_vertex in range(V):
        distances, predecessor = dijkstra(graph, start_vertex)
        all_distances.append(distances)
        all_predecessors.append(predecessor)
    return all_distances, all_predecessors

# Now let's write the Bellman-Ford based algorithm for negative weights.

def bellman_ford(graph, start_vertex):
    """
    Bellman-Ford algorithm for shortest paths in a graph with negative weights.
    """
    V = len(graph)
    distances = [float('inf')] * V
    predecessor = [-1] * V
    distances[start_vertex] = 0
    
    for _ in range(V - 1):
        for u in range(V):
            for v in range(V):
                if graph[u][v] is not None and distances[u] + graph[u][v] < distances[v]:
                    distances[v] = distances[u] + graph[u][v]
                    predecessor[v] = u
    
    # Check for negative-weight cycles
    for u in range(V):
        for v in range(V):
            if graph[u][v] is not None and distances[u] + graph[u][v] < distances[v]:
                print("Graph contains a negative-weight cycle")
                return None, None
                
    return distances, predecessor

def all_pairs_shortest_path_bellman_ford(graph):
    """
    Compute all pairs shortest paths for a graph using Bellman-Ford algorithm.
    Suitable for graphs with negative weights but no negative cycles.
    """
    V = len(graph)
    all_distances = []
    all_predecessors = []
    for start_vertex in range(V):
        distances, predecessor = bellman_ford(graph, start_vertex)
        if distances is None:  # Negative cycle detected
            return None, None
        all_distances.append(distances)
        all_predecessors.append(predecessor)
    return all_distances, all_predecessors

# Graph for Dijkstra's algorithm (no negative weights)
graph_dijkstra = [
    [0, 2, 5, 1],
    [2, 0, 3, 2],
    [5, 3, 0, 3],
    [1, 2, 3, 0]
]

# Graph for Bellman-Ford algorithm (includes a negative weight)
graph_bellman_ford = [
    [0, -1, 4, None],
    [None, 0, 3, 2],
    [None, None, 0, None],
    [None, 1, 5, 0]
]

# Testing Dijkstra
distances_dijkstra, predecessors_dijkstra = all_pairs_shortest_path_dijkstra(graph_dijkstra)

# Testing Bellman-Ford
distances_bellman_ford, predecessors_bellman_ford = all_pairs_shortest_path_bellman_ford(graph_bellman_ford)

print("Dijkstra - Distances:")
for row in distances_dijkstra:
    print(row)

print("Dijkstra - Predecessors:")
for row in predecessors_dijkstra:
    print(row)

print("Bellman-Ford - Distances:")
for row in distances_bellman_ford:
    print(row)

print("Bellman-Ford - Predecessors:")
for row in predecessors_bellman_ford:
    print(row)
