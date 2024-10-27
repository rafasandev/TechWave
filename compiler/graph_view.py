from PyQt6.QtWidgets import QGraphicsView
from graph_scene import GraphScene

class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = GraphScene()  # Certifique-se de que GraphScene é uma subclasse de QGraphicsScene
        self.setScene(self.scene)  # Isso deve funcionar agora

    def add_vertex(self, name, category=None, position=None):
        self.scene.add_vertex(name, category, position)  # Remover relation

    def delete_edge(self, vertex1, vertex2):
        self.scene.delete_edge(vertex1, vertex2)

    def modify_vertex(self, old_id, new_name, new_category=None, position=None):
        self.scene.modify_vertex(old_id, new_name, new_category, position)

    def delete_vertex(self, id):
        self.scene.delete_vertex(id)

    def add_edge(self, id1, id2):
        self.scene.add_edge(id1, id2)

    def list_graph(self):
        self.scene.list_graph()