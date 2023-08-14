import numpy as np 
from typing import Union, List

class Vector:
    def __init__(self, vector: np.ndarray):
        
        #it's a column vector
        if (vector.shape[0] > 1) and (vector.shape[1] == 1):
            self.vector = vector
            self.T = vector.T
        
        #it's a row vector
        elif (vector.shape[1] > 1) and (vector.shape[0] == 1):
            self.vector = vector.T
            self.T = vector.T

        else:
            raise TypeError(f"Should be a row or a column vector, yet has shape: {vector.shape}")

    @property
    def ndimensions(self) -> int:
        return self.vector.shape[0]

    def __add__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector + vector2.vector)
    
    def __sub__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector - vector2.vector)
    
    def __mul__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector * vector2.vector)

    def __str__(self):
        return f"({self.vector[0][0]}, {self.vector[1][0]})"
    
    def __getitem__(self, index: int) -> float:
        return self.vector[index][0]

    @staticmethod
    def build_random_vectors(nvectors:int, minval = -10, maxval = 10) -> List['Vector']:
        vectors = []
        for i in range(nvectors):
            vectors.append(Vector(np.random.randint(minval, maxval, (2, 1))))

        return vectors
    
    @staticmethod
    def cast_to_vector(*vectors: np.ndarray) -> List['Vector']:
        return [Vector(vector) for vector in vectors]