class Vertice:
    def __init__(self, name, value, category, connections):
        self.name = name
        self.value = value
        self.category = category
        self.connections = connections

    def generate_html_connections(self):
        html_string = ""
        for conn in self.connections:
            html_string = html_string + " <br> " + conn

    def __str__(self):
        return f"{{'name': '{self.name}','value': '{self.value}''category': '{self.category}''connection': '{self.connection}'}}"
