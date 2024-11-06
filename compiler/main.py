import sys
from PyQt6.QtWidgets import QApplication
from .graph_view import GraphView


def process_command(command, graph_view):
    tokens = command.split()
    if not tokens:
        return

    cmd = tokens[0].lower()
    cmd_parts = command.split()
    cmd = cmd_parts[0]

    if cmd == "add":
        if len(tokens) < 2:
            print("Erro: Comando incompleto. Use: add (nome) [categoria] [posição]")
            return
        name = tokens[1]
        category = tokens[2] if len(tokens) > 2 else None
        custo = tokens[3] if len(tokens) > 3 else 0
        graph_view.add_vertex(name, category, custo)

    elif cmd == "md":
        if len(tokens) < 3:
            print(
                "Erro: Comando incompleto. Use: md (id) (novo_nome) [nova_categoria] [novo_custo]"
            )
            return
        try:
            old_id = int(tokens[1])  # ID deve ser um inteiro
        except ValueError:
            print("Erro: ID deve ser um número inteiro.")
            return
        new_name = tokens[2]
        new_category = tokens[3] if len(tokens) > 3 else None
        custo = tokens[4] if len(tokens) > 4 else None
        graph_view.modify_vertex(old_id, new_name, new_category, custo)

    elif cmd == "del":
        identifier = tokens[1] if len(tokens) > 1 else None
        if identifier:
            graph_view.delete_vertice(identifier)
        else:
            print("Erro: Comando incompleto. Use: delete (id/nome)")

    elif cmd == "del a":
        if len(tokens) < 3:
            print("Erro: Comando incompleto. Use: del_aresta (nome1) (nome2)")
            return
        vertex1 = tokens[1]
        vertex2 = tokens[2]
        graph_view.delete_aresta(
            vertex1, vertex2
        )  # Chama delete_aresta para excluir a aresta específica

    elif cmd == "connect":
        if len(tokens) != 3:
            print("Comando inválido. Use: connect (id/nome1) (id/nome2)")
            return
        vertex1 = tokens[1]
        vertex2 = tokens[2]
        graph_view.add_aresta(vertex1, vertex2)

    elif cmd == "list":
        graph_view.list_graph()

    elif cmd == "cd":
        if len(tokens) == 3:  # Alterado para tokens
            name_vertice = tokens[1]  # Alterado para tokens
            caminho_arquivo = tokens[2]  # Alterado para tokens
            # Passa os dois argumentos para cd_vertice
            graph_view.cd_vertice(name_vertice, caminho_arquivo)
        else:
            print("Comando 'cd' inválido. Use: cd <nome_vertice> <caminho_arquivo>")

    if cmd == "view":
        if len(tokens) == 2:  # Alterado para tokens
            identifier = tokens[1]  # Alterado para tokens
            try:
                # Tenta converter para int para identificar se é um ID
                identifier = int(identifier)
            except ValueError:
                pass  # Se falhar, permanece como string para buscar pelo nome
            graph_view.view(identifier)
        else:
            print("Comando 'view' inválido. Use: view <nome_ou_id>")

    elif cmd == "del_cd":
        identifier = tokens[1]  # Aqui você quis usar 'tokens', não 'parts'
        if graph_view.delete_arquivo(
            identifier
        ):  # Chama a função de exclusão do arquivo
            print(
                f"Arquivo associado ao vértice '{identifier}' excluído com sucesso."
            )  # Mensagem de sucesso
        else:
            print(f"Erro ao excluir o arquivo associado ao vértice '{identifier}'.")

    elif cmd == "exit":
        sys.exit()


def main():
    app = QApplication(sys.argv)
    graph_view = GraphView()

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
