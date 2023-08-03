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

    def simple_positioning(self, vector2: 'Vector', plotting = False) -> int:
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

    
    def walk_turn(self, v2: 'Vector', v3: 'Vector', plotting = False) -> int:

        """
            assumes there is a walk from self to v2 to v3, 
            and determines if the person turned clockwise or anticlockwise
            at v2.
        
            Output:
                - 0, if vectors are colineal 
                - 1, if vector2 is rotated anticlockwise with respect to the current vector
                - -1, if vector2 is rotated clockwise with respect to the current vector
        """

        vector1 = v2 - self
        vector2 = v3 - self
    
        det = np.linalg.det(np.column_stack([vector1.vector, vector2.vector]))


        if det < 0:
            if plotting:
                legend = ["clockwise"]
                self.plot_walk(v2, v3, legend = legend)

            return -1

        elif det > 0:
            if plotting:
                legend = ["anti-clockwise"]
                self.plot_walk(v2, v3, legend = legend)
            return 1

        return 0

    @staticmethod
    def direction(vector1: 'Vector', vector2: 'Vector', vector3: 'Vector') -> int:

        det = np.linalg.det(np.column_stack([(vector3 - vector1).vector, (vector2 - vector1).vector]))

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0

    @staticmethod
    def on_segment(v1: 'Vector', v2: 'Vector', v3: 'Vector') -> bool:
            
            """
                Checks if v3 is on the segment v1v2
            """
            inx = min(v1.vector[0][0], v2.vector[0][0]) <= v3.vector[0][0] <= max(v1.vector[0][0], v2.vector[0][0]) 
            iny = min(v1.vector[1][0], v2.vector[1][0]) <= v3.vector[1][0] <= max(v1.vector[1][0], v2.vector[1][0])

            if (inx and iny):
                return True
            return False

    @staticmethod
    def segments_intersect(v1: 'Vector', v2: 'Vector', v3: 'Vector', v4: 'Vector', plotting = False) -> bool:

        """
            
        """

        dir1 = Vector.direction(v3, v4, v1)
        dir2 = Vector.direction(v3, v4, v2)
        dir3 = Vector.direction(v1, v2, v3)
        dir4 = Vector.direction(v1, v2, v4)

        #well behaved case
        if (dir1*dir2 < 0) and (dir3*dir4 < 0):
            return True
    
        #collinear case
        elif (dir1 == 0) and (Vector.on_segment(v3, v4, v1)):
            return True

        elif (dir2 == 0) and (Vector.on_segment(v3, v4, v2)):
            return True

        elif (dir3 == 0) and (Vector.on_segment(v1, v2, v3)):
            return True

        elif (dir4 == 0) and (Vector.on_segment(v1, v2, v4)):
            return True
        
        else:
            return False
    
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

    def plot_walk(self, *vectors: 'Vector', legend = []):

        """
            Assumes there is a walk from self to the other vectors, 
            and its order is given by the order of the arguments.

            Plots the walk.
        """

        default_style = {"head_width": 0.1, "head_length": 0.1, "color": "g"}
        
        #the arrow from self to the second vector
        plt.arrow(self.vector[0][0], self.vector[1][0], (vectors[0] - self).vector[0][0], (vectors[0] - self).vector[1][0], **default_style)

        #now we plot the rest of the vectors
        for i in range(1, len(vectors)):
            plt.arrow(vectors[i-1].vector[0][0], vectors[i-1].vector[1][0], (vectors[i] - vectors[i-1]).vector[0][0], (vectors[i] - vectors[i-1]).vector[1][0], **default_style)
        
        #we set the limits of the plot
        norm = max([np.linalg.norm(v.vector) for v in vectors])
        plt.xlim(-1.1*norm, 1.1*norm)
        plt.ylim(-1.1*norm, 1.1*norm)
        plt.legend(legend)
        plt.show()


    #========================================
    #               Overloading
    #========================================
        
    def __add__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector + vector2.vector)
    
    def __sub__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector - vector2.vector)
    
    def __mul__(self, vector2: 'Vector') -> 'Vector':
        return Vector(self.vector * vector2.vector)

    def __str__(self):
        return f"{self.vector}"


