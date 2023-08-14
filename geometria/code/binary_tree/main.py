import sys
sys.setrecursionlimit(2000)

import numpy as np
from tree import Tree

np.random.seed(69)

# generate a list of random values
nelements = 10
list_of_values = np.random.randint(0, 100, nelements)
print(f"list_of_values: {list_of_values}")

# build the tree from the list of values
tree = Tree(list_of_values)

# order the list of values
ordered_values = tree.inorder()
print(f"ordered_values: {ordered_values}")


# build the tree from the ordered list of values
newTree = tree.build_from_sorted_list(ordered_values)
print(f"newTree: {newTree}")
print(f"newTree.list_of_nodes: {newTree.list_of_nodes}")