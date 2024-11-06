from PyQt6.QtWidgets import QGraphicsView
from graph_scene import GraphScene

class GraphView(QGraphicsView):
    def __init__(self, conn):
        super().__init__()
        self.scene = GraphScene()  # Certifique-se de que GraphScene é uma subclasse de QGraphicsScene
        self.setScene(self.scene)  # Isso deve funcionar agora
        self.vertices = {}  # Inicializa um dicionário para armazenar os vértices
        self.conn = conn  # Atribui a conexão à instância de GraphView


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

    def cd_vertice(self, name_vertice, name_arquivo, caminho_arquivo=None, texto=None):
        """Insere ou atualiza o arquivo associado ao vértice."""
        if caminho_arquivo:  # Se o caminho do arquivo foi fornecido
            # Chama a função para inserir o conteúdo do arquivo
            self.scene.inserir_arquivo_txt(name_vertice, name_arquivo, caminho_arquivo)
        elif texto:  # Se o texto foi fornecido diretamente
            # Chama a função para inserir o texto diretamente
            self.scene.inserir_texto_arquivo(name_vertice, name_arquivo, texto)
        else:
            print("Erro: Nenhum caminho de arquivo ou texto fornecido.")

    def view_arquivo(self, name_arquivo):
        """Exibe o conteúdo de um arquivo específico."""
        cursor = self.conn.cursor()

        # Consulta o conteúdo do arquivo baseado no nome do arquivo
        cursor.execute('SELECT txt FROM arquivos WHERE name_arquivo = ?', (name_arquivo,))

        result = cursor.fetchone()

        if result:
            print(f"Conteúdo do arquivo '{name_arquivo}':")
            print(result[0])  # Exibe o conteúdo do arquivo
        else:
            print(f"Erro: Arquivo '{name_arquivo}' não encontrado.")

        cursor.close()

    def view_vertice(self, name_vertice):
        """Exibe todos os arquivos associados ao vértice."""
        cursor = self.conn.cursor()

        # Consulta os arquivos relacionados ao vértice pelo nome
        cursor.execute('SELECT name_arquivo FROM arquivos WHERE name_vertice = ?', (name_vertice,))

        files = cursor.fetchall()

        if files:
            print(f"Arquivos associados ao vértice '{name_vertice}':")
            for file in files:
                print(file[0])  # Exibe apenas o nome do arquivo
        else:
            print(f"Erro: Nenhum arquivo encontrado para o vértice '{name_vertice}'.")

        cursor.close()


    def delete_arquivo(self, identifier):
        """Excluir o arquivo associado ao vértice (por nome ou ID)."""
        cursor = self.conn.cursor()  # Cria um cursor para interagir com o banco de dados

        # Se o identificador for um número (ID), consulta por ID
        if isinstance(identifier, int):
            query = "SELECT id FROM arquivos WHERE id = ?"
            cursor.execute(query, (identifier,))
        else:
            # Caso contrário, consulta pelo nome do vértice
            query = "SELECT id FROM arquivos WHERE name_arquivo = ?"
            cursor.execute(query, (identifier,))

        # Verifica se encontrou o arquivo correspondente
        result = cursor.fetchone()

        if result:
            # Se encontrou o arquivo, procede com a exclusão
            delete_query = "DELETE FROM arquivos WHERE id = ?"
            if isinstance(identifier, int):
                cursor.execute(delete_query, (identifier,))
            else:
                cursor.execute(delete_query, (result[0],))  # Usa o ID do vértice para exclusão

            self.conn.commit()  # Confirma a transação
            cursor.close()
            return True
        else:
            # Caso o arquivo não seja encontrado
            print(f"Erro: Arquivo não encontrado para o vértice '{identifier}'.")
            cursor.close()
            return False

    def modify_cd(self, identifier, new_txt):
        """Modifica o conteúdo do arquivo associado ao vértice."""
        cursor = self.conn.cursor()  # Cria um cursor para interagir com o banco de dados

        # Se o identificador for um número (ID), consulta por ID
        if isinstance(identifier, int):
            query = "SELECT id FROM arquivos WHERE id = ?"
            cursor.execute(query, (identifier,))
        else:
            query = "SELECT id FROM arquivos WHERE name_arquivo = ?"
            cursor.execute(query, (identifier,))

        # Verifica se encontrou o arquivo correspondente
        result = cursor.fetchone()

        if result:
            # Se encontrou o arquivo, procede com a atualização do conteúdo
            update_query = "UPDATE arquivos SET txt = ? WHERE id = ?"
            if isinstance(identifier, int):
                cursor.execute(update_query, (new_txt, identifier))
            else:
                cursor.execute(update_query, (new_txt, result[0]))  # Usa o ID encontrado para atualizar

            self.conn.commit()  # Confirma a transação
            print(f"Conteúdo do arquivo associado ao vértice '{identifier}' atualizado com sucesso.")
            cursor.close()
            return True
        else:
            # Caso o arquivo não seja encontrado
            print(f"Erro: Arquivo não encontrado para o vértice '{identifier}'.")
            cursor.close()
            return False
