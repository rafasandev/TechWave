import sys
import os
import networkx as nx
from pyvis.network import Network
from compiler.main import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.vertice import *


def get_graph_db():
    graph_view = GraphScene()
    return process_command("list", graph_view)


def create_graph_complete(raw_data):
    Graph = nx.MultiGraph()

    for data in raw_data:

        vertice = Vertice(
            name=data[0],
            category=data[1],
            value=int(data[2]),
            connections=data[3],
        )

        Graph.add_node(
            node_for_adding=vertice.name,
            category=vertice.category,
            group=vertice.category,
            size=20,
            title=(
                vertice.category
                if (vertice.category is not None or vertice.category)
                else vertice.name
            ),
        )

        if vertice.connections is not None:
            Graph.add_edge(
                u_for_edge=vertice.name,
                v_for_edge=vertice.connections,
                weight=(vertice.value / 10) + 5,
                color="rgba(208,204,202,0.8)",
            )
    return Graph


def generate_graph_html():
    graph_db = get_graph_db()
    print(graph_db)

    Graph = create_graph_complete(graph_db)

    net = Network(
        notebook=False,
        cdn_resources="remote",
        bgcolor="#272E25",
        height="101vh",
        font_color="#ffffff",
    )

    net.from_nx(Graph)

    net.force_atlas_2based()
    return net.generate_html()
