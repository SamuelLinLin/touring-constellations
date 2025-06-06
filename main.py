import networkx as nx
import json
import matplotlib.pyplot as plt


file = "data/edges-6.txt"

from graph import create_graph_from_edges_file, get_eulerian_tour, standardize_graph_positions
G = create_graph_from_edges_file(file)

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

odd_degree_count = sum(1 for degree in degrees if degree % 2 != 0)
print("Number of vertices with an odd degree:", odd_degree_count)

is_connected = nx.is_connected(G)
print("Is the graph connected?", is_connected)


G_standardized = standardize_graph_positions(G)


# # Draw the standardized graph
# plt.figure(figsize=(9, 9))
# pos = {node: node for node in G_standardized.nodes()}
# # for testing purposes
# #nx.draw_networkx(G_standardized, pos, alpha=0.6, font_size=3) 
# nx.draw_networkx_edges(G_standardized, pos, alpha=0.6)
# plt.show()


def plot_comparison(file, G_constructed):
    # --- Step 1: Load raw edges ---
    edges = []
    with open(file, 'r') as f:
        for line in f:
            x1, y1, x2, y2 = map(float, line.strip().split())
            edges.append(((x1, y1), (x2, y2)))

    # --- Step 2: Setup side-by-side plots ---
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))  # 1 row, 2 columns

    # --- Plot 1: Raw edges ---
    ax1 = axes[0]
    for (x1, y1), (x2, y2) in edges:
        ax1.plot([x1, x2], [y1, y2], 'k-', alpha=0.5)
        ax1.plot([x1, x2], [y1, y2], 'ro', markersize=2)
    ax1.set_aspect('equal')
    ax1.set_title("Raw Edges from File")

    # --- Plot 2: Constructed Graph ---
    ax2 = axes[1]
    pos = {node: node for node in G_constructed.nodes()}
    nx.draw(G_constructed, pos=pos, ax=ax2, with_labels=False, node_size=10, alpha=0.7)
    ax2.set_title("Constructed Graph")

    # --- Show both ---
    plt.tight_layout()
    plt.show()
    
plot_comparison(file, G)

# if not is_connected:
#   components = list(nx.connected_components(G))
#   for i, component in enumerate(components):
#     subgraph = G.subgraph(component)
#     plt.figure(figsize=(9, 9))
#     pos = {node: node for node in subgraph.nodes()}
#     nx.draw_networkx(subgraph, pos, alpha=0.6, font_size=5)
#     plt.title(f"Component {i + 1}")
#     plt.show()

eular_tour = get_eulerian_tour(G_standardized)
print("Eulerian tour:" + str(eular_tour))


with open("eulerian_tour.json", "w") as file:
  json.dump(eular_tour, file)