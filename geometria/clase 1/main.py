from vector import Vector
import numpy as np

v1 = np.array([[0], [1]])
v1 = Vector(v1)

v2 = np.array([[1], [0]])
v2 = Vector(v2)

print(v1.simple_positioning(v2))

#v1.plot()
#v1.plot_many(*(v2, v1 +v2,))


