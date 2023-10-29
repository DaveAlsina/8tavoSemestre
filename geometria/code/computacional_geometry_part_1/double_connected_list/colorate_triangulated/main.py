import os, sys
import numpy as np
from matplotlib import pyplot as plt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from coloration import TriangulationColoring
from base.vector import Vector
from plot_double_connected_edge_list import PlotDoubleConnectedEdgeList
from double_connected_list.triangulation.triangulate import Triangulate
from double_connected_list.double_connected_segments import SemiEdge, SemiEdgeList

#------------------------------------------------------------
points1 = [np.array([4.5, 3]), np.array([3.5, 2.5]), np.array([3, 4]), np.array([2.5, 3.75]), 
          np.array([2, 4]), np.array([1, 3.5]), np.array([1.5, 2.75]), np.array([1, 1.5]), 
          np.array([0.5, 2]), np.array([0, 1]), np.array([1, 0]), np.array([2, 0.5]), 
          np.array([3, 0]), np.array([2.5, 1]), np.array([4, 0.5])]
vectors1 = Vector.cast_to_vector(*points1)

points2 = [np.array([5, 1]), np.array([8, 3]), np.array([5, -2]),
           np.array([2, 2]), np.array([-1, -1]), np.array([1, 5])]
vectors2 = Vector.cast_to_vector(*points2)

points3 = [np.array([9, -1]), np.array([8, 6]), np.array([7, -3]), np.array([6, 3]),
              np.array([4, -4]), np.array([2, -4]), np.array([3, 4]), np.array([4, 2.5]),
              np.array([5, 12]), np.array([7, 12]), np.array([10, 6]), np.array([9.5, 11]),
              np.array([11, 15]), np.array([13, 15]), np.array([12, 10]), np.array([13, 3]),
              np.array([11, 4]), np.array([10, -1])]
vectors3 = Vector.cast_to_vector(*points3)

#------------------------------------------------------------

semiedges = SemiEdgeList(vectors3, name = "S1")

#print(semiedges.show_data_structure())
triangulate = Triangulate(semiedges)
semiedges, diagonals = triangulate.run(plotting=False, plotting_monotone=False)
semiedges.add_new_semi_edges(diagonals)

semiedges = TriangulationColoring(semiedges).run(plotting=True)
