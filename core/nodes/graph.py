# ----------------------------------------------------------------------
# graph.py
#
# Graph classes
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class Graph(Expression):
    def __init__(self, vertices, token) -> None:
        super().__init__()

        self.graph = {}
        self.token, self.length = token, vertices

    def __str__(self) -> str:
        return f"Graph <{self.length}>"

    def _eval(self, env, **kwargs):
        # Eval True
        count = self.length._eval(env, eval=True)

        # Node: list of connections [], associated (label, struct)
        self.graph = {node: [[], None] for node in range(count)}
        return self.graph

class Edge(Expression):
    def __init__(self, graph, start, end, token) -> None:
        super().__init__()

        self.graph = graph
        self.start, self.end = start, end

        self.token = token

    def __str__(self) -> str:
        return f"Edge <{self.graph}> {self.start} -> {self.end}"

    def _eval(self, env, **kwargs):
        graph = self.graph._eval(env, eval=True)
        start = self.start._eval(env, eval=True)
        end = self.end._eval(env, eval=True)

        edges = graph[start][0]

        if end in edges:
            raise Exception(
                f"Node {end} already exists")
                
        edges.append(end)
        return None