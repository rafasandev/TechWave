<<<<<<< HEAD
print('cavalo')
=======
import sqlite3
import sys

def setup_database():
    conn = sqlite3.connect('arquivos.db')
    c = conn.cursor()

    # Cria uma tabela para armazenar arquivos binários com informações adicionais
    c.execute('''
    CREATE TABLE IF NOT EXISTS arquivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    caminho TEXT,
    conteudo BLOB
    )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados configurado com sucesso.")

# Definindo as palavras reservadas
PALAVRAS_RESERVADAS = {
    'add': 'Adicionar Arquivo',
    'modify': 'Modificar Arquivo',
    'delete': 'Excluir Arquivo',
    'retrieve': 'Recuperar Arquivo'
}

def conectar_db():
    return sqlite3.connect('arquivos.db')

def criar_tabela():
    conn = conectar_db()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS arquivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caminho TEXT UNIQUE,
    conteudo BLOB
    )
    ''')
    conn.commit()
    conn.close()

def analisar_comando(comando):
    palavras = comando.strip().split(maxsplit=2)

    if not palavras:
        print("Nenhum comando digitado.")   
        return

    palavra_chave = palavras[0]

    if palavra_chave in PALAVRAS_RESERVADAS:
        if palavra_chave == 'add':
            if len(palavras) < 3:
                print("Uso: add ")
            else:
                caminho = palavras[1]
                caminho_arquivo = palavras[2]
                add_arquivo(caminho, caminho_arquivo)

    elif palavra_chave == 'modify':
        if len(palavras) < 3:
            print("Uso: modify ")
        else:
            caminho = palavras[1]
            caminho_novo_arquivo = palavras[2]
            modify_arquivo(caminho, caminho_novo_arquivo)

    elif palavra_chave == 'delete':
        if len(palavras) < 2:
            print("Uso: delete ")
        else:
            caminho = palavras[1]
            delete_arquivo(caminho)

    elif palavra_chave == 'retrieve':
        if len(palavras) < 2:
            print("Uso: retrieve ")
        else:
            caminho = palavras[1]
            retrieve_arquivo(caminho)

    else:
        print(f"Comando não reconhecido: {palavra_chave}")

def add_arquivo(caminho, caminho_arquivo):
    try:
        with open(caminho_arquivo, 'rb') as file:
            conteudo = file.read()

            conn = conectar_db()
            c = conn.cursor()
            c.execute('INSERT INTO arquivos (caminho, conteudo) VALUES (?, ?)', (caminho, conteudo))
            conn.commit()
            print(f"Arquivo {caminho_arquivo} adicionado ao banco de dados como {caminho}.")
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar o arquivo: {e}")
    finally:
        conn.close()

def modify_arquivo(caminho, caminho_novo_arquivo):
    try:
        with open(caminho_novo_arquivo, 'rb') as file:
            novo_conteudo = file.read()

            conn = conectar_db()
            c = conn.cursor()
            c.execute('UPDATE arquivos SET conteudo = ? WHERE caminho = ?', (novo_conteudo, caminho))
            conn.commit()
            print(f"Arquivo {caminho} modificado com o novo conteúdo.")
    except Exception as e:
        print(f"Ocorreu um erro ao modificar o arquivo: {e}")
    finally:
        conn.close()

def delete_arquivo(caminho):
    try:
        conn = conectar_db()
        c = conn.cursor()
        c.execute('DELETE FROM arquivos WHERE caminho = ?', (caminho,))
        conn.commit()
        print(f"Arquivo {caminho} excluído do banco de dados.")
    except Exception as e:
        print(f"Ocorreu um erro ao excluir o arquivo: {e}")
    finally:
        conn.close()

def retrieve_arquivo(caminho):
    try:
        conn = conectar_db()
        c = conn.cursor()
        c.execute('SELECT conteudo FROM arquivos WHERE caminho = ?', (caminho,))
        resultado = c.fetchone()

        if resultado:
            conteudo = resultado[0]
            nome_arquivo = caminho.split('/')[-1] # Extrai o nome do arquivo
            with open(nome_arquivo, 'wb') as file:
                file.write(conteudo)
            print(f"Arquivo {caminho} recuperado e salvo como {nome_arquivo}.")
        else:
            print(f"O arquivo {caminho} não existe no banco de dados.")
    except Exception as e:
        print(f"Ocorreu um erro ao recuperar o arquivo: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    comando = input("Digite um comando: ")
    analisar_comando(comando)
>>>>>>> e9a2f2dc364a4346e9f09dfae417377457ac508c
