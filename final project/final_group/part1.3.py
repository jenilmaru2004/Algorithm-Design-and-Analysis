from __future__ import annotations
from typing import List, Tuple, Dict, Any


import math
class MinHeap:
    def __init__(self, data):
        self.items = data
        self.length = len(data)
        self.map = {}
        for i in range(self.length):
            self.map[self.items[i].value] = i

        self.build_heap()


    def find_left_index(self,index):
        return 2 * (index + 1) - 1

    def find_right_index(self,index):
        return 2 * (index + 1)

    def find_parent_index(self,index):
        return (index + 1) // 2 - 1  
    
    def sink_down(self, index):
        smallest_known_index = index

        if self.find_left_index(index) < self.length and self.items[self.find_left_index(index)].key < self.items[index].key:
            smallest_known_index = self.find_left_index(index)

        if self.find_right_index(index) < self.length and self.items[self.find_right_index(index)].key < self.items[smallest_known_index].key:
            smallest_known_index = self.find_right_index(index)

        if smallest_known_index != index:
            self.items[index], self.items[smallest_known_index] = self.items[smallest_known_index], self.items[index]
            
            # update map
            self.map[self.items[index].value] = index
            self.map[self.items[smallest_known_index].value] = smallest_known_index

            # recursive call
            self.sink_down(smallest_known_index)

    def build_heap(self,):
        for i in range(self.length // 2 - 1, -1, -1):
            self.sink_down(i) 

    def insert(self, node):
        if len(self.items) == self.length:
            self.items.append(node)
        else:
            self.items[self.length] = node
        self.map[node.value] = self.length
        self.length += 1
        self.swim_up(self.length - 1)

    def insert_nodes(self, node_list):
        for node in node_list:
            self.insert(node)

    def swim_up(self, index):
        
        while index > 0 and self.items[index].key < self.items[self.find_parent_index(index)].key:
            #swap values
            self.items[index], self.items[self.find_parent_index(index)] = self.items[self.find_parent_index(index)], self.items[index]
            #update map
            self.map[self.items[index].value] = index
            self.map[self.items[self.find_parent_index(index)].value] = self.find_parent_index(index)
            index = self.find_parent_index(index)

    def get_min(self):
        if len(self.items) > 0:
            return self.items[0]

    def extract_min(self,):
        #xchange
        self.items[0], self.items[self.length - 1] = self.items[self.length - 1], self.items[0]
        #update map
        self.map[self.items[self.length - 1].value] = self.length - 1
        self.map[self.items[0].value] = 0

        min_node = self.items[self.length - 1]
        self.length -= 1
        self.map.pop(min_node.value)
        self.sink_down(0)
        return min_node

    def decrease_key(self, value, new_key):
        if new_key >= self.items[self.map[value]].key:
            return
        index = self.map[value]
        self.items[index].key = new_key
        self.swim_up(index)

    def get_element_from_value(self, value):
        return self.items[self.map[value]]

    def contains(self, value):
        return value in self.items 


    def is_empty(self):
        return self.length == 0
    
    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height + height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.items[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s
    

class Edge():
  def __init__(self, weight: float, value: int):
    self.weight = weight
    self.value = value
  def __repr__(self):
    return str((self.weight, self.value))
  def __iter__(self):
    yield self.weight
    yield self.value

## updated heap item a bit to make it more general
class HeapItem():
  def __init__(self, key: float, value: Any):
    self.key = key
    self.value = value
  def __repr__(self):
    return str((self.key, self.value))
  def __iter__(self):
    yield self.key
    yield self.value

Graph = Dict[int, List[Edge]]


def grid_to_node(i, j, n):
  return i * n + j


def print_grid(grid):
  for row in grid:
    print(row)
  print()

def create_a_star_test_case(n: int) -> Tuple[Graph, Dict[int, float]]:
  '''
    This function creates an N x N 2D int array respresenting 
    a grid. Adjacent cells of the grid are connected by edges
    in our graph. Cells at random will be blocked and will not be 
    able to be traversed. 
  '''

  grid = []
  for i in range(n):
    grid.append([])
    for j in range(n):
      grid[i].append(1)

  ## block off parts of grid
  for i in range(n - 3):
    grid[n // 2][i] = 0

  for i in range(n - 1):
    grid[i][8] = 0

  for i in range(1, n-1):
    grid[7][i] = 0


  grid[0][0] = 1  
  grid[n - 1][n - 1] = 1  
  
  # print_grid(grid)

  graph = {}
  heuristics= {}
  ## we create a graph with all the edges 
  for i in range(n):
    for j in range(n):
      if grid[i][j] == 0:
        continue
      grid_node = grid_to_node(i, j, n)
      graph[grid_node] = []
      heuristic_value = (n - j) + (n - i)


      ## check if we can create an edge 
      ## for each of the neighbors, and then 
      ## update the 
      if i < n - 1 and grid[i + 1][j] == 1:
        node = grid_to_node(i + 1, j, n)
        edge = Edge(1, node)
        graph[grid_node].append(edge)

      if i > 0 and grid[i - 1][j] == 1:
        node = grid_to_node(i - 1, j, n)
        edge = Edge(1, node)
        graph[grid_node].append(edge)

      if j < n - 1 and  grid[i][j + 1] == 1:
        node = grid_to_node(i, j + 1, n)
        edge = Edge(1, node)
        graph[grid_node].append(edge)

      if j > 0 and grid[i][j - 1] == 1:
        node = grid_to_node(i, j - 1, n)
        edge = Edge(1, node)
        graph[grid_node].append(edge)

      ## update the heuristic value for the current node (i, j)
      heuristics[grid_node] = heuristic_value
    

  return graph, heuristics


graph, heuristics = create_a_star_test_case(10)



def A_star(graph: Dict[int, List[Tuple[int, int]]], source: int, destination: int, heuristics: Dict[int, float]) -> Tuple[Dict[int, int], List[int]]:
  '''
    This function implements the A* algorithm to find the shortest path from the source node to the destination node.
    The function returns the cost of the shortest path and the path itself.
  '''

  ## initialize the priority queue 
  pq = MinHeap([HeapItem(0, source)])
  visited = set()
  parent = {}
  parent[source] = source
  parent[source] = None
  distances = {node: float('inf') for node in graph}
  distances[source] = 0

  while pq.is_empty() == False:
    _, node = pq.extract_min()

    if node in visited:
      continue

    visited.add(node)


    if node == destination:
      break

    for edge_weight, to_node in graph[node]:
      if to_node not in visited:
        if distances[node] + edge_weight < distances[to_node]:
          distances[to_node] = distances[node] + edge_weight
          parent[to_node] = node

        pq.insert(HeapItem(distances[node] + edge_weight + heuristics[to_node], to_node))
  
  ## reconstruct the path 
  path = []
  node = destination
  while node != source:
    path.append(node)
    node = parent[node]
  path.append(source)
  path.reverse()
  return parent, path




# print(A_star(graph, 0, 99, heuristics))



## 3.2 
## The A* algorithms tries to address the issue with Dijkstra's algorithm
## by using a heuristic to estimate the cost of the path from the current
## node to the goal node. The algorithm uses a priority queue to keep track
## of the nodes that need to be visited. Rather than visiting all nodes 
## and considering them to be equal candidates for the shortest path,
## A* uses the heuristic to prioritize nodes that are closer to the goal
## node. This allows the algorithm to converge faster and find the shortest
## path more efficiently.
##-------------------------------------------------------------------------
## We would test djikstra's algorithm on the same graph and compare the
## results with the A* algorithm. The graph in question would need to be designed
## in such a way that the heuristic value is somewhat useful in guiding the search

## If we were to use arbitrary (random) heuristic values, the A* algorithm would
## perform about as well as Dijkstra's algorithm. In this case the negative effects 
## of the heuristic would cancel out the benefits (assuming that the possuble heuristic values
## are uniformly distributed). Since we visit neighbors using a composite weighting of
## the edge weight and the heuristic value, on average the edge weighting would 
## dictate the search path, which is what we use in djikstra's algorithm.

## A* should be used in applications where we can predictably and reliably assign
## heuristic values to the nodes in the graph. This is often the case in pathfinding
## applications where we have a good idea of the distance between two points.





