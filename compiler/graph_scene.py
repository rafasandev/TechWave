import networkx as nx
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QPointF
import secrets
import sqlite3
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, id, name, category, position):
        self.id = id
        self.name = name
        self.category = category
        self.position = position
        self.children = []

class GraphScene(QGraphicsScene):
    def __init__(self, db_filename='graph.db'):
        super().__init__()
        self.vertices = {}
        self.edges = []

        # Conectando ao banco de dados SQLite
        self.conn = sqlite3.connect(db_filename)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS vertices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT,
                    position TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name1 TEXT NOT NULL,
                    name2 TEXT NOT NULL
                )
            ''')

    def add_vertex(self, name, category=None, position=None):
        if position is None:
            position = (secrets.randbelow(800), secrets.randbelow(600))
        
        cursor = self.conn.cursor()
        # Verifica se o vértice já existe
        cursor.execute("SELECT id FROM vertices WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Vértice '{name}' já existe.")
            cursor.close()
            return
        
        try:
            with self.conn:
                cursor = self.conn.execute(
                    'INSERT INTO vertices (name, category, position) VALUES (?, ?, ?)',
                    (name, category, f"{position}")
                )
                new_id = cursor.lastrowid

            self.vertices[new_id] = {
                'id': new_id,
                'name': name,
                'category': category,
                'position': position,
            }

            self.draw_vertex(new_id, name, position)
            print(f"Vértice '{name}' adicionado com sucesso.")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao adicionar vértice: {e}")
        finally:
            cursor.close()


    def draw_vertex(self, vertex_id, name, position):
        x, y = position
        ellipse = QGraphicsEllipseItem(x - 15, y - 15, 30, 30)
        ellipse.setBrush(QBrush(QColor(255, 255, 0)))
        self.addItem(ellipse)

        text_item = self.addText(name)
        text_item.setPos(QPointF(x - 15, y - 15))

    def modify_vertex(self, old_name, new_name, new_category=None, new_position=None):
        """Modifica as propriedades de um vértice existente no banco de dados."""
        cursor = self.conn.cursor()

        # Verifica se o vértice antigo existe
        cursor.execute("SELECT id FROM vertices WHERE name = ?", (old_name,))
        result = cursor.fetchone()

        if not result:
            print(f"Erro: O vértice '{old_name}' não existe no banco de dados.")
            cursor.close()
            return

        vertex_id = result[0]

        # Prepara a atualização
        update_query = "UPDATE vertices SET name = ?"
        parameters = [new_name if new_name else old_name]

        if new_category:
            update_query += ", category = ?"
            parameters.append(new_category)

        if new_position:
            update_query += ", position = ?"
            parameters.append(new_position)

        update_query += " WHERE id = ?"
        parameters.append(vertex_id)

        # Executa a atualização
        cursor.execute(update_query, parameters)
        self.conn.commit()

        # Atualiza a lista local de vértices se o nome foi alterado
        if new_name and old_name != new_name:
            self.vertices.remove(old_name)
            self.vertices.add(new_name)

        print(f"Vértice '{old_name}' modificado com sucesso.")
        cursor.close()


    def delete_edge(self, vertex1, vertex2):  
        """Remove uma aresta específica entre dois vértices."""
        cursor = self.conn.cursor()
        
        # Deleta a aresta do banco de dados
        cursor.execute('DELETE FROM edges WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)',
                       (vertex1, vertex2, vertex2, vertex1))
        self.conn.commit()

        # Remove a aresta da lista local
        self.edges = [edge for edge in self.edges if not (edge[0] == vertex1 and edge[1] == vertex2) and not (edge[0] == vertex2 and edge[1] == vertex1)]

        # Atualiza a cena gráfica para remover a linha associada (se for implementado graficamente)
        self.update_graphics()

        print(f"Aresta entre '{vertex1}' e '{vertex2}' removida.")
        cursor.close()

    def list_graph(self):
        cursor = self.conn.cursor()
        
        print("Lista de Vértices:")
        cursor.execute('SELECT * FROM vertices')
        for row in cursor.fetchall():
            id, name, category, position = row
            print(f"ID: {id}, Nome: {name}, Categoria: {category}, Posição: {position}")

        print("\nLista de Arestas:")
        cursor.execute('SELECT name1, name2 FROM edges')
        for edge in cursor.fetchall():
            print(f"Aresta entre {edge[0]} e {edge[1]}")

        cursor.close()

    def close(self):
        self.conn.close()

    def delete_vertex(self, identifier):
        cursor = self.conn.cursor()
        
        # Tenta apagar pelo ID
        cursor.execute('SELECT * FROM vertices WHERE id = ?', (identifier,))
        vertex = cursor.fetchone()
        
        if vertex:
            # Remove o vértice do banco de dados
            cursor.execute('DELETE FROM vertices WHERE id = ?', (identifier,))
            self.conn.commit()
            print(f"Vértice com ID {identifier} removido.")
        else:
            # Tenta apagar pelo nome se não encontrar pelo ID
            cursor.execute('SELECT * FROM vertices WHERE name = ?', (identifier,))
            vertex = cursor.fetchone()
            
            if vertex:
                # Remove o vértice do banco de dados
                cursor.execute('DELETE FROM vertices WHERE name = ?', (identifier,))
                self.conn.commit()
                print(f"Vértice com nome '{identifier}' removido.")
            else:
                print(f"Nenhum vértice encontrado com ID ou nome '{identifier}'.")

        cursor.close()

    def add_edge(self, vertex1, vertex2):
        """Adiciona uma aresta entre dois vértices, verificando se já existe uma conexão entre eles (em ambas as direções)."""
        cursor = self.conn.cursor()

        # Verifica se o vertex1 existe na tabela vertices e recupera a posição como string
        cursor.execute("SELECT id, position FROM vertices WHERE name = ?", (vertex1,))
        result1 = cursor.fetchone()

        # Verifica se o vertex2 existe na tabela vertices e recupera a posição como string
        cursor.execute("SELECT id, position FROM vertices WHERE name = ?", (vertex2,))
        result2 = cursor.fetchone()

        if not result1 or not result2:
            print(f"Erro: Um ou ambos os vértices '{vertex1}' e '{vertex2}' não existem no banco de dados.")
            cursor.close()
            return

        # Extrai os IDs e posições dos vértices a partir do resultado das consultas
        id1, pos1_str = result1
        id2, pos2_str = result2

        # Verifica se já existe uma aresta entre vertex1 e vertex2 (em qualquer direção)
        cursor.execute('''
            SELECT * FROM edges 
            WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)
        ''', (vertex1, vertex2, vertex2, vertex1))
        
        existing_edge = cursor.fetchone()
        
        if existing_edge:
            print(f"Erro: A aresta entre '{vertex1}' e '{vertex2}' já existe.")
            cursor.close()
            return

        # Converte a string de posição em uma tupla (x, y)
        pos1 = eval(pos1_str)  # Transforma "(x, y)" em (x, y)
        pos2 = eval(pos2_str)  # Transforma "(x, y)" em (x, y)

        # Adiciona a aresta na tabela edges
        cursor.execute("INSERT INTO edges (name1, name2) VALUES (?, ?)", (vertex1, vertex2))
        self.conn.commit()

        # Adiciona a aresta na lista local de arestas
        self.edges.append((vertex1, vertex2))

        # Atualiza a visualização gráfica
        self.addLine(pos1[0], pos1[1], pos2[0], pos2[1])  # Desenha uma linha para representar a aresta

        print(f"Aresta conectada entre '{vertex1}' e '{vertex2}'.")
        cursor.close()

        # Desenha as arestas novamente
        for edge in self.edges:
            vertex1, vertex2 = edge
            if vertex1 in self.vertices and vertex2 in self.vertices:
                pos1 = self.vertices[vertex1]['position']
                pos2 = self.vertices[vertex2]['position']
                self.addLine(pos1.x(), pos1.y(), pos2.x(), pos2.y())  # Desenha uma linha para representar a aresta

    def update_graphics(self):
        """Redesenha os itens gráficos na cena, removendo e redesenhando arestas."""
        # Limpa todas as linhas (arestas) da cena
        for item in self.items():
            if isinstance(item, QGraphicsLineItem):
                self.removeItem(item)

        # Desenha todas as arestas novamente
        for edge in self.edges:
            vertex1, vertex2 = edge
            if vertex1 in self.vertices and vertex2 in self.vertices:
                pos1 = self.vertices[vertex1]['position']
                pos2 = self.vertices[vertex2]['position']
                self.addLine(pos1[0], pos1[1], pos2[0], pos2[1])  # Desenha uma linha para representar a aresta
