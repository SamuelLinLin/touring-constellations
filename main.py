import networkx as nx
import json
import matplotlib.pyplot as plt


file = "data/edges-1.txt"

from graph import create_graph_from_edges_file, get_eulerian_tour, standardize_graph_positions, get_eulerian_circuit, get_shortest_eulerian_circuit, get_longest_eulerian_circuit, get_largest_turn_eulerian_circuit, get_smallest_turn_eulerian_circuit
G = create_graph_from_edges_file(file)

G_standardized = standardize_graph_positions(G)

# Get standard Eulerian tour
eular_tour_standard = get_eulerian_circuit(G_standardized)

with open("eulerian_tour.json", "w") as file:
  json.dump(eular_tour_standard, file)
  
# Get Eulerian tour where the the shortest edge is selected
eular_tour_closest = get_shortest_eulerian_circuit(G_standardized)

with open("eulerian_tour_shortest_edge.json", "w") as file:
  json.dump(eular_tour_closest, file)
  
# Get Eulerian tour where the the longest edge is selected
eular_tour_farthest = get_longest_eulerian_circuit(G_standardized)

with open("eulerian_tour_longest_edge.json", "w") as file:
  json.dump(eular_tour_farthest, file)
  
# Get Eulerian tour where the the edge that makes the largest turn from the previous edge is selected
eular_tour_largest_turn = get_largest_turn_eulerian_circuit(G_standardized)

with open("eulerian_tour_largest_turn.json", "w") as file:
  json.dump(eular_tour_largest_turn, file)
  
# Get Eulerian tour where the the edge that makes the smallest turn from the previous edge is selected
eulerian_circuit_smallest_turn = get_smallest_turn_eulerian_circuit(G_standardized)

with open("eulerian_tour_smallest_turn.json", "w") as file:
  json.dump(eulerian_circuit_smallest_turn, file)