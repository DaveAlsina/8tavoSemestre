import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Union, Tuple
import matplotlib.pyplot as plt

from base import Vector
from double_connected_list.double_connected_segments import SemiEdge, SemiEdgeList
from constants import START_VERTEX, END_VERTEX, SPLIT_VERTEX, MERGE_VERTEX, REGULAR_VERTEX


class PlotMonotonePolygon():


    def __init__(self):
        pass

    @staticmethod
    def plot_polygon(semiedges: SemiEdgeList,
                     color: str = 'black',
                     linewidth: float = 1.0,
                     alpha: float = 1.0,
                     s: float = 40,
                     classifications: List[Tuple[Vector, SemiEdge, str]] = None) -> None:

        for semiedge in semiedges:
            plt.plot([semiedge.seg.start[0], semiedge.seg.end[0]],
                     [semiedge.seg.start[1], semiedge.seg.end[1]],
                      color=color,
                      linewidth=linewidth,
                      alpha=alpha)
        
        for vec, semiedge, classification in classifications:

            # normal black point if it's a regular vertex
            if classification == REGULAR_VERTEX:
                plt.scatter(vec[0], vec[1], color='black', s=s, alpha=3*alpha/4)
            
            # empty square if it's a start vertex, on yellow
            elif classification == START_VERTEX:
                plt.scatter(vec[0], vec[1], color='black', s=s, marker='P', alpha=alpha)
            
            # filled square if it's a end vertex, on orange
            elif classification == END_VERTEX:
                plt.scatter(vec[0], vec[1], color='black', s=s, marker='X', alpha=alpha)
            
            # triangle pointing up if it's a split vertex, on green
            elif classification == SPLIT_VERTEX:
                plt.scatter(vec[0], vec[1], color='green', s=s, marker='^', alpha=alpha)
            
            # triangle pointing down if it's a merge vertex, on red
            elif classification == MERGE_VERTEX:
                plt.scatter(vec[0], vec[1], color='red', s=s, marker='v', alpha=alpha)
        

    @staticmethod
    def show() -> None:
        plt.show()
        
