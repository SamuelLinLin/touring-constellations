import networkx as nx

import matplotlib.pyplot as plt

# Load edges from file
edges_file = "/Users/samuelyslinlin/touring-constellations/data/edges-12.txt"
tolerance = 0.01  # Tolerance for merging nodes
G = nx.Graph()

with open(edges_file, 'r') as file:
  for line in file:
    x1, y1, x2, y2 = map(float, line.split())
    merged = False

    for node in G.nodes():
      if abs(node[0] - x1) < tolerance and abs(node[1] - y1) < tolerance:
        x1, y1 = node
        merged = True
      if abs(node[0] - x2) < tolerance and abs(node[1] - y2) < tolerance:
        x2, y2 = node
        merged = True

    # If the nodes are very close, merge them
    if abs(x1 - x2) < tolerance and abs(y1 - y2) < tolerance:
      G.add_node((x1, y1))
    else:
      if not merged:
        G.add_node((x1, y1))
        G.add_node((x2, y2))
      G.add_edge((x1, y1), (x2, y2))

# Draw the graph
plt.figure(figsize=(9, 9))
pos = {node: node for node in G.nodes()}
nx.draw_networkx(G, pos, alpha=0.6) # for testing purposes
# nx.draw_networkx_edges(G, pos, alpha=0.6)
plt.show()
# Describe the created graph
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

degrees = [val for (node, val) in G.degree()]
highest_degree = max(degrees)
lowest_degree = min(degrees)
average_degree = sum(degrees) / len(degrees)
print("Highest degree:", highest_degree)
print("Lowest degree:", lowest_degree)
print("Average degree:", average_degree)