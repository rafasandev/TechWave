import sys
import os
import random
import networkx as nx
from pyvis.network import Network

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.vertice import *

categorias = {
    "Categoria 1": "#FFB3B3",
    "Categoria 2": "#FF6666",
    "Categoria 3": "#FF3333",
    "Categoria 4": "#B3FFB3",
    "Categoria 5": "#66FF66",
    "Categoria 6": "#33FF33",
    "Categoria 7": "#B3B3FF",
    "Categoria 8": "#6666FF",
    "Categoria 9": "#3333FF",
    "Categoria 10": "#FFE0B3",
    "Categoria 11": "#FF9966",
    "Categoria 12": "#FF6600",
}


def gerar_valor():
    return random.randint(0, 200)


def escolher_categoria():
    return random.choice(list(categorias.keys()))


def escolher_tecnologia():
    tecnologias = []
    for tec in range(50):
        tecnologias.append("Dependência " + str(tec))
    return random.choice(tecnologias)


vertices_data = []

for num in range(50):
    vertices_data.append(
        (
            escolher_tecnologia(),
            escolher_tecnologia(),
            gerar_valor(),
            escolher_categoria(),
        )
    )


def create_graph_complete(raw_data):
    Graph = nx.MultiGraph()

    for data in raw_data:
        vertice = Vertice(data[0], (data[2] * 0.1), data[3], data[1])

        Graph.add_node(
            vertice.name,
            category=vertice.category,
            color=definir_cor_vertice(vertice.category),
            size=20,
            title=vertice.generate_html_connections(),
            group=vertice.category,
        )

        Graph.add_edge(
            vertice.name,
            vertice.connections,
            weight=(vertice.value / 10) + 5,
            color="rgba(208,204,202,0.8)",
        )
    return Graph


def definir_cor_vertice(category):
    if category in categorias:
        return categorias[category]
    else:
        return "#cccccc"


def generate_graph_html():

    Graph = create_graph_complete(vertices_data)

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
