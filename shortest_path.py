import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def find_shortest_paths(graph: list[list]):
    num_nodes = len(graph)
    infinity = float('inf')

    # Initialize the matrices with infinity values.
    min_paths = np.full((num_nodes, num_nodes), infinity)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                min_paths[i, j] = 0
            elif graph[i][j] != 0:
                min_paths[i, j] = graph[i][j]

    # Perform the matrix chain multiplication algorithm.
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if min_paths[i, k] + min_paths[k, j] < min_paths[i, j]:
                    min_paths[i, j] = min_paths[i, k] + min_paths[k, j]

    return min_paths


def visualize_floyd_warshall(graph):
    num_nodes = len(graph)
    infinity = float('inf')

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes to the graph
    G.add_nodes_from(range(num_nodes))

    # Initialize the `min_paths` matrix with infinity values
    min_paths = np.full((num_nodes, num_nodes), infinity)

    # Initialize a colormap for edge labels
    edge_colors = {}

    # Fill in edge data and add edges to the graph
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                min_paths[i, j] = 0
            elif graph[i][j] != 0:
                min_paths[i, j] = graph[i][j]
                G.add_edge(i, j, weight=graph[i][j])
                edge_colors[(i, j)] = 'black'

    # Create a figure and axis for the plot
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)  # Layout the graph nodes

    # Create a colormap for edge labels
    edge_labels = {(i, j): str(min_paths[i, j]) if min_paths[i, j] != infinity else '∞' for i, j in G.edges}

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='black')

    # Display the graph with labels
    plt.axis('off')
    plt.show()

    # Perform the Floyd-Warshall algorithm
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if min_paths[i, k] + min_paths[k, j] < min_paths[i, j]:
                    min_paths[i, j] = min_paths[i, k] + min_paths[k, j]
                    edge_colors[(i, j)] = 'red'

        # Display the updated graph after each iteration
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray')
        nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='black')
        edge_colors = {(i, j): 'black' for i, j in G.edges}  # Reset edge colors
        for i, j in G.edges:
            if min_paths[i, j] != infinity:
                edge_colors[(i, j)] = 'red'
        nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color=[edge_colors[(i, j)] for i, j in G.edges])
        plt.axis('off')
        plt.title(f'Iteration {k + 1}')
        plt.show()


if __name__ == "__main__":
    # Define the graph as an adjacency matrix.

    search_graph = [
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 5, 10, 0],
        [10, 8, 0, 0, 15, 6],
        [0, 0, 5, 0, 0, 0],
        [3, 0, 0, 2, 0, 5],
        [0, 16, 0, 0, 0, 0]
    ]

    shortest_paths = find_shortest_paths(search_graph)
    print("Shortest paths between all pairs of nodes:")
    print(shortest_paths)

    visualize_floyd_warshall(search_graph)
