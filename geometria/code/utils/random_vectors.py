import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from base import Vector

def build_many_vectors(n: int, low = -100, high = 100) -> list:

    vectors = np.random.randint(low, high, size=(n, 2))
    vectors = [Vector(v.reshape((2,-1))) for v in vectors]
    return vectors
