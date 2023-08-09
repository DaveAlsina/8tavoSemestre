import numpy as np
from swiss_army_knife import SwissArmyKnifeVector
from vector import Vector

v1 = np.array([[-1],  [0]])
v2 = np.array([[1],  [0]])
v3 = np.array([[0], [-1]])
v4 = np.array([[0], [1]])

util = SwissArmyKnifeVector()
vectors = util.cast_to_vector(v1, v2, v3, v4)

