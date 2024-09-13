import sys
import networkx as nx
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtCore import Qt, QPointF

# Classe que usa QGraphicsView e QGraphicsScene para visualizar vértices e arestas
class GraphScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.graph = nx.Graph()
        self.vertices = {}

    def add_vertex(self, name, x, y):
        if name in self.vertices:
            print(f"O vértice '{name}' já existe.")
            return
        vertex = QGraphicsEllipseItem(0, 0, 30, 30)
        vertex.setBrush(QBrush(Qt.GlobalColor.blue))
        vertex.setPen(QPen(Qt.GlobalColor.black))
        vertex.setPos(QPointF(x, y))
        self.addItem(vertex)
        self.vertices[name] = vertex
        self.graph.add_node(name)
        print(f"Vértice '{name}' adicionado na posição ({x}, {y}).")

    def modify_vertex(self, old_name, new_name, x, y):
        if old_name not in self.vertices:
            print(f"Vértice '{old_name}' não encontrado.")
            return
        if new_name in self.vertices and new_name != old_name:
            print(f"Vértice '{new_name}' já existe.")
            return
        
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
        if name1 in self.vertices and name2 in self.vertices:
            vertice1 = self.vertices[name1]
            vertice2 = self.vertices[name2]
            line = QGraphicsLineItem(vertice1.x() + 15, vertice1.y() + 15, vertice2.x() + 15, vertice2.y() + 15)
            self.addItem(line)
            self.graph.add_edge(name1, name2)
            print(f"Aresta adicionada entre '{name1}' e '{name2}'.")
        else:
            print(f"Erro: Um ou ambos os vértices '{name1}' e '{name2}' não existem.")

# Classe principal da interface gráfica
class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = GraphScene()
        self.setScene(self.scene)

    def add_vertex(self, name, x, y):
        self.scene.add_vertex(name, x, y)

    def modify_vertex(self, old_name, new_name, x, y):
        self.scene.modify_vertex(old_name, new_name, x, y)

    def delete_vertex(self, name):
        self.scene.delete_vertex(name)

    def add_edge(self, name1, name2):
        self.scene.add_edge(name1, name2)

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
        # Adiciona um novo vértice: add (nome) (x) (y)
        if len(tokens) != 4:
            print("Comando inválido. Use: add (nome) (x) (y)")
            return
        try:
            name = tokens[1]
            x = float(tokens[2])
            y = float(tokens[3])
            graph_view.add_vertex(name, x, y)
        except ValueError:
            print("Coordenadas inválidas. Use números para x e y.")
    
    elif cmd == "modify":
        # Modifica um vértice existente: modify (nome_antigo) (novo_nome) (x) (y)
        if len(tokens) != 5:
            print("Comando inválido. Use: modify (nome_antigo) (novo_nome) (x) (y)")
            return
        try:
            old_name = tokens[1]
            new_name = tokens[2]
            x = float(tokens[3])
            y = float(tokens[4])
            graph_view.modify_vertex(old_name, new_name, x, y)
        except ValueError:
            print("Coordenadas inválidas. Use números para x e y.")
    
    elif cmd == "delete":
        # Exclui um vértice existente: delete (nome)
        if len(tokens) != 2:
            print("Comando inválido. Use: delete (nome)")
            return
        name = tokens[1]
        graph_view.delete_vertex(name)

    elif cmd == "connect":
        # Conecta dois vértices: connect (nome1) (nome2)
        if len(tokens) != 3:
            print("Comando inválido. Use: connect (nome1) (nome2)")
            return
        name1 = tokens[1]
        name2 = tokens[2]
        graph_view.add_edge(name1, name2)

    elif cmd == "show":
        # Exibe o grafo na interface gráfica
        graph_view.show_graph()

    elif cmd == "exit":
        # Sai da aplicação
        print("Saindo...")
        sys.exit()

    else:
        print(f"Comando desconhecido: {cmd}")

# Função principal
def main():
    # Inicializa a aplicação PyQt6
    app = QApplication(sys.argv)
    graph_view = GraphView()

    print("Bem-vindo ao gerenciador de grafos via terminal.")
    print("Comandos disponíveis:")
    print(" - add (nome) (x) (y): Adiciona um novo vértice com nome e coordenadas.")
    print(" - modify (nome_antigo) (novo_nome) (x) (y): Modifica um vértice existente.")
    print(" - delete (nome): Exclui um vértice e suas arestas.")
    print(" - connect (nome1) (nome2): Conecta dois vértices.")
    print(" - show: Mostra o grafo.")
    print(" - exit: Sai da aplicação.")
    
    while True:
        command = input("Comando: ")
        process_command(command, graph_view)

if __name__ == "__main__":
    main()
