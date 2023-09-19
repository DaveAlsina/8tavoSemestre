import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import matplotlib.pyplot as plt
from typing import List, Union, Tuple

from double_connected_segments import SemiEdgeList

class PlotDoubleConnectedEdgeList():

    def __init__(self) -> None:
        pass

    @staticmethod
    def plot(semiedges: SemiEdgeList,
             color: str = 'black',
             linewidth: float = 1.0,
             alpha: float = 1.0) -> None:

        #a plot for each semi-edge, it's an arrow from the start to the end
        #of the semi-edge, dashed line, also plotting the twin of this semi-edge
        #a little bit to the left and with less alpha
        for semiedge in semiedges:
            
            dx = semiedge.end[0] - semiedge.start[0]
            dy = semiedge.end[1] - semiedge.start[1]
            dxtwin = semiedge.twin.end[0] - semiedge.twin.start[0]
            dytwin = semiedge.twin.end[1] - semiedge.twin.start[1]
            offset = 0.05
            
            plt.arrow(semiedge.start[0], semiedge.start[1],
                      dx, dy,
                      color = color, linewidth = linewidth, alpha = alpha,
                      length_includes_head = True, head_width = 0.1)
            
            #a little bit to the left and with half the alpha, dashed line
            plt.arrow(semiedge.twin.start[0]+offset, semiedge.twin.start[1],
                      dxtwin+offset, dytwin,
                      color = 'red', linewidth = linewidth, alpha = alpha/3,
                      length_includes_head = True, head_width = 0.1, linestyle = '--')

            #add name of the vextex to the plot
            plt.text(semiedge.start[0],
                     semiedge.start[1]+2*offset,
                     semiedge.origin.name,
                     fontsize = 10)

    @staticmethod
    def show() -> None:
        plt.show()
        