import numpy as np
from vector import Vector
from segment import Segment
from plotter import VectorPlotter, SegmentPlotter

#===============================================================================
plotter = VectorPlotter()
vectors = Vector.build_random_vectors(100)

plotter.plot(vectors[0])
plotter.plot_many(vectors)


#===============================================================================
segment_plotter = SegmentPlotter()
segments = Segment.build_random_segments(5)

segment_plotter.plot(segments[0])
segment_plotter.plot_many(segments)