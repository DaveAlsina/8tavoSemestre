import numpy as np 
from matplotlib import pyplot as plt

from convex_hull_graham import ConvexHullGraham
from base import Vector, VectorPlotter

np.random.seed(70)
convex_hull = ConvexHullGraham()
plotter = VectorPlotter()
nvectors = 50

# Generate random points
points = Vector.build_random_vectors(nvectors, -100, 100)

# Plot points
plotter.plot_many(points)

#apply convex hull
envelope = convex_hull.convex_hull(points)
plotter.plot_many(points, highlighted=envelope)
plotter.show()


