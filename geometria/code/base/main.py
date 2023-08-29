import numpy as np
from vector import Vector
from segment import Segment
from double_connected_segments import GeometricNode, SemiEdge, Face
from plotter import VectorPlotter, SegmentPlotter

np.random.seed(69)

#===============================================================================
#plotter = VectorPlotter()
#vectors = Vector.build_random_vectors(100)

#plotter.plot(vectors[0])
#plotter.plot_many(vectors)


#===============================================================================
#segment_plotter = SegmentPlotter()
#segments = Segment.build_random_segments(5)
#intersect = segments[0].find_intersection(segments[1])

#segment_plotter.plot(segments[0])
#segment_plotter.plot_many([segments[0], segments[1]])
#plotter.plot(intersect, highlighted=True)
#segment_plotter.plot_many(segments)
#print(f"Intersect: {intersect.vector}")
#segment_plotter.show()

#===============================================================================
set_of_points = [Vector(np.array([[5], [1]])), Vector(np.array([[8], [3]])), 
                 Vector(np.array([[5], [-2]])), Vector(np.array([[2], [2]])), 
                 Vector(np.array([[-1], [-1]])), Vector(np.array([[1], [5]]))]

geometric_nodes = [GeometricNode(point, f"N{i}") for i, point in enumerate(set_of_points)]
print(geometric_nodes)

semi_edges = [SemiEdge(geometric_nodes[i], geometric_nodes[i+1], geometric_nodes[i-1]) for i in range(1, len(geometric_nodes)-1)]

for semi_edge in semi_edges:
    print(semi_edge)
