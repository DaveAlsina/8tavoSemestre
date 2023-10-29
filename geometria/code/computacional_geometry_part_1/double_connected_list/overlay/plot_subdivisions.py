from typing import List, Union
import matplotlib.pyplot as plt
from double_connected_segments import SemiEdgeList
from base import Vector


class PlotSubdivisions():

    epsilon = 0.15
    def __init__(self):
        pass


    @staticmethod
    def plot(subdivision: SemiEdgeList, 
             color: str = 'black',
             linewidth: float = 1.0,
             alpha: float = 1.0,
             label: str = None) -> None:
        """
            This method plots a subdivision.
        """

        for semiedge in subdivision.semi_edges:
            plt.plot([semiedge.seg.start[0], semiedge.seg.end[0]],
                     [semiedge.seg.start[1], semiedge.seg.end[1]],
                     color=color,
                     linewidth=linewidth,
                     alpha=alpha)
        
        plt.scatter([node.point[0] for node in subdivision.list_of_nodes],
                    [node.point[1] for node in subdivision.list_of_nodes],
                    color=color,
                    alpha=alpha,)

        #adds text to the points, with the geometric node name atribute 
        for node in subdivision.list_of_nodes:
            plt.text(node.point[0], node.point[1] + PlotSubdivisions.epsilon, f"{node.name}", 
                     fontsize=8, color=color, alpha=alpha)
            

        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.25)

    def plot_many(subdivisions: List[SemiEdgeList],
                  intersection_points: List[Vector] = None,
                  colors: List[str] = ['black'],
                  linewidths: List[float] = [1.0],
                  alphas: List[float] = [0.5],) -> None:

        """
            This method plots many subdivisions.
        """

        if len(colors) != len(subdivisions):
            colors = colors * len(subdivisions)
        
        if len(linewidths) != len(subdivisions):
            linewidths = linewidths * len(subdivisions)
        
        if len(alphas) != len(subdivisions):
            alphas = alphas * len(subdivisions)


        for i, subdivision in enumerate(subdivisions):
            PlotSubdivisions.plot(subdivision=subdivision,
                                  color=colors[i],
                                  linewidth=linewidths[i],
                                  alpha=alphas[i])

        if intersection_points:
            plt.scatter([point[0] for point in intersection_points],
                        [point[1] for point in intersection_points],
                        color='red',
                        alpha=0.25)
        
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.25)


    @staticmethod
    def show() -> None:
        """
            This method shows the plot.
        """
        plt.show()

