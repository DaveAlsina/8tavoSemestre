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
            plt.arrow(0, 0, v1.vector[0][0], v1.vector[1][0], head_width=0.1, head_length=0.1, color="g")
            norm = np.linalg.norm(v1.vector)
            plt.xlim(-2*norm, 2*norm)
            plt.ylim(-2*norm, 2*norm)
        elif highlighted:
            plt.scatter(v1.vector[0][0], v1.vector[1][0], color="b", s=30, marker="X")
            plt.text(v1.vector[0][0], v1.vector[1][0], f"V{v1.vector}")
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
                  title: str='') -> None:

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
                                     intersections: List[Union[Vector,Segment]],
                                     with_labels: bool=True, 
                                     title: str = '') -> None:
        
        fig = plt.figure()
        SegmentPlotter.plot_many(segments, with_labels=with_labels)
        
        #remove duplicates
        intersections = set(intersections)

        for i, intersection in enumerate(intersections):
            
            #plots a dotted line if the intersection is a segment, this line
            #has black color and no end points, it also shifts the line 
            #a little bit below
            if isinstance(intersection, Segment):
                print(f"INTERVAL intersect {intersection}")
                plt.plot([intersection.start.vector[0], intersection.end.vector[0]], [intersection.start.vector[1], intersection.end.vector[1]], color = 'k', linestyle="dotted")

                #add text label on the middle of the segment
                if with_labels:
                    middle = intersection.get_midpoint()
                    plt.text(middle.vector[0], middle.vector[1]-0.33, f"I{i}")

            #plots a red cross if the intersection is a vector
            elif isinstance(intersection, Vector):
                print(f"POINT intersect {intersection}")
                plt.scatter(intersection[0], intersection[1], color="r", marker="X")

                if with_labels:
                    plt.text(intersection[0], intersection[1]-0.33, f"P{i}")

        fig.text(0.5, -0.1, "I: Intervalos de Intersección\nP: Puntos de intersección\nS: Segmentos", ha="center")
        plt.title(title)