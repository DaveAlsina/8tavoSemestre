import numpy as np 
from vector import Vector

#we are using some new concepts to me, like:
# - forward annotations, to use the class Vector before it's defined
# - unpacking operator (*), to pass a variable number of arguments to a function

class SwissArmyKnifeVector:

    """
    ImportError: attempted relative import with no known parent package
        Assumes every vector is a column vector.
        Meaning this works with the Vector class.

        This has a compendium of operations that can be done with vectors.
    """

    def __init__(self):
        pass

    #========================================
    #              Operations
    #========================================
    def find_furthest_point(v0: Vector, *points: Vector) -> Vector:

        """
            Finds the furthest point from v0.
        """

        # calculate the distance from v0 to each point
        distances = [SwissArmyKnifeVector.calculate_distance(v0, point) for i, point in enumerate(points)]
        
        # find the maximum distance
        maxdist = max(distances)

        # find the indexes of the points with the maximum distance
        indexes = [i for i, d in enumerate(distances) if d == maxdist]

        return points[indexes[0]]
    