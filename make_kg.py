import json
import networkx as nx
from pyvis.network import Network
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a knowledge graph from a JSON file.")
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('output_file', type=str, help='Path to the output HTML file')
    args = parser.parse_args()

    with open(args.input_file) as f:
        data = json.load(f)

    grouped_tuples = data["grouped_tuples"]

    # Create a directed graph
    G = nx.DiGraph()
    

    # Add edges to the graph
    added_edges = set()
    for key, tuples in grouped_tuples.items():
        for t in tuples:
            edge = (t[0], t[2], t[1])
            if edge not in added_edges:
                G.add_edge(t[0], t[2], label=t[1])
                added_edges.add(edge)

    # Create a PyVis network
    net = Network(notebook=True, height='750px', width='100%', directed=True)

    # Load the NetworkX graph into PyVis
    net.from_nx(G)

    # Add labels to edges
    # for edge in G.edges(data=True):
    #     src = edge[0]
    #     dst = edge[1]
    #     label = edge[2]['label']
    #     net.add_edge(src, dst, title=label, label=label)
        
    net.set_edge_smooth('dynamic')
    net.show(args.output_file)

if __name__ == "__main__":
    main()
