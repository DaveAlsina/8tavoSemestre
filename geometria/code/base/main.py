import numpy as np
from vector import Vector
from segment import Segment
from plotter import VectorPlotter, SegmentPlotter

np.random.seed(69)

#===============================================================================
plotter = VectorPlotter()
vectors = Vector.build_random_vectors(100)

plotter.plot(vectors[0])
plotter.plot_many(vectors)


#===============================================================================
segment_plotter = SegmentPlotter()
segments = Segment.build_random_segments(5)
intersect = segments[0].find_intersection(segments[1])

segment_plotter.plot(segments[0])
segment_plotter.plot_many([segments[0], segments[1]])
plotter.plot(intersect, highlighted=True)
segment_plotter.plot_many(segments)
print(f"Intersect: {intersect.vector}")
segment_plotter.show()