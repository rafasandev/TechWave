import sys
import os
import random
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

        cor_vertice = definir_cor_vertice(vertice.category)

        Graph.add_node(
            vertice.name,
            category=vertice.category,
            color=cor_vertice,
            group=vertice.category,
            size=20,
            title=vertice.category,
        )

        if vertice.connections is None:
            Graph.add_edge(
                u_for_edge=vertice.name,
                weight=(vertice.value / 10) + 5,
                color="rgba(208,204,202,0.8)",
            )
        else:
            Graph.add_edge(
                u_for_edge=vertice.name,
                v_for_edge=vertice.connections,
                weight=(vertice.value / 10) + 5,
                color="rgba(208,204,202,0.8)",
            )

    return Graph


def definir_cor_vertice(category):

    categorias = {
        "frontend": "#FFB3B3",
        "backend": "#FF6666",
        "servidor": "#FF3333",
        "frontend": "#B3FFB3",
        "frontend": "#66FF66",
        "frontend": "#33FF33",
        "frontend": "#B3B3FF",
        "frontend": "#6666FF",
        "frontend": "#3333FF",
        "frontend": "#FFE0B3",
        "frontend": "#FF9966",
        "frontend": "#FF6600",
    }

    if category is not None:
        category = category.lower()
    else:
        category = ""

    return categorias.get(category, "#c8e721")


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
