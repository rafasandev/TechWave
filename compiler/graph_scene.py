import networkx as nx
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QPointF
import sqlite3
import matplotlib.pyplot as plt
import os


class Vertice:
    def __init__(self, id, name, category, custo):
        self.id = id
        self.name = name
        self.category = category
        self.custo = custo
        self.children = []


class GraphScene(QGraphicsScene):
    def __init__(self, db_filename="graph.db"):
        super().__init__()
        self.vertices = {}
        self.arestas = []

        # Conectando ao banco de dados SQLite
        self.conn = sqlite3.connect(db_filename)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS vertices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT,
                    custo TEXT
                )
            """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS arestas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name1 TEXT NOT NULL,
                    name2 TEXT NOT NULL
                )
            """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS arquivos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_arquivo TEXT NOT NULL,
                    name_vertice TEXT NOT NULL,
                    txt BLOB
                )
            """
            )

    def add_vertex(self, name, category=None, custo=None):

        cursor = self.conn.cursor()
        # Verifica se o vértice já existe
        cursor.execute("SELECT id FROM vertices WHERE name = ?", (name,))
        if cursor.fetchone():
            cursor.close()
            return f"Vértice '{name}' já existe."

        try:
            with self.conn:
                cursor = self.conn.execute(
                    "INSERT INTO vertices (name, category, custo) VALUES (?, ?, ?)",
                    (name, category, f"{custo}"),
                )
                new_id = cursor.lastrowid

            self.vertices[new_id] = {
                "id": new_id,
                "name": name,
                "category": category,
                "custo": custo,
            }

            return f"Vértice '{name}' adicionado com sucesso."
        except sqlite3.IntegrityError as e:
            return f"Erro ao adicionar vértice: {e}"
        finally:
            cursor.close()

    def modify_vertice(self, old_name, new_name, new_category=None, new_custo=None):
        """Modifica as propriedades de um vértice existente no banco de dados."""
        cursor = self.conn.cursor()

        # Verifica se o vértice antigo existe
        cursor.execute("SELECT id FROM vertices WHERE name = ?", (old_name,))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            return f"Erro: O vértice '{old_name}' não existe no banco de dados."
        vertex_id = result[0]

        # Prepara a atualização
        update_query = "UPDATE vertices SET name = ?"
        parameters = [new_name if new_name else old_name]

        if new_category:
            update_query += ", category = ?"
            parameters.append(new_category)

        if new_custo:
            update_query += ", custo = ?"
            parameters.append(new_custo)

        update_query += " WHERE id = ?"
        parameters.append(vertex_id)

        # Executa a atualização
        cursor.execute(update_query, parameters)
        self.conn.commit()

        # Atualiza a lista local de vértices se o nome foi alterado
        if new_name and old_name != new_name:
            self.vertices.remove(old_name)
            self.vertices.add(new_name)

        cursor.close()
        return f"Vértice '{old_name}' modificado com sucesso."

    def delete_aresta(self, vertex1, vertex2):
        """Remove uma aresta específica entre dois vértices."""
        cursor = self.conn.cursor()

        # Deleta a aresta do banco de dados
        cursor.execute(
            "DELETE FROM arestas WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)",
            (vertex1, vertex2, vertex2, vertex1),
        )
        self.conn.commit()

        # Remove a aresta da lista local
        self.arestas = [
            aresta
            for aresta in self.arestas
            if not (aresta[0] == vertex1 and aresta[1] == vertex2)
            and not (aresta[0] == vertex2 and aresta[1] == vertex1)
        ]

        cursor.close()
        return f"Aresta entre '{vertex1}' e '{vertex2}' removida."

    def list_graph(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM vertices")
        for row in cursor.fetchall():
            id, name, category, custo = row
            return f"ID: {id}, Nome: {name}, Categoria: {category}, custo: {custo}"

        cursor.execute("SELECT name1, name2 FROM arestas")

        for aresta in cursor.fetchall():
            return f"Aresta entre {aresta[0]} e {aresta[1]}"

        cursor.close()

        return cursor.fetchall()

    def close(self):
        self.conn.close()

    def delete_vertice(self, identifier):
        cursor = self.conn.cursor()
        if identifier == int:
            # Tenta apagar pelo ID
            cursor.execute("SELECT * FROM vertices WHERE id = ?", (identifier,))
            vertice = cursor.fetchone()

            if vertice:
                # Remove o vértice do banco de dados
                cursor.execute("DELETE FROM vertices WHERE id = ?", (identifier,))
                self.conn.commit()
                return f"Vértice com ID {identifier} removido."
            else:
                # Tenta apagar pelo nome se não encontrar pelo ID
                cursor.execute("SELECT * FROM vertices WHERE name = ?", (identifier,))
                vertex = cursor.fetchone()

                if vertice:
                    # Remove o vértice do banco de dados
                    cursor.execute("DELETE FROM vertices WHERE name = ?", (identifier,))
                    self.conn.commit()
                    return f"Vértice com nome '{identifier}' removido."
                else:
                    return f"Nenhum vértice encontrado com ID ou nome '{identifier}'."
        else:
            cursor.execute("SELECT * FROM vertices WHERE name = ?", (identifier,))
            vertice = cursor.fetchone()

            if vertice:
                # Remove o vértice do banco de dados
                cursor.execute("DELETE FROM vertices WHERE name = ?", (identifier,))
                self.conn.commit()
                return f"Vértice com ID {identifier} removido."
            else:
                # Tenta apagar pelo nome se não encontrar pelo ID
                cursor.execute("SELECT * FROM vertices WHERE name = ?", (identifier,))
                vertex = cursor.fetchone()

                if vertice:
                    # Remove o vértice do banco de dados
                    cursor.execute("DELETE FROM vertices WHERE name = ?", (identifier,))
                    self.conn.commit()
                    return f"Vértice com nome '{identifier}' removido."
                else:
                    return f"Nenhum vértice encontrado com ID ou nome '{identifier}'."

        cursor.close()

    def add_aresta(self, vertex1, vertex2):
        """Adiciona uma aresta entre dois vértices, verificando se já existe uma conexão entre eles (em ambas as direções)."""
        cursor = self.conn.cursor()

        # Verifica se o vertex1 existe na tabela vertices e recupera a posição como string
        cursor.execute("SELECT id, custo FROM vertices WHERE name = ?", (vertex1,))
        result1 = cursor.fetchone()

        # Verifica se o vertex2 existe na tabela vertices e recupera a posição como string
        cursor.execute("SELECT id, custo FROM vertices WHERE name = ?", (vertex2,))
        result2 = cursor.fetchone()

        if not result1 or not result2:
            cursor.close()
            return f"Erro: Um ou ambos os vértices '{vertex1}' e '{vertex2}' não existem no banco de dados."

        # Extrai os IDs e posições dos vértices a partir do resultado das consultas
        id1, pos1_str = result1
        id2, pos2_str = result2

        # Verifica se já existe uma aresta entre vertex1 e vertex2 (em qualquer direção)
        cursor.execute(
            """
            SELECT * FROM arestas 
            WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)
        """,
            (vertex1, vertex2, vertex2, vertex1),
        )

        existing_edge = cursor.fetchone()

        if existing_edge:
            return f"Erro: A aresta entre '{vertex1}' e '{vertex2}' já existe."
            cursor.close()
            return f"Erro: A aresta entre '{vertex1}' e '{vertex2}' já existe."

        # Adiciona a aresta na tabela edges
        cursor.execute(
            "INSERT INTO arestas (name1, name2) VALUES (?, ?)", (vertex1, vertex2)
        )
        self.conn.commit()

        # Adiciona a aresta na lista local de arestas
        self.arestas.append((vertex1, vertex2))

        cursor.close()
        return f"Aresta conectada entre '{vertex1}' e '{vertex2}'."

        def inserir_arquivo_txt(self, name_vertice, name_arquivo, caminho_arquivo):
            """Insere o conteúdo de um arquivo .txt na tabela arquivos associado ao name_vertice."""
            try:
                # Verifica se o caminho do arquivo existe
                if not os.path.exists(caminho_arquivo):
                    return f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado."
                    return

                # Abre o arquivo .txt no modo de leitura
                with open(caminho_arquivo, "r", encoding="utf-8") as file:
                    arquivo = file.read()  # Lê todo o conteúdo do arquivo

                cursor = self.conn.cursor()

                # Insere o conteúdo do arquivo no banco de dados
                cursor.execute(
                    """
                    INSERT INTO arquivos (name_vertice, name_arquivo, txt)
                    VALUES (?, ?, ?)
                """,
                    (name_vertice, name_arquivo, arquivo),
                )

                self.conn.commit()  # Confirma a transação para salvar as alterações
                return f"Arquivo '{name_arquivo}' armazenado com sucesso para o vértice '{name_vertice}'."
                cursor.close()

            except Exception as e:
                return f"Erro ao inserir arquivo .txt: {e}"

        def inserir_texto_arquivo(self, name_vertice, name_arquivo, texto):
            """Insere o conteúdo do texto na tabela arquivos associado ao name_vertice."""
            try:
                cursor = self.conn.cursor()

                # Insere o conteúdo do texto no banco de dados
                cursor.execute(
                    """
                    INSERT INTO arquivos (name_vertice, name_arquivo, txt)
                    VALUES (?, ?, ?)
                """,
                    (name_vertice, name_arquivo, texto),
                )

                self.conn.commit()  # Confirma a transação para salvar as alterações
                return f"Conteúdo do arquivo '{name_arquivo}' armazenado com sucesso para o vértice '{name_vertice}'."
                cursor.close()

            except Exception as e:
                return f"Erro ao inserir texto no arquivo: {e}"

    def view_arquivo(self, name_arquivo):
        """Exibe o conteúdo de um arquivo específico."""
        cursor = self.conn.cursor()

        # Consulta o conteúdo do arquivo baseado no nome do arquivo
        cursor.execute(
            "SELECT txt FROM arquivos WHERE name_arquivo = ?", (name_arquivo,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]  # Exibe o conteúdo do arquiv
        else:
            return f"Erro: Arquivo '{name_arquivo}' não encontrado."
        cursor.close()

    def view_vertice(self, name_vertice):
        """Exibe todos os arquivos associados ao vértice."""
        cursor = self.conn.cursor()

        # Consulta os arquivos relacionados ao vértice pelo nome
        cursor.execute(
            "SELECT name_arquivo FROM arquivos WHERE name_vertice = ?", (name_vertice,)
        )

        files = cursor.fetchall()

        if files:
            for file in files:
                return file[0]  # Exibe apenas o nome do arquiv
        else:
            return f"Erro: Nenhum arquivo encontrado para o vértice '{name_vertice}'."
        cursor.close()
