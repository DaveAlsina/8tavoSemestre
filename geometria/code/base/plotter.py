import numpy as np 
import matplotlib.pyplot as plt
from typing import Union, List

from vector import Vector
from segment import Segment

plt.rcParams["figure.autolayout"] = True

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
            plt.arrow(0, 0, v1[0], v1[1], head_width=0.1, head_length=0.1, color="g")
            norm = np.linalg.norm(v1.vector)
            plt.xlim(-1*norm, 1*norm)
            plt.ylim(-1*norm, 1*norm)
        elif highlighted:
            plt.scatter(v1[0], v1[1], color="b", s=30, marker="X")
            plt.text(v1[0], v1[1], f"V{v1.vector}")
        else:
            plt.scatter(v1[0], v1[1], color="b", s=20)
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
                plt.arrow(0, 0, vector[0], vector[1], head_width=0.1, head_length=0.1, color="g")
            else: 
                plt.scatter(vector[0], vector[1], color="g", s=7)

            if with_labels:
                plt.text(vector[0], vector[1], f"v{i}")


        for vector in highlighted:
            #marker is a cross sign 
            plt.scatter(vector[0], vector[1], color="b", s=20, marker="X")

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
        plt.plot([segment.start[0], segment.end[0]], [segment.start[1], segment.end[1]])
        plt.scatter(segment.start[0], segment.start[1], color="g")
        plt.scatter(segment.end[0], segment.end[1], color="g")

    
    @staticmethod
    def plot_many(segments: List[Segment],
                  with_labels: bool=True, 
                  title: str='') -> None:

        left = min([min([seg.start[0], seg.end[0]]) for seg in segments])
        right = max([max([seg.start[0], seg.end[0]]) for seg in segments])
        up = max([max([seg.start[1], seg.end[1]]) for seg in segments])
        down = min([min([seg.start[1], seg.end[1]]) for seg in segments])

        plt.xlim(left-1, right+1)
        plt.ylim(down-1, up+1)

        for i, segment in enumerate(segments):
            plt.plot([segment.start[0], segment.end[0]], [segment.start[1], segment.end[1]])
            plt.scatter(segment.start[0], segment.start[1], color="g")
            plt.scatter(segment.end[0], segment.end[1], color="g")

            if with_labels:
                #add text label on the middle of the segment
                middle = segment.get_midpoint()
                plt.text(middle[0], middle[1], f"S{i}")
            
        plt.title(title)

    @staticmethod
    def plot_many_with_intersections(segments: List[Segment],
                                     intersections: List[Vector],
                                     with_labels: bool=True, 
                                     title: str = '') -> None:
        
        fig = plt.figure()
        SegmentPlotter.plot_many(segments, with_labels=with_labels)
        
        #remove duplicates
        intersections = list(set(intersections))

        for i, intersection in enumerate(intersections):

            plt.scatter(intersection[0], intersection[1], color="r", marker="X")
            if with_labels:
                plt.text(intersection[0], intersection[1]-0.33, f"P{i}")

        fig.text(0.5, -0.1, "I: Intervalos de Intersección\nP: Puntos de intersección\nS: Segmentos", ha="center")
        plt.title(title)