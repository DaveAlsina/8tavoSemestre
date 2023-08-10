import numpy as np 
from matplotlib import pyplot as plt
from base import Vector

class SwissArmyKnifePlotting:

    def __init__(self):
        pass

    #========================================
    #               Plotting
    #========================================
    
    @staticmethod
    def plot(v1: Vector):
        plt.arrow(0, 0, v1.vector[0][0], v1.vector[1][0], head_width=0.1, head_length=0.1, color="g")
        norm = np.linalg.norm(v1.vector)
        plt.xlim(-2*norm, 2*norm)
        plt.ylim(-2*norm, 2*norm)
        plt.show()
    
    @staticmethod
    def plot_many(*vectors: Vector,
                   highlighted: list = [],
                   with_arrows: bool = False,
                   with_labels: bool = False):

        for i, vector in enumerate(vectors):
            if with_arrows:
                plt.arrow(0, 0, vector.vector[0][0], vector.vector[1][0], head_width=0.1, head_length=0.1, color="g")
            else: 
                plt.scatter(vector.vector[0][0], vector.vector[1][0], color="g")

            if with_labels:
                plt.text(vector.vector[0][0], vector.vector[1][0], f"v{i}")


        for vector in highlighted:
            plt.scatter(vector.vector[0][0], vector.vector[1][0], color="r")

        norm = max([np.linalg.norm(v.vector) for v in vectors])

        plt.xlim(-2*norm, 2*norm)
        plt.ylim(-2*norm, 2*norm)
        plt.show()
