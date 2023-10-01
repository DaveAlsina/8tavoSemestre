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

            #add name of the semi-edge to the plot, in the middle of the semi-edge and a little bit 
            #to the right of the semi-edge, in purple
            semiedge_center = [(semiedge.start[0] + semiedge.end[0])/2, (semiedge.start[1] + semiedge.end[1])/2]

            plt.text( semiedge_center[0] + offset,
                      semiedge_center[1] + 0,
                       semiedge.name,
                       fontsize = 10,
                       color = 'purple')


        #plot the faces
        if semiedges.faces:
            PlotDoubleConnectedEdgeList.plot_faces(semiedges)

    

    @staticmethod
    def plot_faces(semiedges: SemiEdgeList):
        offset = 0.05

        for face in semiedges.faces:

            #calculate the center of the face
            #the center is the average of the coordinates of the vertices of the face

            center = [0, 0]
            for semiedge in face.semi_edges:
                center[0] += semiedge.origin.x
                center[1] += semiedge.origin.y
            
            center[0] /= len(face.semi_edges)
            center[1] /= len(face.semi_edges)

            #plot the center of the face
            plt.scatter(center[0], center[1], color = 'blue', s = 40)
            plt.text(center[0], center[1]+offset, face.name, fontsize = 10)


    @staticmethod
    def show() -> None:
        plt.show()
        