import sys
import os
import random
import networkx as nx
from pyvis.network import Network

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.vertice import *

categorias = {
    "Frontend": "#FF9F80 ",
    "Backend": "#80FF9F ",
    "Database": "#9F80FF ",
    "Security": "#FFE680 ",
    "DevOps": "#80FFFF ",
}


# Função para gerar valores aleatórios
def gerar_valor():
    return random.randint(0, 200)  # Valores entre 5 e 100 para as arestas


# Função para escolher uma categoria aleatória
def escolher_categoria():
    return random.choice(list(categorias.keys()))


def escolher_tecnologia():
    tecnologias = [
        "Dependencia 1",
        "Dependencia 2",
        "Dependencia 3",
        "Dependencia 4",
        "Dependencia 5",
        "Dependencia 6",
        "Dependencia 7",
        "Dependencia 8",
        "Dependencia 9",
        "Dependencia 10",
        "Dependencia 11",
        "Dependencia 12",
        "Dependencia 13",
        "Dependencia 14",
        "Dependencia 15",
        "Dependencia 16",
        "Dependencia 17",
        "Dependencia 18",
        "Dependencia 19",
        "Dependencia 20",
        "Dependencia 21",
        "Dependencia 22",
        "Dependencia 23",
        "Dependencia 24",
        "Dependencia 25",
        "Dependencia 26",
        "Dependencia 27",
        "Dependencia 28",
        "Dependencia 29",
        "Dependencia 30",
        "Dependencia 31",
        "Dependencia 32",
        "Dependencia 33",
        "Dependencia 34",
        "Dependencia 35",
    ]
    return random.choice(tecnologias)


vertices_data = [
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
    (escolher_tecnologia(), escolher_tecnologia(), gerar_valor(), escolher_categoria()),
]


def create_graph_complete(raw_data):
    Graph = nx.MultiGraph()

    for data in raw_data:
        vertice = Vertice(data[0], (data[2] * 0.1), data[3], data[1])

        Graph.add_node(
            vertice.name,
            category=vertice.category,
            color=definir_cor_vertice(vertice.category),
            size=20,
            title="Categoria: " + vertice.category,
            group=vertice.category,
        )

        Graph.add_edge(
            vertice.name,
            vertice.connection,
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
