from __future__ import annotations
from typing import List, Tuple, Dict, Union
from part_3 import MinHeap, HeapItem, create_a_star_test_case
from dataclasses import dataclass
import timeit 

weight = float
node = int 
edge = Tuple[weight, int]

class HeuristicGraph():
  def __init__(self):
    self.__heuristic : Dict[int, float] = {}

  def get_heuristic(self, node: int) -> float:
    return self.__heuristic[node]
  def set_heuristic(self, heuristic: Dict[int, float]) -> None:
    self.__heuristic = heuristic

class WeightedGraph(HeuristicGraph):

  def __init__(self):
    super().__init__()
  def w(self, start: int, end: int) -> float:
    return 0
    

class Graph(WeightedGraph):
  def __init__(self):
    super().__init__()
    self.__adj : Dict[int, List[Tuple[float, int]]] = {}
  def get_all_nodes(self) -> List[int]:
    return list(self.__adj.keys())
  def get_adj_nodes(self, node: int) -> List[Tuple[float, int]]:
    return self.__adj[node]
  def add_node(self, node: int) -> None:
    self.__adj[node] = []
  def add_edge(self, start: int, end: int, weight: float) -> None:
    self.__adj[start].append((weight, end))
  def get_num_of_nodes(self) -> int:
    return len(self.__adj)
  def w(self, start: int, end: int) -> float:
    for edge in self.__adj[start]:
      if edge[1] == end:
        return edge[0]
    return float('inf')
  


def djikstra(G:Graph, source: int, destination: int) -> Union[Tuple[Dict[int, int], List[int]], None]:
  '''
    This function implements the Dijkstra's algorithm to find the shortest path from the source node to the destination node.
    The function returns the cost of the shortest path and the path itself.
  '''
  ## initialize the priority queue 
  pq = MinHeap([HeapItem(0, source)])
  visited = set()
  parent = {}
  parent[source] = source
  parent[source] = None
  distances = {node: float('inf') for node in G.get_all_nodes()}
  distances[source] = 0

  while pq.is_empty() == False:
    _, node = pq.extract_min()

    if node in visited:
      continue

    visited.add(node)


    if node == destination:
      break

    for edge_weight, to_node in G.get_adj_nodes(node):
      if to_node not in visited:
        if distances[node] + edge_weight < distances[to_node]:
          distances[to_node] = distances[node] + edge_weight
          parent[to_node] = node

        pq.insert(HeapItem(distances[node] + edge_weight, to_node))
  
  ## reconstruct the path 
  
  path = []
  node = destination
  while node != source:
    if not node in parent:
      return None
    path.append(node)
    node = parent[node]
  path.append(source)
  path.reverse()
  return parent, path

def a_star(G:Graph, source: int, destination: int) -> Union[Tuple[Dict[int, int], List[int]], None]:
  '''
    This function implements the A* algorithm to find the shortest path from the source node to the destination node.
    The function returns the cost of the shortest path and the path itself.
  '''
  ## initialize the priority queue 
  pq = MinHeap([HeapItem(0, source)])
  visited = set()
  parent: Dict[int, int] = {}
  parent[source] = source
  parent[source] = -1
  distances = {node: float('inf') for node in G.get_all_nodes()}
  distances[source] = 0

  while pq.is_empty() == False:
    _, node = pq.extract_min()

    if node in visited:
      continue

    visited.add(node)


    if node == destination:
      break

    for edge_weight, to_node in G.get_adj_nodes(node):
      if to_node not in visited:
        if distances[node] + edge_weight < distances[to_node]:
          distances[to_node] = distances[node] + edge_weight
          parent[to_node] = node

        pq.insert(HeapItem(distances[node] + edge_weight + G.get_heuristic(to_node), to_node))
  
  ## reconstruct the path 
  path = []
  node = destination
  while node != source:
    path.append(node)
    if not node in parent:
      return None
    node = parent[node]
  path.append(source)
  path.reverse()
  return parent, path

  
@dataclass
class Station:
    id: int
    lat: float
    long: float

def read_csv_into_graph():
  node_map = {}
  G = Graph()
  with open('london_stations.csv', 'r') as f:
    i = 0
    for line in f:
      if i == 0:
        i += 1
        continue
      line = line.strip().split(',')
      id = int(line[0])
      lat = float(line[1])
      long = float(line[2])
      G.add_node(id)
      node_map[id] = Station(id, lat, long)



  with open('london_connections.csv', 'r') as f:
    edge_map: Dict[Tuple[int, int], int] = {}
    i = 0
    for line in f:
      if i == 0:
        i += 1
        continue
      line = line.strip().split(',')
      start = int(line[0])
      end = int(line[1])
      rail_line = int(line[2])

      ## get weight based on eudclidean distance of lat and long of two nodes
      ## we pull this from node_map
      weight = ((node_map[start].lat - node_map[end].lat)**2 + (node_map[start].long - node_map[end].long)**2)**0.5
      G.add_edge(start, end, weight)
      edge_map[(start, end)] = rail_line

    return G, node_map, edge_map




  
if __name__ == "__main__":
  G, node_map, edge_map = read_csv_into_graph()

  node_set = G.get_all_nodes()


  djikstra_times = []
  a_star_times = []




  def calculate_number_of_line_changes(path: List[int], edge_map: Dict[Tuple[int, int], int]) -> int:
    num_line_changes = 0
    for i in range(1, len(path) - 1):
      start = path[i]
      end = path[i + 1]
      if edge_map[(start, end)] != edge_map[(path[i - 1], start)]:
        num_line_changes += 1
    return num_line_changes

  for start in node_set:  
    for end in node_set:
      if start != end:
        G.set_heuristic({node: ((node_map[node].lat - node_map[end].lat)**2 + (node_map[node].long - node_map[end].long)**2)**0.5 for node in G.get_all_nodes()})
        a_star_path = a_star(G, start, end)
        if a_star_path is not None:
          parent, path = a_star_path
          a_star_times.append(timeit.timeit(lambda: a_star(G, start, end), number=1))
          

        djikstra_path = djikstra(G, start, end)
        if djikstra_path is not None:
          parent, path = djikstra_path
          djikstra_times.append(timeit.timeit(lambda: djikstra(G, start, end), number=1))

  print(sum(djikstra_times) )
  print(sum(a_star_times) )


## Question 4 
## there is a slight performance advantage to using A* over Dijkstra's algorithm. 
## this is because we're using the heuristic function to better select which nodes should 
## be visited first. However for this dataset, the difference is nominal. This is likely 
## because the nodes with the shortest path are close to each other, and the heuristic
## function doesn't provide much of an advantage. If the nodes were further apart, we would
## expect to see a larger difference between the two algorithms.
## only about 20% of pairs of nodes require a line change, other pairs are reachable by the same line.


## Question 5
## in the UML diagram, we have an inhieiarchy of classes, with the Graph class at the top. The Graph class
## has two subclasses, WeightedGraph and HeuristicGraph. The WeightedGraph class has a subclass called
## HeuristicGraph. The Graph class has a method called get_all_nodes, which returns a list of all nodes in the graph.
## The Graph class also has a method called get_adj_nodes, which returns a list of all adjacent nodes to a given node.
## The Graph class has a method called add_node, which adds a node to the graph. The Graph class has a method called
## add_edge, which adds an edge between two nodes. The Graph class has a method called get_num_of_nodes, which returns
## the number of nodes in the graph. The Graph class has a method called w, which returns the weight of an edge between two nodes.

## We also implement functions which depend on instances of the graph class, djiastra and a_star. These functions
## implement the djikstra and a_star algorithms respectively. The djikstra function finds the shortest path between two nodes

## Since we use the int representation of the node as they key, we would need to be able to hash the new type of the node, 
## we could do this by defining a __hash__ method for the Station class. We would also need to define an __eq__ method for the
## Station class, so that we can compare two Station objects for equality.
## we need the value to be hashable since we use it as a key in a dictionary. We need the __eq__ method so that we can compare
## two Station objects for equality. We need to be able to compare two Station objects for equality so that we can check if a node

## The graph class could be implemented by network graphs, machine learning compilers for dependancy graphs, databases for graph querying 
## functionality, etc. Since the graph class implements weights, and heuristics, it could be used in a variety of applications where
## we need to find the shortest path between nodes. 

