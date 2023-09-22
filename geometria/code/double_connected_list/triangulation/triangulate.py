import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#standard imports
from copy import deepcopy
from typing import List, Tuple
from matplotlib import pyplot as plt


#custom imports
from base import Vector, Segment
from sweep_line_to_monotone_polygon import SweepLineMonotonePoly
from double_connected_list.face import Face
from double_connected_list.geometric_node import GeometricNode
from double_connected_list.double_connected_segments import SemiEdge, SemiEdgeList

class Triangulate():

    """
        Given an arbitrary polygon, this class triangulates it.
        For this process first we need to convert the polygon into a y-monotone polygon.
        And then Apply the triangulation algorithm, defined inside this class.

        Attributes:
            semiedges: A SemiEdgeList object that represents the polygon to be triangulated.
    """


    def __init__(self, semiedges: SemiEdgeList):

        self.semiedges: SemiEdgeList = deepcopy(semiedges)
        self.vertex_stack: List[GeometricNode] = []


    def convert_to_ymonotone(self):
        """
            Converts the polygon into a y-monotone polygon.
        """
        diagonals: List[SemiEdge] = SweepLineMonotonePoly(self.semiedges).run(plotting=False)
        self.semiedges.add_new_semi_edges(diagonals)

    def get_vertex_chain(self, endpoint: GeometricNode, semiedge: SemiEdge) -> Face:
        """
            Get the chain associated with the endpoint.
        """
        pass

    def is_interior_diagonal(self, semiedge: SemiEdge) -> bool:
        """
            Check if the diagonal is an interior diagonal or not.
        """
        pass

    def merge_left_right_vertices(self) -> List[GeometricNode]:
        """
            Merge the vertices on th left chain and the vertices on the right chain of 
            the polygon, described by the semiedge list, into one sequence of vertices.
        """
        pass

    def sort_endpoints(self) -> List[Tuple[GeometricNode, SemiEdge]]:

        """
            Sort the endpoints of the segments in the lexigraphical order.
                        
            Returns:
            -----------
                A list of tuples, where each tuple contains the endpoint, the semiedge that contains the endpoint as 
                origin, and the type of endpoint.
        """
        endpoints = []

        for i in range(len(self.semiedges)):
            semiedge = self.semiedges[i]
            origin = semiedge.origin

            endpoints.append((origin, semiedge))
            
        # sort by using the vector own comparison methods
        endpoints.sort(key=lambda endpoint_tuple: endpoint_tuple[0])
        return endpoints


    def handle_different_chains(self, endpoint: GeometricNode, semiedge: SemiEdge):
        #pop the all the vertices in the stack
        #insert a new diagonal from the ith endpoint to each popped vertex, except the last one
        #push the (ith - 1) endpoint and the ith endpoint into the stack
        pass

    def handle_same_chain(self, endpoint: GeometricNode, semiedge: SemiEdge):

        #pop the other vertices in the stack as long as the diagonals from the ith endpoint to the
        #popped vertices are inside the polygon.

        #insert these diagonals into the semiedge list. 

        #push the last vertex that has been popped back onto the stack.

        #push the ith endpoint into the stack.

        pass

    def run(self):
        """
            Apply the triangulation algorithm to the polygon.
        """

        #convert the polygon into a y-monotone polygon
        self.convert_to_ymonotone()

        #sort the endpoints of the segments in the lexigraphical order
        endpoints = self.sort_endpoints()

        #insert the first two vertices into the stack
        self.vertex_stack = [endpoints[0], endpoints[1]]

        #for each endpoint
        for i in range(2, len(endpoints)):
            
            #if the ith endpoint is in a different chain from the endpoint in top of the stack
            self.handle_different_chains(*endpoints[i])


            #otherwise
            self.handle_same_chain(*endpoints[i])
            
        #add diagonals from the last endpoint to all the vertices in the stack, except the first one
        #and the last one