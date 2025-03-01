"""
langgraph/graph.py - Minimal state graph engine implementation
"""
# Define an END marker for workflow termination
END = "END"

class StateGraph:
    def __init__(self, state_class):
        self.nodes = {}
        self.edges = {}
        self.conditional_edges = {}
        self.entry_point = None
        self.state_class = state_class

    def add_node(self, name, func):
        self.nodes[name] = func

    def add_edge(self, src, dest):
        self.edges.setdefault(src, []).append(dest)

    def add_conditional_edges(self, src, condition_func, mapping):
        self.conditional_edges[src] = (condition_func, mapping)

    def set_entry_point(self, name):
        self.entry_point = name

    def compile(self):
        return GraphCompiled(self.entry_point, self.nodes, self.edges, self.conditional_edges)

class GraphCompiled:
    def __init__(self, entry_point, nodes, edges, cond_edges):
        self.entry_point = entry_point
        self.nodes = nodes
        self.edges = edges
        self.cond_edges = cond_edges

    def invoke(self, state):
        current = self.entry_point
        while current != END:
            if current in self.cond_edges:
                condition_func, mapping = self.cond_edges[current]
                result = condition_func(state)
                if result == END:
                    current = END
                    continue
                current = mapping.get(result, END)
                continue
            else:
                func = self.nodes.get(current)
                if func is None:
                    raise Exception(f"Node {current} not found.")
                state = func(state)
                if current in self.edges:
                    current = self.edges[current][0]
                else:
                    current = END
        return state
