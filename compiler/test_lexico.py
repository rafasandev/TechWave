import sys
import networkx as nx
import pickle
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtCore import Qt, QPointF
import random
import pickle

# Classe que usa QGraphicsView e QGraphicsScene para visualizar vértices e arestas
class GraphScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.graph = nx.Graph()
        self.vertices = {}

    def generate_random_position(self):
        """Gera coordenadas aleatórias para novos vértices."""
        return random.uniform(0, 500), random.uniform(0, 500)

    def add_vertex(self, name, x=None, y=None):
        """Adiciona um novo vértice ao grafo."""
        if name in self.vertices:
            print(f"O vértice '{name}' já existe.")
            return
        if x is None or y is None:
            x, y = self.generate_random_position()

        vertex = QGraphicsEllipseItem(0, 0, 30, 30)
        vertex.setBrush(QBrush(Qt.GlobalColor.blue))
        vertex.setPen(QPen(Qt.GlobalColor.black))
        vertex.setPos(QPointF(x, y))
        self.addItem(vertex)
        self.vertices[name] = vertex
        self.graph.add_node(name)
        print(f"Vértice '{name}' adicionado na posição ({x}, {y}).")

    def modify_vertex(self, old_name, new_name, x=None, y=None):
        """Modifica um vértice existente no grafo."""
        if old_name not in self.vertices:
            print(f"Vértice '{old_name}' não encontrado.")
            return
        if new_name in self.vertices and new_name != old_name:
            print(f"Vértice '{new_name}' já existe.")
            return

        if x is None or y is None:
            x, y = self.generate_random_position()

        vertex_item = self.vertices.pop(old_name)
        self.removeItem(vertex_item)
        self.graph.remove_node(old_name)

        vertex_item = QGraphicsEllipseItem(0, 0, 30, 30)
        vertex_item.setBrush(QBrush(Qt.GlobalColor.blue))
        vertex_item.setPen(QPen(Qt.GlobalColor.black))
        vertex_item.setPos(QPointF(x, y))
        self.addItem(vertex_item)
        self.vertices[new_name] = vertex_item
        self.graph.add_node(new_name)
        print(f"Vértice '{old_name}' modificado para '{new_name}' na posição ({x}, {y}).")

    def delete_vertex(self, name):
        """Remove um vértice e suas arestas do grafo."""
        if name not in self.vertices:
            print(f"Vértice '{name}' não encontrado.")
            return

        vertex_item = self.vertices.pop(name)
        self.removeItem(vertex_item)
        self.graph.remove_node(name)

        edges_to_remove = list(self.graph.edges(name))
        self.graph.remove_edges_from(edges_to_remove)
        print(f"Vértice '{name}' e suas arestas foram removidos.")

    def add_edge(self, name1, name2):
        """Conecta dois vértices com uma aresta."""
        if name1 in self.vertices and name2 in self.vertices:
            vertice1 = self.vertices[name1]
            vertice2 = self.vertices[name2]
            line = QGraphicsLineItem(vertice1.x() + 15, vertice1.y() + 15, vertice2.x() + 15, vertice2.y() + 15)
            self.addItem(line)
            self.graph.add_edge(name1, name2)
            print(f"Aresta adicionada entre '{name1}' e '{name2}'.")
        else:
            print(f"Erro: Um ou ambos os vértices '{name1}' e '{name2}' não existem.")

    def list_graph(self):
        """Exibe os vértices e arestas do grafo atual."""
        print("Vértices no grafo:")
        for name, vertex in self.vertices.items():
            x, y = vertex.x(), vertex.y()
            print(f" - {name}: ({x}, {y})")
        print("Arestas no grafo:")
        for edge in self.graph.edges:
            print(f" - {edge[0]} <--> {edge[1]}")

    def save_graph(self, filename):
            try:
                # Verifica se existem vértices no grafo
                if not self.graph.nodes:
                    print("Nenhum vértice existente para salvar.")
                    return

                # Salva os dados do grafo e as coordenadas dos vértices
                vertex_data = {}
                for name, item in self.vertices.items():
                    vertex_data[name] = (item.pos().x(), item.pos().y())

                with open(filename, 'wb') as file:
                    pickle.dump((self.graph, vertex_data), file)
                print(f"Grafo salvo em '{filename}'.")
            except Exception as e:
                print(f"Erro ao salvar o grafo: {e}")

    def load_graph(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.graph, vertex_data = pickle.load(file)
                self.vertices.clear()  # Limpa os vértices existentes na cena
                self.clear()  # Limpa a cena gráfica
                
                for name, (x, y) in vertex_data.items():
                    self.add_vertex(name, x, y)  # Adiciona novamente os vértices na cena
                
                print(f"Grafo carregado de '{filename}'.")
        except Exception as e:
            print(f"Erro ao carregar o grafo: {e}")


# Classe principal da interface gráfica
class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = GraphScene()
        self.setScene(self.scene)

    def add_vertex(self, name, x=None, y=None):
        self.scene.add_vertex(name, x, y)

    def modify_vertex(self, old_name, new_name, x=None, y=None):
        self.scene.modify_vertex(old_name, new_name, x, y)

    def delete_vertex(self, name):
        self.scene.delete_vertex(name)

    def add_edge(self, name1, name2):
        self.scene.add_edge(name1, name2)

    def list_graph(self):
        self.scene.list_graph()

    def save_graph(self, filename):
        self.scene.save_graph(filename)

    def load_graph(self, filename):
        self.scene.load_graph(filename)

    def show_graph(self):
        """Mostra a janela do PyQt6 para visualizar o grafo."""
        self.show()

# Função para processar os comandos do terminal
def process_command(command, graph_view):
    tokens = command.split()
    if not tokens:
        return

    cmd = tokens[0].lower()

    if cmd == "add":
        if len(tokens) < 2:
            print("Erro: Comando incompleto. Use: add (nome) [x] [y]")
            return
        name = tokens[1]
        x = float(tokens[2]) if len(tokens) > 2 else None
        y = float(tokens[3]) if len(tokens) > 3 else None
        graph_view.add_vertex(name, x, y)

    elif cmd == "modify":
        if len(tokens) < 3:
            print("Erro: Comando incompleto. Use: modify (nome_antigo) (novo_nome) [x] [y]")
            return
        old_name = tokens[1]
        new_name = tokens[2]
        x = float(tokens[3]) if len(tokens) > 3 else None
        y = float(tokens[4]) if len(tokens) > 4 else None
        graph_view.modify_vertex(old_name, new_name, x, y)

    elif cmd == "delete":
        if len(tokens) != 2:
            print("Comando inválido. Use: delete (nome)")
            return
        name = tokens[1]
        graph_view.delete_vertex(name)

    elif cmd == "connect":
        if len(tokens) != 3:
            print("Comando inválido. Use: connect (nome1) (nome2)")
            return
        name1 = tokens[1]
        name2 = tokens[2]
        graph_view.add_edge(name1, name2)

    elif cmd == "list":
        graph_view.list_graph()

    elif cmd == "save":
        if len(tokens) != 2:
            print("Comando inválido. Use: save (arquivo.graph)")
            return
        filename = tokens[1]
        graph_view.save_graph(filename)


    elif cmd == "load":
        if len(tokens) != 2:
            print("Comando inválido. Use: load (arquivo.graph)")
            return
        filename = tokens[1]
        graph_view.load_graph(filename)


    elif cmd == "show":
        graph_view.show_graph()

    elif cmd == "exit":
        print("Saindo...")
        sys.exit()

    else:
        print(f"Comando desconhecido: {cmd}")

# Função principal
def main():
    app = QApplication(sys.argv)
    graph_view = GraphView()

    print("Bem-vindo ao gerenciador de grafos via terminal.")
    print("Comandos disponíveis:")
    print(" - add (nome) [x] [y]: Adiciona um novo vértice com nome e coordenadas.")
    print(" - modify (nome_antigo) (novo_nome) [x] [y]: Modifica um vértice existente.")
    print(" - delete (nome): Exclui um vértice e suas arestas.")
    print(" - connect (nome1) (nome2): Conecta dois vértices.")
    print(" - list: Lista todos os vértices e arestas.")
    print(" - save (arquivo.graph): Salva o grafo atual em um arquivo.")
    print(" - load (arquivo.graph): Carrega um grafo de um arquivo.")
    print(" - show: Mostra a visualização gráfica.")
    print(" - exit: Encerra o programa.")

    while True:
        command = input("Digite um comando: ")
        process_command(command, graph_view)

if __name__ == "__main__":
    main()
