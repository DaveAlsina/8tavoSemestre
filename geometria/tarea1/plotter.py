import numpy as np 
import matplotlib.pyplot as plt
from typing import Union, List

from vector import Vector
from segment import Segment

class VectorPlotter:

    def __init__(self):
        """
            This class is used to plot vectors.
        """
        pass

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def plot(v1: Vector, arrow: bool = False, highlighted: bool = False) -> None:
        
        if arrow:
            plt.arrow(0, 0, v1.vector[0][0], v1.vector[1][0], head_width=0.1, head_length=0.1, color="g")
            norm = np.linalg.norm(v1.vector)
            plt.xlim(-2*norm, 2*norm)
            plt.ylim(-2*norm, 2*norm)
        elif highlighted:
            plt.scatter(v1.vector[0][0], v1.vector[1][0], color="b", s=30, marker="X")
            plt.text(v1.vector[0][0], v1.vector[1][0], f"V")
        else:
            plt.scatter(v1.vector[0][0], v1.vector[1][0], color="b", s=20)
            norm = np.linalg.norm(v1.vector)
            plt.xlim(-1*norm, 1*norm)
            plt.ylim(-1*norm, 1*norm)


    @staticmethod
    def plot_many(vectors: List[Vector],
                   highlighted: list = [],
                   with_arrows: bool = False,
                   with_labels: bool = False):

        for i, vector in enumerate(vectors):
            if with_arrows:
                plt.arrow(0, 0, vector.vector[0][0], vector.vector[1][0], head_width=0.1, head_length=0.1, color="g")
            else: 
                plt.scatter(vector.vector[0][0], vector.vector[1][0], color="g", s=7)

            if with_labels:
                plt.text(vector.vector[0][0], vector.vector[1][0], f"v{i}")


        for vector in highlighted:
            #marker is a cross sign 
            plt.scatter(vector.vector[0][0], vector.vector[1][0], color="b", s=20, marker="X")

        norm = max([np.linalg.norm(v.vector) for v in vectors])

        plt.xlim(-1*norm, 1*norm)
        plt.ylim(-1*norm, 1*norm)




class SegmentPlotter:

    def __init__(self):
        """
            This class is used to plot segments.
        """
        pass

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def plot(segment: Segment) -> None:
        plt.plot([segment.start.vector[0][0], segment.end.vector[0][0]], [segment.start.vector[1][0], segment.end.vector[1][0]])
        plt.scatter(segment.start.vector[0][0], segment.start.vector[1][0], color="g")
        plt.scatter(segment.end.vector[0][0], segment.end.vector[1][0], color="g")

    
    @staticmethod
    def plot_many(segments: List[Segment],
                  with_labels: bool=True, 
                  title: str = '') -> None:

        left = min([min([seg.start[0], seg.end[0]]) for seg in segments])
        right = max([max([seg.start[0], seg.end[0]]) for seg in segments])
        up = max([max([seg.start[1], seg.end[1]]) for seg in segments])
        down = min([min([seg.start[1], seg.end[1]]) for seg in segments])

        plt.xlim(left-1, right+1)
        plt.ylim(down-1, up+1)

        for i, segment in enumerate(segments):
            plt.plot([segment.start.vector[0][0], segment.end.vector[0][0]], [segment.start.vector[1][0], segment.end.vector[1][0]])
            plt.scatter(segment.start.vector[0][0], segment.start.vector[1][0], color="g")
            plt.scatter(segment.end.vector[0][0], segment.end.vector[1][0], color="g")

            if with_labels:
                #add text label on the middle of the segment
                middle = segment.get_midpoint()
                plt.text(middle.vector[0][0], middle.vector[1][0], f"S{i}")
        
        plt.title(title)

    @staticmethod
    def plot_many_with_intersections(segments: List[Segment],
                                     intersections: List[Vector],
                                     with_labels: bool=True, 
                                     title: str = '') -> None:
        
        SegmentPlotter.plot_many(segments, with_labels=with_labels)

        for i, intersection in enumerate(intersections):
            plt.scatter(intersection.vector[0][0], intersection.vector[1][0], color="r", marker="X")
            if with_labels:
                plt.text(intersection.vector[0][0], intersection.vector[1][0], f"I{i}")

        plt.title(title)