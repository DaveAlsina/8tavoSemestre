import numpy as np
from vector import Vector
from plotter import VectorPlotter, SegmentPlotter
from poligon import Poligon

#===============================================================================
# example 1
plotter = VectorPlotter()
vectors1 = [np.array([[2.2], [1.6]]), np.array([[2.0], [0.2]]),
           np.array([[1.5], [0.3]]), np.array([[0.7], [1.3]]), 
           np.array([[0.5], [1.7]]), ]
vectors1 = Vector.cast_to_vector(vectors1)

p1 = Poligon(vectors1)
print(f"is poligon ex. 1 convex? {p1.is_convex()}")
plotter.plot_many(vectors1, with_labels=True)
plotter.show()

#===============================================================================
# example 2
vectors2 = [np.array([[1.4], [1.2]]), np.array([[2.2], [1.6]]),
           np.array([[2.0], [0.2]]), np.array([[1.5], [0.3]]), 
           np.array([[0.7], [1.3]]), ]
vectors2 = Vector.cast_to_vector(vectors2)

p2 = Poligon(vectors2)
print(f"is poligon ex. 2 convex? {p2.is_convex()}")
plotter.plot_many(vectors2, with_labels=True)
plotter.show()
#===============================================================================
# example 3

#a square
vectors3 = [np.array([[0], [0]]), np.array([[1], [0]]),
            np.array([[1], [1]]), np.array([[0], [1]]),]

vectors3 = Vector.cast_to_vector(vectors3)
p3 = Poligon(vectors3)
print(f"is poligon ex. 3 convex? {p3.is_convex()}")
plotter.plot_many(vectors3, with_labels=True)
plotter.show()

#===============================================================================
# example 4

# another not convex poligon of 5 vertices
vectors4 = [np.array([[0], [0]]), np.array([[1], [0]]),
            np.array([[1], [1]]), np.array([[0.5], [0.5]]),
            np.array([[0], [1]]),]

vectors4 = Vector.cast_to_vector(vectors4)
p4 = Poligon(vectors4)
print(f"is poligon ex. 4 convex? {p4.is_convex()}")
plotter.plot_many(vectors4, with_labels=True)
plotter.show()

