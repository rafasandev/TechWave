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

    # Dicionário para armazenar o número de conexões de cada vértice
    connection_counts = {}

    # Primeiro loop: contar conexões de cada vértice
    for data in raw_data:
        vertice_name = data[0]
        connected_to = data[3]

        # Incrementa a contagem para o vértice atual
        if vertice_name not in connection_counts:
            connection_counts[vertice_name] = 0
        connection_counts[vertice_name] += 1

    # Segundo loop: adicionar vértices e arestas com pesos ajustados
    for data in raw_data:
        vertice = Vertice(
            name=data[0],
            category=data[1],
            value=int(data[2]),
            connections=data[3],
        )

        # Adicionar o nó ao grafo
        Graph.add_node(
            node_for_adding=vertice.name,
            category=vertice.category,
            group=vertice.category,
            size=20,
            title=(
                f"Categoria: {vertice.category.replace('_', ' ')}\n Valor: {vertice.value}"
                if (vertice.category is not None or vertice.category)
                else f"Valor: {vertice.value}"
            ),
        )

        # Adicionar a aresta se houver uma conexão
        if vertice.connections is not None:
            connected_vertice_value = int(
                [
                    item[2]
                    for item in raw_data
                    if item[0] == vertice.connections and item[3] == vertice.name
                ][0]
            )

            count_a = connection_counts[vertice.name]
            count_b = connection_counts[vertice.connections]

            edge_weight = (vertice.value / count_a) + (
                connected_vertice_value / count_b
            )
            edge_width = edge_weight / 10

            Graph.add_edge(
                u_for_edge=vertice.name,
                v_for_edge=vertice.connections,
                weight=edge_weight,
                color="rgba(208,204,202,0.8)",
                width=edge_width,
                title=f"Custo: R${edge_weight:.2f}",
            )
    return Graph


def generate_graph_html():
    graph_db = get_graph_db()
    print(graph_db)

    Graph = create_graph_complete(graph_db)

    communities = nx.algorithms.community.greedy_modularity_communities(Graph)
    print(communities)

    positions = nx.spring_layout(Graph, seed=42)

    net = Network(
        notebook=False,
        cdn_resources="remote",
        bgcolor="#272E25",
        height="101vh",
        font_color="#ffffff",
    )

    for node, pos in positions.items():
        x, y = pos[0] * 1000, pos[1] * 1000
        net.add_node(
            node,
            x=x,
            y=y,
            title=Graph.nodes[node].get("title"),
            group=Graph.nodes[node].get("group"),
            size=Graph.nodes[node].get("size"),
        )

    for edge in Graph.edges(data=True):
        net.add_edge(
            edge[0],
            edge[1],
            weight=edge[2].get("weight"),
            width=edge[2].get("width"),
            color=edge[2].get("color"),
            title=edge[2].get("title"),
        )
    # net.from_nx(Graph)

    return net.generate_html()
