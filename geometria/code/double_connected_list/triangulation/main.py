import os, sys
import numpy as np
from matplotlib import pyplot as plt
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

points3 = [np.array([9, -1]), np.array([8, 6]), np.array([7, -3]), np.array([6, 3]),
              np.array([4, -4]), np.array([2, -4]), np.array([3, 4]), np.array([4, 2.5]),
              np.array([5, 12]), np.array([7, 12]), np.array([10, 6]), np.array([9.5, 11]),
              np.array([11, 15]), np.array([13, 15]), np.array([12, 10]), np.array([13, 3]),
              np.array([11, 4]), np.array([10, -1])]
vectors3 = Vector.cast_to_vector(*points3)
vectors3 = vectors3[::-1]

#------------------------------------------------------------

semiedges = SemiEdgeList(vectors3, name = "S1")
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

print(semiedges.show_data_structure())
triangulate = Triangulate(semiedges)
semiedges, diagonals = triangulate.run(plotting=False, plotting_monotone=False)


for diagonal in diagonals:

    print(f"typeof(diagonal): {type(diagonal)}")
    #plot the diagonal I want to add in orange
    PlotDoubleConnectedEdgeList.plot(semiedges)
    plt.plot([diagonal.origin.x, diagonal.next_.x], [diagonal.origin.y, diagonal.next_.y], color="orange")
    PlotDoubleConnectedEdgeList.show()

    semiedges.add_new_edge(diagonal)
    print(semiedges.show_data_structure())
    PlotDoubleConnectedEdgeList.plot(semiedges)
    PlotDoubleConnectedEdgeList.show()
    print("\n\n")


