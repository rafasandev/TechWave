import networkx as nx
from pyvis.network import Network

def generate_graph_html():
    Graph = nx.MultiGraph()

    edges = [
        ['A', 'B', 20], 
        ['A', 'H', 2],

        ['B', 'A', 8], 
        ['B', 'C', 2], 
        ['B', 'H', 2],
        
        ['C', 'B', 2], 
        ['C', 'D', 2], 
        ['C', 'F', 2], 
        ['C', 'I', 2], 

        ['D', 'C', 2],
        ['D', 'F', 2], 

        ['F', 'C', 2],
        ['F', 'D', 2], 
        ['F', 'E', 2], 
        ['F', 'G', 2], 

        ['G', 'F', 2], 
        ['G', 'H', 2],
        ['G', 'I', 2], 

        ['H', 'A', 2], 
        ['H', 'B', 2], 
        ['H', 'G', 2], 
        ['H', 'I', 2],
        
        ['I', 'C', 2], 
        ['I', 'G', 2], 
        ['I', 'H', 2]
    ]

    Graph.add_weighted_edges_from(edges)

    net = Network(
        notebook=False, 
        cdn_resources='remote', 
        bgcolor="#5C5C5C", 
        height="101vh",
        font_color="#000000",
    )


    for node in Graph.nodes:
        net.add_node(node, color="#BAA89C")

    for edge in Graph.edges(data=True):
        net.add_edge(edge[0], edge[1], weight=edge[2], color="#D0CCCA")

    net.force_atlas_2based()
    return net.generate_html()

