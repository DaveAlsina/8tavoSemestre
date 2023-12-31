import os, sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.vector import Vector
from double_connected_list.double_connected_segments import SemiEdgeList
from code.double_connected_list.overlay.plot_subdivisions import PlotSubdivisions 
from code.double_connected_list.overlay.overlay_of_subdivisions import OverlayOfSubdivisions

set_of_points1 = [Vector(np.array([[5], [1]])), Vector(np.array([[8], [3]])), 
                 Vector(np.array([[5], [-2]])), Vector(np.array([[2], [2]])), 
                 Vector(np.array([[-1], [-1]])), Vector(np.array([[1], [5]]))]

set_of_points2 = [Vector(np.array([[0], [3]])),  Vector(np.array([[4], [3]])),
                  Vector(np.array([[4], [-1]])), Vector(np.array([[0], [-1]]))]

list_of_semiedges1 = SemiEdgeList(set_of_points1, name = "S1")
list_of_semiedges2 = SemiEdgeList(set_of_points2, name = "S2")

PlotSubdivisions.plot_many([list_of_semiedges1, list_of_semiedges2],)
PlotSubdivisions.show()

o = OverlayOfSubdivisions([list_of_semiedges1, list_of_semiedges2])
o.find_subdivisions_intersections(False)
print(o.overlay_intersections)

# now with the overlay intersections we can build the overlay subdivision
PlotSubdivisions.plot_many([list_of_semiedges1, list_of_semiedges2], 
                           intersection_points=o.overlay_intersections)
PlotSubdivisions.show()