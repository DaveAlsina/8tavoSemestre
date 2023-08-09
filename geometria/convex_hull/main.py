import numpy as np 
from convex_hull import *

v1 = np.array([[1], [0]])
v2 = np.array([[1], [1]])
v3 = np.array([[1], [4]])
v4 = np.array([[-3], [4]])

points = (v1, v2, v3, v4)
v0 = get_stating_point(*points)
print("v0: ", v0)

sorted_points = sort_by_slope(v0, *points)
print("sorted_points: ", sorted_points)