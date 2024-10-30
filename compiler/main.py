import sys
from PyQt6.QtWidgets import QApplication
from graph_view import GraphView

def process_command(command, graph_view):
    tokens = command.split()
    if not tokens:
        return

    cmd = tokens[0].lower()

    if cmd == "add":
        if len(tokens) < 2:
            print("Erro: Comando incompleto. Use: add (nome) [categoria] [posição]")
            return
        name = tokens[1]
        category = tokens[2] if len(tokens) > 2 else None
        custo = tokens[3] if len(tokens) > 3 else 0
        graph_view.add_vertex(name, category, custo)

    elif cmd == "modify":
        if len(tokens) < 3:
            print("Erro: Comando incompleto. Use: modify (id) (novo_nome) [nova_categoria] [novo_custo]")
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

    elif cmd == "delete":
        identifier = tokens[1] if len(tokens) > 1 else None
        if identifier:
            graph_view.delete_vertex(identifier)
        else:
            print("Erro: Comando incompleto. Use: delete (id/nome)")

    elif cmd == "delete_aresta":
        if len(tokens) < 3:
            print("Erro: Comando incompleto. Use: delete_aresta (nome1) (nome2)")
            return
        vertex1 = tokens[1]
        vertex2 = tokens[2]
        graph_view.delete_aresta(vertex1, vertex2)  # Chama delete_aresta para excluir a aresta específica

    elif cmd == "connect":
        if len(tokens) != 3:
            print("Comando inválido. Use: connect (id/nome1) (id/nome2)")
            return
        vertex1 = tokens[1]
        vertex2 = tokens[2]
        graph_view.add_aresta(vertex1, vertex2)  # Chama add_edge com nomes ou IDs

    elif cmd == "list":
        graph_view.list_graph()

    elif cmd == "exit":
        sys.exit()

    else:
        print(f"Comando desconhecido: {cmd}")

def main():
    app = QApplication(sys.argv)
    graph_view = GraphView()

    while True:
        command = input("Digite um comando (add, modify, delete, connect, list, exit): ")
        if command.lower() == 'exit':
            break
        process_command(command, graph_view)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
