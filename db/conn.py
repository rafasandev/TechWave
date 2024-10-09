import sqlite3
import os 

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect('Vertices.db')

# Criar um cursor
cursor = conn.cursor()

# Criar a tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS Vertices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    posicao TEXT NOT NULL,
)
''')
# Criar a tabela de arestas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Arestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    custos REAL NOT NULL,
    vertices_id INTEGER,
    FOREIGN KEY (vertices_id) REFERENCES Vertices(id)
)
''')

# Salvar (commit) as alterações
conn.commit()

# Fechar a conexão
conn.close()

print("Banco de dados e tabela criados com sucesso!")
