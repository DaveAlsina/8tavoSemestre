# code/convex_hull/__init__.py
import sys

#get the parent directory of the current directory
parent_dir = "/".join(__file__.split("/")[:-1])
parent2_dir = "/".join(__file__.split("/")[:-2])
#add the parent directory to the path
sys.path.append(parent_dir)
sys.path.append(parent2_dir)


from node import Node, Node1D, Node2D
from tree import Tree
from plotter import TreePlotter