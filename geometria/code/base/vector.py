import numpy as np 
from typing import Union, List

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

    def calculate_distance(self, vector2: 'Vector') -> float:
        """
            Calculates the distance between self and vector2.

            Input:
                vector2: Vector
            Output:
                distance: float
        """
        return np.linalg.norm(self.vector - vector2.vector)
    
    def get_furthest_point(self, *points: 'Vector') -> 'Vector':

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

    #================================================
    #               Static methods
    #================================================
    @staticmethod
    def build_random_vectors(nvectors:int, minval = -10, maxval = 10) -> List['Vector']:
        vectors = []
        for i in range(nvectors):
            vectors.append(Vector(np.random.randint(minval, maxval, (2, 1))))

        return vectors
    
    @staticmethod
    def cast_to_vector(*vectors: np.ndarray) -> List['Vector']:
        return [Vector(vector) for vector in vectors]


    #================================================
    #               Operator overloading
    #================================================
    def __add__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector + vector2.vector)
    
    def __sub__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector - vector2.vector)
    
    def __mul__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector * vector2.vector)
    
    def __truediv__(self, number: float) -> 'Vector':
        return Vector(self.vector / number)

    def __str__(self):
        return f"({self.vector[0][0]}, {self.vector[1][0]})"
    
    def __getitem__(self, index: int) -> float:
        return self.vector[index][0]

    #================================================
    #              Order relations overloading
    #================================================

    def __eq__(self, vector: 'Vector') -> bool:
        return (self[0] == vector[0]) and (self[1] == vector[1])

    def __ne__(self, vector: 'Vector') -> bool:
        return (self[0] != vector[0]) or (self[1] != vector[1])

    def __gt__(self, vector2: 'Vector') -> bool:
        return (self[1] > vector2[1]) or (self[1] == vector2[1] and self[0] < vector2[0])
    
    def __lt__(self, vector2: 'Vector') -> bool:
        return (not (self > vector2)) and (self != vector2)
    
    def __ge__(self, vector2: 'Vector') -> bool:
        return (self > vector2) or (self == vector2)
    
    def __le__(self, vector2: 'Vector') -> bool:
        return (self < vector2) or (self == vector2)
    


