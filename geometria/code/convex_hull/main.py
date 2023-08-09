import numpy as np 
from matplotlib import pyplot as plt

from convex_hull import *
from utils import *

np.random.seed(69)

v1 = np.array([[1], [0]])
v2 = np.array([[1], [1]])
v3 = np.array([[1], [4]])
v4 = np.array([[-3], [4]])

convex_hull = ConvexHull()
plotter = SwissArmyKnifePlotting()
vectors = build_many_vectors(20)

v0 = convex_hull.get_stating_point(*vectors)
print("v0: ", v0)

sorted_points = convex_hull.sort_by_slope(v0, *vectors)
print("sorted_points: ", sorted_points)

convex_hull.convex_hull(*vectors)
plotter.plot_many(*vectors, highlighted=[v0,])

