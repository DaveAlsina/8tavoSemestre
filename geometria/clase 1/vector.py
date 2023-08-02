import numpy as np 
from matplotlib import pyplot as plt

#we are using some new concepts to me, like:
# - forward annotations, to use the class Vector before it's defined
# - unpacking operator (*), to pass a variable number of arguments to a function

class Vector:

    """
        Assumes every vector is a column vector
    """

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

    #========================================
    #              Operations
    #========================================

    def simple_positioning(self, vector2: 'Vector') -> int:
        """
            Output:
                - 0, if vectors are colineal 
                - 1, if vector2 is rotated clockwise with respect to the current vector
                - -1, if vector2 is rotated anticlockwise with respect to the current vector
        """

        det = np.linalg.det(np.column_stack([self.vector, vector2.vector]))

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0 
    
    def walk(self, v2: 'Vector', v3: 'Vector', plotting = False) -> int:

        """
            assumes there is a walk from self to v2 to v3, 
            and determines if the person turned clockwise or anticlockwise
            at v2.
        
            Output:
                - 0, if vectors are colineal 
                - 1, if vector2 is rotated clockwise with respect to the current vector
                - -1, if vector2 is rotated anticlockwise with respect to the current vector
        """


        vector1 = v2 - self
        vector2 = v3 - self
    
        det = np.linalg.det(np.column_stack([vector1.vector, vector2.vector]))

        if plotting:
            plt.legend(["v1", "v2", "v3"])
            self.plot_many(self, v2, v3)

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0

    
    #========================================
    #               Plotting
    #========================================
    
    def plot(self):
        plt.arrow(0, 0, self.vector[0][0], self.vector[1][0], head_width=0.1, head_length=0.1, color="g")
        norm = np.linalg.norm(self.vector)
        plt.xlim(-2*norm, 2*norm)
        plt.ylim(-2*norm, 2*norm)
        plt.show()
    
    def plot_many(self, *vectors: 'Vector'):

        for vector in vectors:
            print(vector)
            plt.arrow(0, 0, vector.vector[0][0], vector.vector[1][0], head_width=0.1, head_length=0.1, color="g")

        norm = max([np.linalg.norm(v.vector) for v in vectors])

        plt.xlim(-2*norm, 2*norm)
        plt.ylim(-2*norm, 2*norm)
        plt.show()

        
    def __add__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector + vector2.vector)
    
    def __sub__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector - vector2.vector)
    
    def __mul__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector * vector2.vector)

    def __str__(self):
        return f"{self.vector}"

