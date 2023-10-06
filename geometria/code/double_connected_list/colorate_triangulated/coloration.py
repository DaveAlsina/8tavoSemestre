import os, sys
import matplotlib as mpl
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
from double_connected_list.plot_double_connected_edge_list import PlotDoubleConnectedEdgeList


class TriangulationColoring:

    def __init__(self, semiedges: SemiEdgeList) -> None:
        self.semiedges = semiedges#deepcopy(semiedges)
        
        # a dictionary that contains the number of times that each color is used
        self.all_colors = [GeometricNode.COLOR1, GeometricNode.COLOR2, GeometricNode.COLOR3]
        self.color_count = dict([(color, 0) for color in self.all_colors])

        self.handling_problematic_node = False

    def breadth_first_search(self):

        nodes = self.update_queue()

        while nodes:#self.semiedges.list_of_nodes:
            
            node = nodes.pop(0)

            #if the node is already colored, then skip it
            if node.color is not None:
                continue

            #if the node is not colored, then color it
            else:
                
                #if the node is already colored, then skip it
                available_colors = self.check_neighboring_node(node)

                color = self.choose_color_from_available_colors(available_colors)
                #if there are available colors, then color the node
                if color is not None:
                    node.set_color(color)
                    self.update_node(node)

                    #update the queue by going from the node that has the least incident edges
                    #to the node that has the most incident edges
                    nodes = self.update_queue(True)
                
                #if there are no available colors, then raise an exception
                else:
                    #raise Exception("There are no available colors for coloring the node.")
                    print(f"\nThere are no available colors for coloring the node {node}.")
                    self.handle_problematic_node(node)

            print(f"Node {node} is colored with color {node.color}. color = {color}")
            print()

            #plot the current state
            if self.plotting:
                self.plot_current_state()

                
    def update_node(self, node: GeometricNode) -> None:

        #get the incident edges of the node
        incident_edges = self.semiedges.get_incident_edges_of_vertex(node)

        #update the color of the node in each incident edge
        for incident_edge in incident_edges:
            incident_edge.origin = node

    def update_queue(self, sorting_type: bool = False) -> List[GeometricNode]:
        """
            This method updates the queue of the nodes that are not colored.
            The queue is updated by sorting the nodes by the number of incident edges.
        """

        self.handling_problematic_node = False

        #get the nodes that are not colored
        uncolored_nodes = [node for node in self.semiedges.list_of_nodes if node.color is None]

        #sort the nodes by the number of incident edges
        uncolored_nodes.sort(key=lambda x: len(self.semiedges.get_incident_edges_of_vertex(x)), reverse=sorting_type)

        #update the queue
        return uncolored_nodes

    def handle_problematic_node(self, node: GeometricNode) -> None:

        #get the incident edges of the node
        incident_edges = self.semiedges.get_incident_edges_of_vertex(node)

        #erase the color of the node in each incident edge
        for incident_edge in incident_edges:
            incident_edge.next_.set_color(None)
            self.update_node(incident_edge.next_)

        #build a queue of the next nodes of the incident edges
        queue = [incident_edge.next_ for incident_edge in incident_edges]

        #sort the queue by the number of incident edges
        queue.sort(key=lambda x: len(self.semiedges.get_incident_edges_of_vertex(x)), reverse=True)

        #color each node in the queue with the first available color
        while queue:
            node = queue.pop(0)

            available_colors = self.check_neighboring_node(node)
            color = self.choose_color_from_available_colors(available_colors)

            node.set_color(color)
            self.update_node(node)


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

            #build a sub-dictionary that contains only the available colors
            available_color_count = dict([(color, self.color_count[color]) for color in available_colors])

            #find the color that is used the least
            color = max(available_color_count, key=available_color_count.get)

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
        
        print(f"\nAnalizing node = {node}")
        #available colors
        colors = set([GeometricNode.COLOR1, GeometricNode.COLOR2, GeometricNode.COLOR3])

        #edges that are originating from the node
        incident_edges = self.semiedges.get_incident_edges_of_vertex(node)

        #used colors
        used_colors = set()

        for incident_edge in incident_edges:
            print(f"incident_edge = {incident_edge}, next node color = {incident_edge.next_.color}")
            used_colors.add(incident_edge.next_.color)

        print(f"used_colors = {used_colors}")

        #available colors
        available_colors = colors - used_colors

        print(f"available_colors = {available_colors}")
            
        return list(available_colors)


    def run(self, plotting: bool = False) -> SemiEdgeList:
        """
            This method runs the coloring algorithm.

            Output:
            -------------------
                semiedges: SemiEdgeList
                    The colored nodes of the semiedge list.
        """

        #plot the current state
        self.plotting = plotting
        print(f"\n\nStarting the coloration algorithm...")

        #color the nodes
        self.breadth_first_search()

        return self.semiedges

    def plot_current_state(self, cmap = 'viridis'):
        PlotDoubleConnectedEdgeList.plot(self.semiedges)

        colormap = mpl.colormaps[cmap].resampled(50)
        main_colors = [colormap(0.33), colormap(0.66), colormap(0.99)]

        #plot the colors of the nodes
        for node in self.semiedges.list_of_nodes:
            
            if node.color is not None:
                color = main_colors[node.color]
                plt.scatter(node.x, node.y, color=color, s=40)

        plt.show()
