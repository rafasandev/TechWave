from PyQt6.QtWidgets import QGraphicsView
from graph_scene import GraphScene

class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = GraphScene()  # Certifique-se de que GraphScene é uma subclasse de QGraphicsScene
        self.setScene(self.scene)  # Isso deve funcionar agora
        self.vertices = {}  # Inicializa um dicionário para armazenar os vértices

    def add_vertex(self, name, category=None, custo=None):
        self.scene.add_vertex(name, category, custo)
        self.vertices[name] = {'category': category, 'custo': custo}  # Adiciona ao dicionário de vértices

    def delete_aresta(self, vertex1, vertex2):
        self.scene.delete_aresta(vertex1, vertex2)

    def modify_vertice(self, old_id, new_name, new_category=None, custo=None):
        self.scene.modify_vertex(old_id, new_name, new_category, custo)
        if old_id in self.vertices:
            self.vertices[new_name] = self.vertices.pop(old_id)  # Atualiza o dicionário de vértices

    def delete_vertice(self, id):
        self.scene.delete_vertice(id)
        if id in self.vertices:
            del self.vertices[id]  # Remove do dicionário de vértices

    def add_aresta(self, id1, id2):
        self.scene.add_aresta(id1, id2)

    def list_graph(self):
        self.scene.list_graph()

    def cd_vertice(self, name, caminho):
        self.scene.inserir_arquivo_txt(name, caminho)
    
    def view(self, identifier):
        conteudo = self.scene.view_arquivo_txt(identifier)
        if conteudo:
            print("Conteúdo do arquivo:")
            print(conteudo)
        else:
            print("Arquivo não encontrado para o identificador fornecido.")

    def delete_arquivo(self, identifier):
        if identifier in self.vertices:  # Verifica se o vértice existe
            del self.vertices[identifier]  # Exclui o vértice
            print(f"Arquivo '{identifier}' excluído com sucesso.")
        else:
            print(f"Erro: Arquivo '{identifier}' não encontrado.")
