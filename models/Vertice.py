class Vertice:
    def __init__(self, name, value, category, connection):
        self.name = name
        self.value = value
        self.category = category
        self.connection = connection

    def __str__(self):
        return f"{{'name': '{self.name}','value': '{self.value}''category': '{self.category}''connection': '{self.connection}'}}"
