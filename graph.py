import networkx as nx
import matplotlib.pyplot as plt
import math
  
def create_graph_from_edges_file(edges_file):
  """
  Reads a file of edges and creates a NetworkX graph.
  Merges nodes that are within a given Euclidean distance (tolerance).

  Parameters:
    edges_file (str): Path to the file containing edges in the format "x1 y1 x2 y2".

  Returns:
    nx.Graph: A graph where nodes are coordinate tuples and edges connect them.
  """
  tolerance = 1  # Adjust as needed
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
  """
  Computes an Eulerian tour (path that visits every edge exactly once) of the given graph.

  Parameters:
      graph (nx.Graph): A NetworkX graph that has an Eulerian path.

  Returns:
      List[Tuple[Any, Any]]: A list of edges (as tuples of nodes) representing the Eulerian path.

  Raises:
      NetworkXError: If the graph is not Eulerian or does not have an Eulerian path.
  """
  tour = list(nx.eulerian_path(graph))
  return tour

def get_eulerian_circuit(graph):
  """
  Computes an Eulerian circuit (path that visits every edge exactly once) of the given graph.

  Parameters:
      graph (nx.Graph): A NetworkX graph that has an Eulerian path.

  Returns:
      List[Tuple[Tuple[float, float], Tuple[float, float]]]: A list of edges (as tuples of nodes) representing the Eulerian path.

  Raises:
      NetworkXError: If the graph is not Eulerian or does not have an Eulerian path.
  """
    def dfs(cur, G, path):
        neighbors = list(G.neighbors(cur))
        for neighbor in neighbors:
            if G.has_edge(cur, neighbor):
                G.remove_edge(cur, neighbor)
                dfs(neighbor, G, path)
        path.append(cur)

    G_copy = graph.copy()
    path = []
    start_node = next(iter(G_copy.nodes))
    dfs(start_node, G_copy, path)
    path.reverse() 

    edge_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    return edge_path

def get_shortest_eulerian_circuit(graph):
  """
  Computes an Eulerian circuit that always selects the shortest unused edge.

  Parameters:
      graph (nx.Graph): A NetworkX graph that has an Eulerian path.

  Returns:
      List[Tuple[Tuple[float, float], Tuple[float, float]]]: A list of edges (as tuples of nodes) representing the Eulerian path.

  Raises:
      NetworkXError: If the graph is not Eulerian or does not have an Eulerian path.
  """
    def dfs(cur, G, path):
        neighbors = sorted(
            G.neighbors(cur),
            key=lambda neighbor: euclidean_distance(cur, neighbor)
        )

        for neighbor in neighbors:
            if G.has_edge(cur, neighbor):
                G.remove_edge(cur, neighbor)
                dfs(neighbor, G, path)
        path.append(cur)

    G_copy = graph.copy()
    path = []
    start_node = next(iter(G_copy.nodes))
    dfs(start_node, G_copy, path)
    path.reverse()

    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]

def get_longest_eulerian_circuit(graph):
  """
  Computes an Eulerian circuit that always selects the longest unused edge.

  Parameters:
      graph (nx.Graph): A NetworkX graph that has an Eulerian path.

  Returns:
      List[Tuple[Tuple[float, float], Tuple[float, float]]]: A list of edges (as tuples of nodes) representing the Eulerian path.

  Raises:
      NetworkXError: If the graph is not Eulerian or does not have an Eulerian path.
  """
    def dfs(cur, G, path):
        neighbors = sorted(
            G.neighbors(cur),
            key=lambda neighbor: euclidean_distance(cur, neighbor),
            reverse=True
        )

        for neighbor in neighbors:
            if G.has_edge(cur, neighbor):
                G.remove_edge(cur, neighbor)
                dfs(neighbor, G, path)
        path.append(cur)

    G_copy = graph.copy()
    path = []
    start_node = next(iter(G_copy.nodes))
    dfs(start_node, G_copy, path)
    path.reverse()

    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]

def get_smallest_turn_eulerian_circuit(graph):
  """
  Computes an Eulerian circuit that always selects the unused edge that makes the smallest turn from the previous edge.

  Parameters:
      graph (nx.Graph): A NetworkX graph that has an Eulerian path.

  Returns:
      List[Tuple[Tuple[float, float], Tuple[float, float]]]: A list of edges (as tuples of nodes) representing the Eulerian path.

  Raises:
      NetworkXError: If the graph is not Eulerian or does not have an Eulerian path.
  """
    def dfs(cur, G, path, prev=None):
        neighbors = list(G.neighbors(cur))

        if prev is not None:
            prev_vec = vector_from_edge(prev, cur)
            neighbors.sort(key=lambda n: -cosine_similarity(prev_vec, vector_from_edge(cur, n)))
        for neighbor in neighbors:
            if G.has_edge(cur, neighbor):
                G.remove_edge(cur, neighbor)
                dfs(neighbor, G, path, cur)
        path.append(cur)

    G_copy = graph.copy()
    path = []
    start_node = next(iter(G_copy.nodes))
    dfs(start_node, G_copy, path)
    path.reverse()

    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]

def get_largest_turn_eulerian_circuit(graph):
  """
  Computes an Eulerian circuit that always selects the unused edge that makes the largest turn from the previous edge.

  Parameters:
      graph (nx.Graph): A NetworkX graph that has an Eulerian path.

  Returns:
      List[Tuple[Tuple[float, float], Tuple[float, float]]]: A list of edges (as tuples of nodes) representing the Eulerian path.

  Raises:
      NetworkXError: If the graph is not Eulerian or does not have an Eulerian path.
  """
    def dfs(cur, G, path, prev=None):
        neighbors = list(G.neighbors(cur))

        if prev is not None:
            prev_vec = vector_from_edge(prev, cur)
            neighbors.sort(key=lambda n: cosine_similarity(prev_vec, vector_from_edge(cur, n)))
        for neighbor in neighbors:
            if G.has_edge(cur, neighbor):
                G.remove_edge(cur, neighbor)
                dfs(neighbor, G, path, cur)
        path.append(cur)

    G_copy = graph.copy()
    path = []
    start_node = next(iter(G_copy.nodes))
    dfs(start_node, G_copy, path)
    path.reverse()

    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def standardize_graph_positions(graph):
  """
  Scales the positions of coordinate nodes in a graph to fit within a 800 by 800 canvas.
  The output coordinates will be in the range [10, 790] for both x and y axes.

  Parameters:
      graph (nx.Graph): A NetworkX graph with 2D coordinate tuples (x, y) as nodes.

  Returns:
      nx.Graph: A new graph with the same structure as the input but with node positions scaled
                to the [10, 790] range. Edges are added between the scaled nodes accordingly.
  """
  x_coords, y_coords = zip(*graph.nodes())
    
  min_x, max_x = min(x_coords), max(x_coords)
  min_y, max_y = min(y_coords), max(y_coords)
    
  scaled_graph = nx.Graph()

  x_diff = max_x - min_x
  y_diff = max_y - min_y
    
  for (x, y) in graph.nodes():
    if x_diff == 0:
      scaled_x = 400  
    else:
      scaled_x = 10 + (x - min_x) / (x_diff) * (790 - 10)

    if y_diff == 0:
      scaled_y = 400  
    else:
      scaled_y = 10 + (y - min_y) / (y_diff) * (790 - 10)

    scaled_graph.add_node((scaled_x, scaled_y))
    
  for (u, v) in graph.edges():
    scaled_graph.add_edge(
      (10 + (u[0] - min_x) / x_diff * (790 - 10) if x_diff != 0 else 400,
      10 + (u[1] - min_y) / y_diff * (790 - 10) if y_diff != 0 else 400),
      (10 + (v[0] - min_x) / x_diff * (790 - 10) if x_diff != 0 else 400,
      10 + (v[1] - min_y) / y_diff * (790 - 10) if y_diff != 0 else 400)
    )
    
  return scaled_graph

def vector_from_edge(a, b):
    return (b[0] - a[0], b[1] - a[1])

def cosine_similarity(v1, v2):
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    mag1 = math.hypot(v1[0], v1[1])
    mag2 = math.hypot(v2[0], v2[1])
    if mag1 == 0 or mag2 == 0:
        return -1  
    return dot / (mag1 * mag2)

def euclidean_distance(p1, p2):
  return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5