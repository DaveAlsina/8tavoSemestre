import numpy as np 
import matplotlib.pyplot as plt
from typing import Union, List

from vector import Vector
from segment import Segment

class VectorPlotter:

    def __init__(self):
        pass

    @staticmethod
    def plot(v1: Vector):
        plt.arrow(0, 0, v1.vector[0][0], v1.vector[1][0], head_width=0.1, head_length=0.1, color="g")
        norm = np.linalg.norm(v1.vector)
        plt.xlim(-2*norm, 2*norm)
        plt.ylim(-2*norm, 2*norm)
        plt.show()

    @staticmethod
    def plot_many(vectors: List[Vector],
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




class SegmentPlotter:

    def __init__(self):
        pass

    @staticmethod
    def plot(segment: Segment) -> None:
        plt.plot([segment.v0.vector[0][0], segment.v1.vector[0][0]], [segment.v0.vector[1][0], segment.v1.vector[1][0]])
        plt.scatter(segment.v0.vector[0][0], segment.v0.vector[1][0], color="g")
        plt.scatter(segment.v1.vector[0][0], segment.v1.vector[1][0], color="g")

        plt.show()
    
    @staticmethod
    def plot_many(segments: List[Segment], with_labels: bool=True) -> None:

        for i, segment in enumerate(segments):
            plt.plot([segment.v0.vector[0][0], segment.v1.vector[0][0]], [segment.v0.vector[1][0], segment.v1.vector[1][0]])
            plt.scatter(segment.v0.vector[0][0], segment.v0.vector[1][0], color="g")
            plt.scatter(segment.v1.vector[0][0], segment.v1.vector[1][0], color="g")

            if with_labels:
                #add text label on the middle of the segment
                middle = segment.get_midpoint()
                plt.text(middle.vector[0][0], middle.vector[1][0], f"S{i}")
        
        plt.show()