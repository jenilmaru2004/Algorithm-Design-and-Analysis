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