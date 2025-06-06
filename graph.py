import networkx as nx

import matplotlib.pyplot as plt

def euclidean_distance(p1, p2):
  return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
  
def create_graph_from_edges_file(edges_file):
  tolerance = 0.0000000001  # Adjust as needed
  G = nx.Graph()

  def find_existing_node(x, y):
      for node in G.nodes():
          if euclidean_distance(node, (x, y)) < tolerance:
              return node
      return (x, y)

  with open(edges_file, 'r') as file:
      for line in file:
          x1, y1, x2, y2 = map(float, line.split())

          node1 = find_existing_node(x1, y1)
          node2 = find_existing_node(x2, y2)

          G.add_edge(node1, node2)

  return G



def get_eulerian_tour(graph):
  tour = list(nx.eulerian_path(graph))
  return tour



def standardize_graph_positions(graph):
  x_coords, y_coords = zip(*graph.nodes())
    
  min_x, max_x = min(x_coords), max(x_coords)
  min_y, max_y = min(y_coords), max(y_coords)
    
  scaled_graph = nx.Graph()

  x_diff = max_x - min_x
  y_diff = max_y - min_y
    
  for (x, y) in graph.nodes():
    if x_diff == 0:
      scaled_x = 200  # or some other default value
    else:
      scaled_x = 10 + (x - min_x) / (x_diff) * (390 - 10)

    if y_diff == 0:
      scaled_y = 200  # or some other default value
    else:
      scaled_y = 10 + (y - min_y) / (y_diff) * (390 - 10)

    scaled_graph.add_node((scaled_x, scaled_y))
    
  for (u, v) in graph.edges():
    scaled_graph.add_edge(
      (10 + (u[0] - min_x) / x_diff * (390 - 10) if x_diff != 0 else 200,
      10 + (u[1] - min_y) / y_diff * (390 - 10) if y_diff != 0 else 200),
      (10 + (v[0] - min_x) / x_diff * (390 - 10) if x_diff != 0 else 200,
      10 + (v[1] - min_y) / y_diff * (390 - 10) if y_diff != 0 else 200)
    )
    
  return scaled_graph
