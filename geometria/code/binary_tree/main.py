import numpy as np
from tree import Tree
from plotter import TreePlotter

np.random.seed(69)
plotter = TreePlotter()

# generate a list of random values
nelements = 10
list_of_values = np.random.randint(0, 100, nelements)
print(f"list_of_values: {list_of_values}")

# build the tree from the list of values
tree = Tree(list_of_values)
plotter.plot(tree, filename="Original Tree")

# order the list of values
ordered_values = tree.inorder()
print(f"ordered_values: {ordered_values}")


# build the tree from the ordered list of values
newTree = tree.build_from_sorted_list(ordered_values)
plotter.plot(newTree, filename="New Tree")