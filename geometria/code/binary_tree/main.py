import sys
sys.setrecursionlimit(2000)

import numpy as np
from tree import Tree

np.random.seed(69)

nelements = 10
list_of_values = np.random.randint(0, 100, nelements)
print(f"list_of_values: {list_of_values}")

tree = Tree(list_of_values)

ordered_values = tree.inorder()
print(f"ordered_values: {ordered_values}")
