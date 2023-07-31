import numpy as np 

class Vector:

    """
        Assumes every vector is a column vector
    """

    def __init__(self, vector: np.ndarray):
        
        #its a column vector
        if (vector.shape[0] >= 1) and (vector.shape[1] == 1):
            self.vector = vector
            self.T = vector.T
        
        #it's a row vector
        elif (vector.shape[1] > 1) and (vector.shape[0] == 1):
            self.vector = vector.T
            self.T = vector.T

        else:
            raise TypeError(f"Should be a row or a column vector, yet has shape: {vector.shape}")


    def ndimensions(self) -> int:
        return self.vector.shape[0]

    def simple_positioning(self, vector2) -> int:
        """
            Output:
                - 0, if vectors are colineal 
                - 1, if vector2 is rotated clockwise with respect to the current vector
                - 2, if vector2 is rotated anticlockwise with respect to the current vector
        """

        det = np.linalg.det(np.column_stack([self.vector, vector2.vector]))

        if det < 0:
            return 1
        elif det > 0:
            return 2
        return 0 
        
    def __str__(self):
        return f"{self.vector}"



