import numpy as np 
from matplotlib import pyplot as plt

from convex_hull import *
from utils import *

np.random.seed(69)

convex_hull = ConvexHull()
plotter = SwissArmyKnifePlotting()
vectors = build_many_vectors(20)

v0 = convex_hull.get_stating_point(*vectors)
print("v0: ", v0)

sorted_points = convex_hull.sort_by_slope(v0, *vectors)
print("sorted_points: ", sorted_points)

convex_hull.convex_hull(*vectors)
plotter.plot_many(*sorted_points, highlighted=[v0,], with_labels=True)

