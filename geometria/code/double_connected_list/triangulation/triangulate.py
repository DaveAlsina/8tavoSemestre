import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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


#custom plotting imports
from plot_double_connected_edge_list import PlotDoubleConnectedEdgeList

CHAIN1 = 1
CHAIN2 = 2

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
        self.vertex_stack: List[Tuple[GeometricNode, SemiEdge]] = []
        self.curr_iter: int = 0
        self.endpoints: List[Tuple[GeometricNode, SemiEdge]] = []
        self.diagonals: List[SemiEdge] = []


    def convert_to_ymonotone(self, plotting: bool = False):
        """
            Converts the polygon into a y-monotone polygon.
        """
        diagonals: List[SemiEdge] = SweepLineMonotonePoly(self.semiedges).run(plotting=plotting)
        self.semiedges.add_new_semi_edges(diagonals)

    def get_vertex_chain(self, endpoint: GeometricNode, semiedge: SemiEdge) -> bool:
        """
            Get the chain associated with the endpoint.
        """
        #two vertexes are on the same chain if they have the same orientation 
        #meaning: if v1 <= v2 <= v3 and v4 <= v5 <= v6, you would say that v2 and v5 
        #are on the same chain
        next_ = semiedge.next_
        prev_ = semiedge.prev_edge.origin
        
        return prev_ < endpoint < next_

    def is_interior_diagonal(self, diagonal: SemiEdge, main_edge: SemiEdge) -> bool:
        """
            Check if the diagonal is an interior diagonal or not.
        """

        #check the turn we would have to do from the incident edge to the diagonal
        #if we were to add it 
        turn = main_edge.seg.direction(diagonal.end)

        #if the turn is a left turn, then the diagonal is an interior diagonal
        if (turn == 1) or (turn == 0):
            return True
        return False

    def sort_endpoints(self, semiedges) -> List[Tuple[GeometricNode, SemiEdge]]:

        """
            Sort the endpoints of the segments in the lexigraphical order.
                        
            Returns:
            -----------
                A list of tuples, where each tuple contains the endpoint, the semiedge that contains the endpoint as 
                origin, and the type of endpoint.
        """
        semiedges_ = deepcopy(semiedges)
        endpoints = []

        for i in range(len(semiedges_)):
            semiedge = semiedges_[i]
            origin = semiedge.origin

            endpoints.append((origin, semiedge))
            
        #drop the duplicates if any
        endpoints = list(set(endpoints))

        # sort by using the vector own comparison methods
        endpoints.sort(key=lambda endpoint_tuple: endpoint_tuple[0])
        return endpoints


    def handle_different_chains(self, endpoint: GeometricNode, semiedge: SemiEdge):
        print("Handling different chains")
        print(f"Endpoint: {endpoint}, Semiedge: {semiedge}")
        print(f"Vertex stack: {self.vertex_stack}")
        
        #pop the all the vertices in the stack
        #insert a new diagonal from the ith endpoint to each popped vertex, except the last one,
        #push the (ith - 1) endpoint and the ith endpoint into the stack
        diagonals = []

        while self.vertex_stack:

            #pop the vertex
            vertex, s = self.vertex_stack.pop()

            #get the diagonal from the ith endpoint to the popped vertex
            diagonal = SemiEdge(endpoint, vertex)
            
            #insert the diagonal into the semiedge list iif it's not the last vertex
            if  self.vertex_stack: 
                diagonals.append(diagonal)

        #insert these diagonals into the semiedge list.
        #self.semiedges.add_new_semi_edges(diagonals)
        self.diagonals.extend(diagonals)

        #push the (ith - 1) endpoint and the ith endpoint into the stack
        #get the index of the current endpoint in the semiedge list
        self.vertex_stack.append(self.endpoints[self.curr_iter - 1])
        self.vertex_stack.append((endpoint, semiedge))


    def handle_same_chain(self, endpoint: GeometricNode, semiedge: SemiEdge):
        print("Handling same chain")
        print(f"Endpoint: {endpoint}, Semiedge: {semiedge}")
        print(f"Vertex stack: {self.vertex_stack}")

        diagonals = []
        
        #keep track of the last vertex which lead to an interior diagonal
        #that was inserted into the diagonals list, this is useful for
        #insering this vertex back into the stack when we're done
        last_inserted: Tuple[GeometricNode, SemiEdge] = ()

        #pop the first vertex
        vertex, s = self.vertex_stack.pop()
        
        #get the diagonal from the 1st endpoint to the popped vertex
        diagonal = SemiEdge(endpoint, vertex)

        #pop the other vertices in the stack as long as the diagonals from the ith endpoint to the
        #popped vertices are inside the polygon.
        while self.vertex_stack and (self.is_interior_diagonal(diagonal, semiedge)):

            #if the diagonal is an interior diagonal and it's not in the diagonals list
            if diagonal not in diagonals:
                #insert the diagonal into the semiedge list
                print(f"Diagonal inserted: {diagonal}")
                diagonals.append(diagonal)
                last_inserted = (vertex, s)

            #pop the vertex
            vertex, s = self.vertex_stack.pop()

            #get the diagonal from the ith endpoint to the popped vertex
            diagonal = SemiEdge(endpoint, vertex)

        #push the last vertex back into the stack 
        # (because it was popped in the while loop but not inserted into the diagonals list)
        self.vertex_stack.append((vertex, s))

        #remove the duplicates from the diagonals list
        self.diagonals.extend(diagonals)

        #insert these diagonals into the semiedge list. 
        #self.semiedges.add_new_semi_edges(diagonals)

        #push the last_inserted vertex into the stack
        if last_inserted:
            self.vertex_stack.append(last_inserted)

        #push the ith endpoint into the stack
        self.vertex_stack.append((endpoint, semiedge))


    def run(self, plotting: bool = False, plotting_monotone: bool = False) -> Tuple[SemiEdgeList, List[SemiEdge]]:
        """
            Apply the triangulation algorithm to the polygon.
        """

        self.plotting = plotting

        #convert the polygon into a y-monotone polygon
        print("Converting to y-monotone...")
        self.convert_to_ymonotone(plotting=plotting_monotone)
        print("="*50)
        print("*"*50)
        print("="*50)

        #triangulate the y-monotone polygon
        #by triangulating each face
        for face in self.semiedges.faces:

            if face.face_type == Face.INTERIOR_FACE:
                continue

            #keep track of the current face
            self.curr_face = face
            self.curr_iter = 0

            #sort the endpoints associated to the segments of the face in the lexigraphical order
            self.endpoints = self.sort_endpoints(face.semi_edges)

            #insert the first two vertices into the stack
            self.vertex_stack = [self.endpoints[0], self.endpoints[1]]

            print(f"Computing triangulation for Face: {face}")
            print("Initial state: ")
            print(f"Vertex stack: {self.vertex_stack}")
            print(f"Endpoints: {self.endpoints}\n")


            #plot the current state
            if plotting:
                plt.title(f"Initial state, NEW FACE: {face}")
                self.plot_current_state()

            #for each endpoint
            for i in range(2, len(self.endpoints)-1):
                
                #keep track of the current iteration
                self.curr_iter = i
                
                chain_endpoint = self.get_vertex_chain(*self.endpoints[i])
                chain_stack_top = self.get_vertex_chain(*self.vertex_stack[-1])

                if plotting:
                    plt.title("Before handling the endpoint")
                    self.plot_current_state()

                #if the ith endpoint is in a different chain from the endpoint in top of the stack
                if chain_endpoint != chain_stack_top:
                    self.handle_different_chains(*self.endpoints[i])
                #otherwise
                else:
                    self.handle_same_chain(*self.endpoints[i])
                
                print(f"Vertex stack: {self.vertex_stack}")
                print()

                if plotting:
                    plt.title("After handling the endpoint")
                    self.plot_current_state()
            
            #add diagonals from the last endpoint to all the vertices in the stack, except the first one
            #and the last one
            diagonals = []

            #update the current iteration
            self.curr_iter = len(self.endpoints) - 1

            for i in range(1, len(self.vertex_stack) - 1):
                vertex, semiedge = self.vertex_stack[i]
                diagonal = SemiEdge(self.endpoints[-1][0], vertex)
                diagonals.append(diagonal)

                if plotting:
                    plt.title("Handling the last endpoint, adding the last diagonals")
                    self.plot_current_state()
                    plt.pause(5)

            #self.semiedges.add_new_semi_edges(diagonals)
            self.diagonals.extend(diagonals)

        return self.semiedges, self.diagonals


    def plot_current_state(self):
        PlotDoubleConnectedEdgeList.plot(self.semiedges)
        
        #plot the current face in orange
        for semiedge in self.curr_face.semi_edges:
            plt.plot([semiedge.seg.start[0], semiedge.seg.end[0]], 
                     [semiedge.seg.start[1], semiedge.seg.end[1]], color="orange")

        #plot the diagonals in red
        for diagonal in self.diagonals:
            #use diagonal.seg.start and diagonal.seg.end 
            plt.plot([diagonal.seg.start[0], diagonal.seg.end[0]], 
                     [diagonal.seg.start[1], diagonal.seg.end[1]], color="red")

        #plot the current endpoint in green as a square
        plt.scatter(self.endpoints[self.curr_iter][0].x, self.endpoints[self.curr_iter][0].y, color="green", marker="s")

        #plot the current top vertex stack in blue, as a square
        plt.scatter(self.vertex_stack[-1][0].x, self.vertex_stack[-1][0].y, color="red", marker="s")


        plt.show()