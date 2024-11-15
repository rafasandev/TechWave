import sys
from PyQt6.QtWidgets import QApplication
from .graph_view import GraphView
from .graph_scene import *


def process_command(command, graph_view):
    tokens = command.split()
    if not tokens:
        return

    cmd = tokens[0].lower()
    cmd_parts = command.split()
    cmd = cmd_parts[0]

    if cmd == "add":
        if len(tokens) < 2:
            return "Erro: Comando incompleto. Use: add (nome) [categoria] [valor]"
        name = tokens[1]
        category = tokens[2] if len(tokens) > 2 else None
        custo = tokens[3] if len(tokens) > 3 else 0
        return graph_view.add_vertex(name, category, custo)

    elif cmd == "md":
        if len(tokens) < 3:
            return "Erro: Comando incompleto. Use: md (id) (novo_nome) [nova_categoria] [novo_custo]"
        try:
            old_id = int(tokens[1])  # ID deve ser um inteiro
        except ValueError:
            return "Erro: ID deve ser um número inteiro."
        new_name = tokens[2]
        new_category = tokens[3] if len(tokens) > 3 else None
        custo = tokens[4] if len(tokens) > 4 else None
        return graph_view.modify_vertex(old_id, new_name, new_category, custo)

    elif cmd == "del":
        identifier = tokens[1] if len(tokens) > 1 else None
        if identifier:
            return graph_view.delete_vertice(identifier)
        else:
            return "Erro: Comando incompleto. Use: delete (id/nome)"

    elif cmd == "del_aresta":
        if len(tokens) < 3:
            return "Erro: Comando incompleto. Use: del_aresta (nome1) (nome2)"
        vertex1 = tokens[1]
        vertex2 = tokens[2]
        return graph_view.delete_aresta(
            vertex1, vertex2
        )  # Chama delete_aresta para excluir a aresta específica

    elif cmd == "connect":
        if len(tokens) != 3:
            return "Comando inválido. Use: connect (id/nome1) (id/nome2)"
        vertex1 = tokens[1]
        vertex2 = tokens[2]
        return graph_view.add_aresta(vertex1, vertex2)

    elif cmd == "list":
        return graph_view.list_graph()

    elif cmd == "cd":
        if (
            len(tokens) == 4
        ):  # Se houver 4 tokens (nome_vertice, nome_arquivo, caminho_arquivo)
            name_vertice = tokens[1]  # Nome do vértice
            name_arquivo = tokens[2]  # Nome do arquivo
            caminho_arquivo = tokens[3]  # Caminho do arquivo

            # Verifica se o caminho do arquivo é válido
            if os.path.exists(caminho_arquivo):
                # Se o caminho do arquivo existir, chama a função para associar o arquivo ao vértice
                return graph_view.cd_vertice(
                    name_vertice, name_arquivo, caminho_arquivo
                )
            else:
                return f"Erro: O caminho do arquivo '{caminho_arquivo}' não existe."
        elif (
            len(tokens) == 3
        ):  # Caso o usuário não forneça um caminho de arquivo, mas sim um conteúdo
            name_vertice = tokens[1]  # Nome do vértice
            name_arquivo = tokens[2]  # Nome do arquivo

            # Pergunta para o usuário o conteúdo do arquivo
            texto = input("Digite o conteúdo do arquivo:\n")

            # Chama a função para associar o conteúdo diretamente ao vértice
            return graph_view.cd_vertice(name_vertice, name_arquivo, texto=texto)
        else:
            return "Comando 'cd' inválido. Use: cd <nome_vertice> <nome_arquivo> <caminho_arquivo> ou <conteudo_arquivo>"

    elif cmd == "view":
        if len(tokens) == 2:  # Alterado para tokens
            identifier = tokens[1]  # Alterado para tokens
            try:
                # Tenta converter para int para identificar se é um ID
                identifier = int(identifier)
            except ValueError:
                pass  # Se falhar, permanece como string para buscar pelo nome
            return graph_view.view(identifier)
        else:
            return "Comando 'view' inválido. Use: view <nome_ou_id>"

    elif cmd == "view":
        if (
            len(tokens) == 2
        ):  # Se houver 2 tokens, o primeiro é o comando, o segundo o identificador
            identifier = tokens[
                1
            ]  # O identificador pode ser nome de vértice ou nome de arquivo

            cursor = (
                graph_view.conn.cursor()
            )  # Abre o cursor para realizar a consulta SQL

            # Primeira busca: verifica se o identificador é um name_vertice
            cursor.execute(
                "SELECT COUNT(*) FROM arquivos WHERE name_vertice = ?", (identifier,)
            )
            result = cursor.fetchone()

            if result[0] > 0:
                # Se encontrado como name_vertice, chama a função para exibir os arquivos associados ao vértice
                return graph_view.view_vertice(identifier)
            else:
                # Segunda busca: verifica se o identificador é um name_arquivo
                cursor.execute(
                    "SELECT COUNT(*) FROM arquivos WHERE name_arquivo = ?",
                    (identifier,),
                )
                result = cursor.fetchone()

                if result[0] > 0:
                    # Se encontrado como name_arquivo, chama a função para exibir o conteúdo do arquivo
                    return graph_view.view_arquivo(identifier)
                else:
                    # Se não encontrar nenhum dos dois, exibe a mensagem de erro
                    return f"Não foi possível encontrar nenhum vértice ou arquivo com o identificador '{identifier}'."

            cursor.close()  # Fecha o cursor após a execução da consulta

        else:
            return "Comando 'view' inválido. Use: view <nome_vertice ou nome_arquivo>"

    elif cmd == "del_cd":
        if len(tokens) < 2:
            return "Erro: Comando incompleto. Use: del_cd <nome_arquivo>"
        nome_arquivo = tokens[1]  # Nome do vértice fornecido pelo usuário
        # Chama o método delete_arquivo da instância de GraphView
        if graph_view.delete_arquivo(nome_arquivo):
            return f"Arquivo associado ao vértice '{nome_arquivo}' excluído com sucesso."  # Mensagem de sucess
        else:
            return f"Erro ao excluir o arquivo associado ao vértice '{nome_arquivo}'."  # Mensagem de err

    elif cmd == "modify_cd":
        if len(tokens) < 3:
            return (
                "Erro: Comando incompleto. Use: modify_cd (id/nome) (novo_conteudo_txt)"
            )

        identifier = tokens[1]  # ID ou nome do vértice
        new_txt = " ".join(tokens[2:])  # O conteúdo do arquivo a ser atualizado

        try:
            # Tenta converter o identificador para int (ID)
            identifier = int(identifier)
        except ValueError:
            pass  # Se não for um número, mantemos como nome do vértice

        if graph_view.modify_cd(identifier, new_txt):
            return f"Conteúdo do arquivo associado ao vértice '{identifier}' atualizado com sucesso."
        else:
            return f"Erro ao excluir o arquivo associado ao vértice '{identifier}'."

    elif cmd == "exit":
        return f"Erro ao atualizar o conteúdo do arquivo associado ao vértice '{identifier}'."

    elif cmd == "exit":
        sys.exit()

    else:
        return "Comando não encontrado. Digite novamente"


import sqlite3  # Usando SQLite como exemplo


def main():
    app = QApplication(sys.argv)

    # Criação da conexão com o banco de dados
    conn = sqlite3.connect(
        "graph.db"
    )  # Substitua pelo caminho correto do seu banco de dados

    # Passa a conexão para o GraphView
    graph_view = GraphView(conn)  # Agora você passa a conexão para o GraphView

    while True:
        command = input(
            "Digite um comando (add, modify, del, connect, list, del_aresta, cd exit): "
        )
        if command.lower() == "exit":
            break
        process_command(command, graph_view)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
