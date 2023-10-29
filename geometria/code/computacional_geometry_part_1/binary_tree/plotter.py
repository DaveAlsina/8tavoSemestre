import graphviz
from tree import Tree

class TreePlotter:

    def __init__(self):
        pass

    @staticmethod
    def plot(tree: Tree, filename: str = 'tree'):
        dot = graphviz.Digraph()
        dot.node(str(tree.root.value))

        def add_nodes_edges(node):
            if node.left:
                dot.node(str(node.left.value))
                dot.edge(str(node.value), str(node.left.value))
                add_nodes_edges(node.left)
            if node.right:
                dot.node(str(node.right.value))
                dot.edge(str(node.value), str(node.right.value))
                add_nodes_edges(node.right)

        add_nodes_edges(tree.root)
        dot.render(filename, view=True, format='png')