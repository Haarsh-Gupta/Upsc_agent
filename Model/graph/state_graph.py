class StateNode:
    def __init__(self, name, handler):
        self.name = name
        self.handler = handler
        self.edges = {}

    def connect(self, condition, node):
        self.edges[condition] = node
