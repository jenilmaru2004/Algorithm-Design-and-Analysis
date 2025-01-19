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

    V = len(graph)
    all_distances = []
    all_predecessors = []
    for start_vertex in range(V):
        distances, predecessor = dijkstra(graph, start_vertex)
        all_distances.append(distances)
        all_predecessors.append(predecessor)
    return all_distances, all_predecessors


def bellman_ford(graph, start_vertex):

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

# MAIN TAKEAWAY:

# The code defines a minimum heap structure and utilizes it within Dijkstra's algorithm to efficiently find the 
# shortest paths from a single source to all other nodes in a graph with non-negative weights, repeating this process 
# for each vertex to solve the all-pairs shortest path problem. For graphs that might have negative weights, it 
# employs the Bellman-Ford algorithm to achieve the same goal, carefully checking for negative-weight cycles which 
# would invalidate the shortest path calculations. Both algorithms return a matrix of shortest distances and a matrix 
# of predecessors for path reconstruction.

# The complexity of the all-pairs shortest path algorithms for dense graphs can be derived from the complexities 
# of the single-source shortest path algorithms, Dijkstra's and Bellman-Ford, since they are effectively 
# being run from each vertex in the graph.

# For Dijkstra's algorithm, using a binary min-heap, the complexity is ( O(E + Vlog V) ) for each run from a single source. 
# In a dense graph, where ( E ) is close to ( V^2 ), this complexity becomes ( O(V^2 + Vlog V) ), which simplifies 
# to ( O(V^2) ) for each run from a single source.

# Since you need to run Dijkstra's algorithm from each of the ( V ) vertices for the all-pairs shortest path problem, 
# the overall complexity for Dijkstra's algorithm in a dense graph becomes ( O(V times V^2) ), which simplifies to ( O(V^3) ).

# For the Bellman-Ford algorithm, the complexity is ( O(VE) ) for each run from a single source. In a dense graph, 
# where ( E ) is close to ( V^2 ), this complexity is ( O(V times V^2) ), which is ( O(V^3) ) for each run from a single source.

# Since you need to run the Bellman-Ford algorithm from each of the ( V ) vertices for the all-pairs shortest path problem, 
# the overall complexity for Bellman-Ford in a dense graph becomes ( O(V times V^3) ), which simplifies to ( O(V^4) ).

# Therefore, for dense graphs, the complexity of the provided algorithms would be:

# - For all-pairs shortest path using Dijkstra's algorithm: ( O(V^3) ).
# - For all-pairs shortest path using Bellman-Ford algorithm: ( O(V^4) ).

# This conclusion holds if we assume that the graph is dense and the priority queue operations in Dijkstra's algorithm scale
#  with ( O(V^2) ) due to the high number of edges, which is typical for dense graphs.