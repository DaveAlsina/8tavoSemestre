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

    @staticmethod
    def cast_to_vector(*vectors: np.ndarray) -> list:
        return [Vector(vector) for vector in vectors]

    #========================================
    #              Operations
    #========================================
    @staticmethod
    def calcutale_slope(v1: 'Vector', v2: 'Vector') -> float:
        """
            Calculates the slope of the line that passes through v1 and v2
        """
        deltas = v2 - v1

        if deltas[0] == 0:
            return np.inf
        return (deltas[1])/(deltas[0])

    @staticmethod
    def calculate_distance(v1: 'Vector', v2: 'Vector') -> float:
        """
            Calculates the distance between v1 and v2
        """
        return np.linalg.norm(v2 - v1)


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

    @staticmethod
    def simple_positioning(vector1: Vector, vector2: Vector) -> int:
        """
            Output:
                - 0, if vectors are colineal 
                - 1, if vector2 is rotated clockwise with respect to the current vector
                - -1, if vector2 is rotated anticlockwise with respect to the current vector
        """

        det = np.linalg.det(np.column_stack([vector1.vector, vector2.vector]))

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0 

    
    @staticmethod
    def turn(v1: Vector, v2: Vector, v3: Vector) -> int:

        """
            Assumes there is a walk from v1 to v2 to v3, 
            and determines if the person turned clockwise or anticlockwise
            at v2.
        
            Output:
                - 0, if vectors are colineal 
                - 1, if vector2 is rotated clockwise with respect to the current vector
                - -1, if vector2 is rotated anticlockwise with respect to the current vector
        """

        vector1 = v2 - v1
        vector2 = v3 - v1
    
        det = np.linalg.det(np.column_stack([vector1.vector, vector2.vector]))

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0

    @staticmethod
    def direction(vector1: Vector, vector2: Vector, vector3: Vector) -> int:

        det = np.linalg.det(np.column_stack([(vector3 - vector1).vector, (vector2 - vector1).vector]))

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0

    @staticmethod
    def on_segment(v1: Vector, v2: Vector, v3: Vector) -> bool:
            
            """
                Checks if v3 is on the segment v1v2
            """
            inx = min(v1[0], v2[0]) <= v3[0] <= max(v1[0], v2[0]) 
            iny = min(v1[1], v2[1]) <= v3[1] <= max(v1[1], v2[1])

            if (inx and iny):
                return True
            return False

    @staticmethod
    def segments_intersect(v1: Vector, v2: Vector, v3: Vector, v4: Vector) -> bool:

        """
            Given two pairs of vectors, determines if the segments they form intersect.
            Segments are v1v2 and v3v4, from the input.
        """

        dir1 = SwissArmyKnifeVector.direction(v3, v4, v1)
        dir2 = SwissArmyKnifeVector.direction(v3, v4, v2)
        dir3 = SwissArmyKnifeVector.direction(v1, v2, v3)
        dir4 = SwissArmyKnifeVector.direction(v1, v2, v4)

        #well behaved case
        if (dir1*dir2 < 0) and (dir3*dir4 < 0):
            return True
    
        #collinear case
        elif (dir1 == 0) and (SwissArmyKnifeVector.on_segment(v3, v4, v1)):
            return True

        elif (dir2 == 0) and (SwissArmyKnifeVector.on_segment(v3, v4, v2)):
            return True

        elif (dir3 == 0) and (SwissArmyKnifeVector.on_segment(v1, v2, v3)):
            return True

        elif (dir4 == 0) and (SwissArmyKnifeVector.on_segment(v1, v2, v4)):
            return True
        
        else:
            return False
    
    @staticmethod
    def find_intersection(v1: Vector, v2: Vector, v3: Vector, v4: Vector) -> Vector:
        """
            Finds the intersection of the lines formed by the segments v1v2 and v3v4.
        """

        matrix = np.column_stack([v1 - v2, v3 - v4])
        result = v1 - v3
        intersection = np.linalg.solve(matrix, result)

        return Vector(intersection)
    