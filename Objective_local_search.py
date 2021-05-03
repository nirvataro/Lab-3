class ObjectiveFunctionGraph:
    def __init__(self, graph):
        self.graph = graph

    def objective_function(self):
        val = sum([color**2 for color in self.graph.colors])
        return val

    def kempe_chains(self, node, new_color):
        true_new_color = new_color
        old_color_nodes = []
        new_color_nodes = []
        old_color = node.color
        new_nodes = [node.number]
        while new_nodes:
            neighbors = []
            for node in new_nodes:
                neighbors += [self.graph.nodes[v] for v in self.graph.nodes[node].neighbors if self.graph.nodes[v].color == new_color]
                old_color_nodes.append(node)
            new_nodes = []
            for v in neighbors:
                if v.number not in new_color_nodes:
                    new_nodes.append(v.number)
            old_color, new_color = new_color, old_color
            old_color_nodes, new_color_nodes = new_color_nodes, old_color_nodes
        if true_new_color != new_color:
            old_color, new_color = new_color, old_color
            old_color_nodes, new_color_nodes = new_color_nodes, old_color_nodes
        for v in old_color_nodes:
            self.graph.uncolor_node(v)
        for v in new_color_nodes:
            self.graph.uncolor_node(v)
        for v in old_color_nodes:
            self.graph.color_node(v, new_color)
        for v in new_color_nodes:
            self.graph.color_node(v, old_color)

    def improve(self):
        objective = self.objective_function()
        for node in self.graph.nodes:
            if node.number:
                current_color = node.color
                for color in range(len(self.graph.colors)):
                    if color != current_color:
                        self.kempe_chains(node, color)
                        if self.objective_function() > objective:
                            return True
                        else:
                            self.kempe_chains(node, current_color)
        return False


def objective_local_search(graph):
    ols_graph = ObjectiveFunctionGraph(graph)
    can_improve = ols_graph.graph.initial_solution()
    while can_improve:
        print(ols_graph.graph)
        can_improve = ols_graph.improve()