import numpy as np
from vector import Vector
from segment import Segment
from plotter import VectorPlotter, SegmentPlotter

np.random.seed(69)

##===============================================================================
#plotter = VectorPlotter()
#vectors = Vector.build_random_vectors(100)
#
#plotter.plot(vectors[0])
#plotter.plot_many(vectors)
#
#
##===============================================================================
#segment_plotter = SegmentPlotter()
#segments = Segment.build_random_segments(5)
#intersect = segments[0].find_intersection(segments[1])
#
#segment_plotter.plot(segments[0])
#segment_plotter.plot_many([segments[0], segments[1]])
#plotter.plot(intersect, highlighted=True)
#segment_plotter.plot_many(segments)
#print(f"Intersect: {intersect.vector}")
#segment_plotter.show()


vectors = [np.array([[4], [0]]), np.array([[2], [1]]), np.array([[0], [0]])]
vectors = Vector.cast_to_vector(*vectors)
a, b, c = vectors[0], vectors[1], vectors[2]
plotter = VectorPlotter()
plotter.plot_many(vectors)
plotter.show()

print(f"Angle between a and b: {Vector.calculate_angle(a, b, c)}")
