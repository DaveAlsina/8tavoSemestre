import os, sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base.vector import Vector
from sweep_line_to_monotone_polygon import SweepLineMonotonePoly
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
#invert the order of the points
vectors2 = vectors2[::-1]

#------------------------------------------------------------

semiedges = SemiEdgeList(vectors1, name = "S1")
#diagonals = SweepLineMonotonePoly(semiedges).run(plotting=False)
#semiedges.add_new_semi_edges(diagonals)
#semiedges.add_new_edge(diagonals[0])
#
#print(f"Diagonals: {diagonals}\n\n")
#print(semiedges.show_data_structure())
#
#
#PlotDoubleConnectedEdgeList.plot(semiedges)
#PlotDoubleConnectedEdgeList.show()

triangulate = Triangulate(semiedges)
triangulate.run()


