import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

#standard imports
from copy import deepcopy
from typing import List, Tuple
from matplotlib import pyplot as plt


#custom imports
from double_connected_list.face import Face
from double_connected_list.geometric_node import GeometricNode
from double_connected_list.double_connected_segments import SemiEdge, SemiEdgeList


class TriangulationColoring:

    def __init__(self, semiedges: SemiEdgeList) -> None:
        self.semiedges = deepcopy(semiedges)
        
        # a dictionary that contains the number of times that each color is used
        self.all_colors = [GeometricNode.COLOR1, GeometricNode.COLOR2, GeometricNode.COLOR3]
        self.color_count = dict([(color, 0) for color in self.all_colors])

    def breadth_first_search(self):

        for node in self.semiedges.list_of_nodes:
            
            #if the node is already colored, then skip it
            available_colors = self.check_neighboring_node(node)

            #if the node is already colored, then skip it
            if node.color is not None:
                continue

            #if the node is not colored, then color it
            else:
                self.choose_color_from_available_colors(available_colors)


                
    def choose_color_from_available_colors(self, available_colors: List[int]) -> int:
        """
            This method chooses a color from the available colors.
            If there are no available colors, then it returns None.

            For choosing the color, we use the following strategy:
                1. If there is only one available color, then choose that color.
                2. If there is more than one available color, then choose the color
                   that is used the least.

            Input:
            -------------------
                available_colors: List[int]
                    The available colors.

            Output:
            -------------------
                color: int
                    The chosen color.
        """

        #if there are no available colors, then return None
        if len(available_colors) == 0:
            return None

        #if there is only one available color, then choose that color
        if len(available_colors) == 1:
            return available_colors[0]

        #if there is more than one available color, then choose the color that is used the least
        else:

            #find the color that is used the least
            color = min(self.color_count, key=self.color_count.get)

            #increase the color count
            self.color_count[color] += 1

            return color
                    
    def check_neighboring_node(self, node: GeometricNode) -> List[int]:
        """
            This method checks the neighboring nodes of the given node and returns
            a list of available colors, for coloring the input node.
            The available colors are the colors that are not used by the neighboring nodes.

            Input:
            -------------------
                node: GeometricNode
                    The node that we want to color.

            Output:
            -------------------
                available_colors: List[int]
                    The available colors for coloring the input node.
        """
        
        #available colors
        colors = set([GeometricNode.COLOR1, GeometricNode.COLOR2, GeometricNode.COLOR3])

        #edges that are originating from the node
        incident_edges = self.semiedges.get_incident_edges_of_vertex(node)

        #used colors
        used_colors = set()

        for incident_edge in incident_edges:
            used_colors.add(incident_edge.origin.color)

        #available colors
        available_colors = colors - used_colors
            
        return list(available_colors)


