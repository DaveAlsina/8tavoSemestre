# code/__init___.py
import sys

#get the parent directory of the current directory
parent_dir = "/".join(__file__.split("/")[:-1])
#add the parent directory to the path
sys.path.append(parent_dir)

from base import *
from convex_hull import *