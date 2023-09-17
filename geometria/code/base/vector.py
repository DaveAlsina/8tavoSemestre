import math
import numpy as np 
from typing import Union, List, Tuple

#we are using some new concepts to me, like:
# - forward annotations, to use the class Vector before it's defined
# - unpacking operator (*), to pass a variable number of arguments to a function

class Vector:
    def __init__(self, vector: np.ndarray):
        
        #it's a column vector
        if (vector.shape[0] > 1) and (vector.shape[1] == 1):
            self.vector = vector
            self.T = vector.T
            self.ndimensions = self.vector.shape[0]
        
        #it's a row vector
        elif (vector.shape[1] > 1) and (vector.shape[0] == 1):
            self.vector = vector.T
            self.T = vector.T
            self.ndimensions = self.vector.shape[0]
        else:
            raise TypeError(f"Should be a row or a column vector, yet has shape: {vector.shape}")

    #================================================
    #            Some important operations
    #================================================

    def calculate_slope(self, vector2: 'Vector') -> float:
        """
            Calculates the slope between self and vector2.

            Input:
                vector2: Vector
            Output:
                slope: float
        """

        if self[0] == vector2[0]:
            return np.inf
        return (self[1] - vector2[1]) / (self[0] - vector2[0])


    def calculate_distance(self, vector2: 'Vector') -> float:
        """
            Calculates the distance between self and vector2.

            Input:
                vector2: Vector
            Output:
                distance: float
        """
        return np.linalg.norm(self.vector - vector2.vector)
    
    def get_furthest_point(self, points: List['Vector']) -> 'Vector':

        """
            Finds the furthest point from self.

            Input:
                points: Vector or List[Vector]
            Output:
                furthest_point: Vector
        """

        # calculate the distance from v0 to each point
        distances = [self.calculate_distance(point) for i, point in enumerate(points)]
        
        # find the maximum distance
        maxdist = max(distances)

        # find the indexes of the points with the maximum distance
        indexes = [i for i, d in enumerate(distances) if d == maxdist]

        return points[indexes[0]]


    @staticmethod
    def calculate_angle(A:'Vector', B:'Vector', C:'Vector') -> Tuple[float, float]:
        """
            Calculates the angle between the vectors AB and BC. This is the same
            as the angle between a walk from A to B and a walk from B to C, and 
            get the angle at the bend.

            Args:
            -----------
                A: Vector
                B: Vector
                C: Vector
            
            Returns:
            -----------
                angle_rad: float
                    Angle in radians
                angle_deg: float
                    Angle in degrees
        """

        AB = B - A
        BC = B - C

        # calculate the cross product between A and B (which are column vectors)
        cross_product = np.cross(AB.vector.T, BC.vector.T)

        # calculate the dot product between A and B (which are column vectors)
        dot_product = np.dot(AB.vector.T, BC.vector)

        # get direction, which is the sign of the cross product and determine if 
        # the angle is convex or concave
        direction = np.sign(cross_product)

        # calculate the angle between A and B, using the cross and dot products
        # with the arctan2 function
        angle_rad = np.arctan2(cross_product, dot_product) + np.pi*direction

        # convert the angle to degrees
        angle_deg = np.degrees(angle_rad)

        #make sure both angles are positive with modular arithmetic
        angle_rad = (angle_rad + 2) % (2)
        angle_deg = (angle_deg + 360) % 360

        return float(angle_rad), float(angle_deg)


    @staticmethod
    def calculate_turn(vector1: 'Vector', vector2: 'Vector', vector3: 'Vector') -> int:

        """
            Calculates if the walk from vector1 to vector2 to vector3 is a left turn
            or a right turn.

            Input:
                vector1: Vector
                vector2: Vector
                vector3: Vector
            Output:
                1: if the walk is a left turn
                -1: if the walk is a right turn
                0: if the points are collinear
        """

        # calculate the cross product between A and B (which are column vectors)
        cross_product = np.cross((vector2 - vector1).vector.T, (vector3 - vector2).vector.T)

        # get direction, which is the sign of the cross product and determine if 
        # the angle is convex or concave
        direction = np.sign(cross_product)

        return int(direction)

    #================================================
    #               Static methods
    #================================================
    @staticmethod
    def get_leftmost_point(points: List['Vector']) -> 'Vector':
        """
            Finds the leftmost point from a list of points.

            Input:
                points: List[Vector]
            Output:
                leftmost_point: Vector
        """
        # find the leftmost point
        leftmost_point = points[0]
        for point in points[1:]:
            if point[0] < leftmost_point[0]:
                leftmost_point = point
        return leftmost_point
    
    @staticmethod
    def get_rightmost_point(points: List['Vector']) -> 'Vector':
        """
            Finds the rightmost point from a list of points.

            Input:
                points: List[Vector]
            Output:
                rightmost_point: Vector
        """
        # find the rightmost point
        rightmost_point = points[0]
        for point in points[1:]:
            if point[0] > rightmost_point[0]:
                rightmost_point = point
        return rightmost_point

    @staticmethod
    def build_random_vectors(nvectors:int, minval = -10, maxval = 10) -> List['Vector']:
        vectors = []
        for i in range(nvectors):
            vectors.append(Vector(np.random.randint(minval, maxval, (2, 1))))

        return vectors
    
    @staticmethod
    def cast_to_vector(*vectors: np.ndarray) -> List['Vector']:
        """
            Casts a list of numpy arrays to a list of column vectors.
        """
        #reshape the vectors to be column vectors
        vectors = [vector.reshape((2, 1)) for vector in vectors]
        return [Vector(vector) for vector in vectors]

    #================================================
    #               Operator overloading
    #================================================
    
    def times_scalar(self, scalar: float) -> 'Vector':
        return Vector(self.vector * scalar)

    def __add__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector + vector2.vector)
    
    def __sub__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector - vector2.vector)
    
    def __mul__(self, other: 'Vector') -> 'Vector':
        if isinstance(other, Vector): 
            return Vector(self.vector * other.vector)
        else: 
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other) 
    
    def __truediv__(self, number: float) -> 'Vector':
        return Vector(self.vector / number)

    def __getitem__(self, index: int) -> float:
        return float(self.vector[index][0])

    def __repr__(self):
        return f"Vec({self.vector[0][0]}, {self.vector[1][0]})"

    def __str__(self):
        return f"Vec({self.vector[0][0]}, {self.vector[1][0]})"

    #================================================
    #              Order relations overloading
    #================================================

    def __eq__(self, vector: 'Vector') -> bool:
        return (self[0] == vector[0]) and (self[1] == vector[1])

    def __ne__(self, vector: 'Vector') -> bool:
        return (self[0] != vector[0]) or (self[1] != vector[1])

    def __lt__(self, vector2: 'Vector') -> bool:
        return (self[1] > vector2[1]) or (self[1] == vector2[1] and self[0] < vector2[0])

    def __gt__(self, vector2: 'Vector') -> bool:
        return (self[1] < vector2[1]) or (self[1] == vector2[1] and self[0] > vector2[0])
    
    def __ge__(self, vector2: 'Vector') -> bool:
        return (self > vector2) or (self == vector2)
    
    def __le__(self, vector2: 'Vector') -> bool:
        return (self < vector2) or (self == vector2)
    
    def __hash__(self):
        return hash((self[0], self[1]))