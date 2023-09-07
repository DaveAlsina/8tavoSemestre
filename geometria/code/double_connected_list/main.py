import os, sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.vector import Vector
from double_connected_list.double_connected_segments import SemiEdgeList

set_of_points = [Vector(np.array([[5], [1]])), Vector(np.array([[8], [3]])), 
                 Vector(np.array([[5], [-2]])), Vector(np.array([[2], [2]])), 
                 Vector(np.array([[-1], [-1]])), Vector(np.array([[1], [5]]))]

list_of_semiedges = SemiEdgeList(set_of_points, name = "S1")
print("-"*80)
print(list_of_semiedges)