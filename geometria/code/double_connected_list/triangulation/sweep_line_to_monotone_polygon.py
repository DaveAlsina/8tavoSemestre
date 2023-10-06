# add path with sys
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# standard imports
import bisect
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
from typing import Union, List, Tuple

# custom dependencies
from base.vector  import  Vector
from base.segment import  Segment
from binary_tree import Tree, Node1D

from double_connected_list.geometric_node import GeometricNode
from double_connected_list.double_connected_segments import SemiEdge, SemiEdgeList
from constants import START_VERTEX, END_VERTEX, SPLIT_VERTEX, MERGE_VERTEX, REGULAR_VERTEX
from plot_triangulation import PlotMonotonePolygon


class SweepLineMonotonePoly:

    def __init__(self, semiedges: SemiEdgeList, epsilon: float = 1e-5):

        """
            Implement use sweepline abstraction to Make any polygon a monotone polygon.

            Args:
                segments: list of segments to be processed.
        """

        self.semiedges = semiedges#deepcopy(semiedges)
        self.epsilon  = epsilon
        self.status_tree : Tree[Node1D]   = None 
        self.event_points : List[Vector]  = None 
        self.sorted_status : List[Node1D] = None 
        self.diagonals : List[SemiEdge] = [] 

        #to keep track of the number of event points processed
        self.count: int = 0
        
        #to ensure that we do not add a semiedge that has already been removed
        self.removed_semiedges: List[SemiEdge] = []

        #to set the sweepline width in the x axis
        self.leftmost_endpoint : Vector  = None 
        self.rightmost_endpoint : Vector = None 

        #to keep track of the event points
        self.sweep_line : Segment = None 

    def update_sweepline(self, y, type_: str) -> None:

        """
            Update the sweepline to the height y. 
            If type_ is "intersection" then we update the sweepline to the height y - epsilon, 
            which is equivalent to check a little bit below the intersection.
            Otherwise we update the sweepline to the height y.
            
            Args:
            -----------
                y: height of the sweepline.
                type_: type of endpoint, whether it's a start, end (vertex) 
                or intersection endpoint (intersection).
        """

        xleft = self.leftmost_endpoint[0] - 1
        xright = self.rightmost_endpoint[0] + 1

        if type_ == "intersection":
            y = y - self.epsilon

        # build the sweepline, from leftmost to rightmost points in the x axis
        # at height y, and tilt a little bit on the right end of the sweepline
        # in order to avoid problematic behavior with horizontal segments.
        self.sweep_line = Segment(Vector(np.array([[xleft], [y]])), Vector(np.array([[xright], [y + self.epsilon]])))

    def update_status_tree(self) -> None:
        """
            And update the nodes positions in the status tree, by the x coordinate of the intersection
            of the segment with the sweepline.
        """

        in_order_tree = self.status_tree.inorder()
        updated_nodes = []

        # update the status tree
        # for each node in the status tree, we update the intersection with the sweepline
        for node in in_order_tree:
            node.value = self.sweep_line.find_intersection(node.extra)[0]
            
            #reset the left and right childs
            node.left = None
            node.right = None
            updated_nodes.append(node)
        
        # rebuild the status tree
        if len(updated_nodes) > 0:
            self.status_tree = Tree(updated_nodes)
            self.sorted_status = self.status_tree.inorder() 


    def sort_and_classify_endpoints(self) -> List[Tuple[Vector, SemiEdge, str]]:

        """
            Sort the endpoints of the segments, and classify them as one of the following:
                - regular vertex
                - start vertex
                - end vertex
                - split vertex
                - merge vertex

            Returns:
            -----------
                A list of tuples, where each tuple contains the endpoint, the semiedge that contains the endpoint as 
                origin, and the type of endpoint.
        """
        endpoints = []

        for i in range(len(self.semiedges)):
            semiedge = self.semiedges[i]
            prev_semiedge = self.semiedges[i - 1]
            origin = semiedge.origin

            # classify the vertex
            type_ = self.classify_vertex(origin.point, semiedge, prev_semiedge)
            endpoints.append((origin.point, semiedge, type_))
            
        # sort by using the vector own comparison methods
        endpoints.sort(key=lambda endpoint_tuple: endpoint_tuple[0])
        return endpoints

    

    def classify_vertex(self, vertex: Vector, semiedge: SemiEdge, prev_semiedge: SemiEdge) -> int:
            
        """
            Classify a vertex as one of the following:
                - regular vertex
                - start vertex
                - end vertex
                - split vertex
                - merge vertex

            Args:
                vertex: vertex to be classified.
                semiedge: semiedge that contains the vertex, as the origin.
                prev_semiedge: previous semiedge in the list of semiedges.
            
            Returns:
                vertex type: int
        """

        # get previous and next points of the vertex
        prev_point = prev_semiedge.origin.point
        next_point = semiedge.next_.point
        turn = Vector.calculate_turn(prev_point, vertex, next_point)

        # the neighbors of the vertex are below the vertex
        if (vertex < prev_point) and (vertex < next_point):

            #if the angle between prev_point, vertex and next_point is less than 180 degrees
            #then the vertex is a start vertex, this is the same as saying that the turn is 1
            #(clockwise turn)
            if turn == 1:
                return START_VERTEX
            else:
                return SPLIT_VERTEX
            
        # the neighbors of the vertex are above the vertex
        elif (vertex > prev_point) and (vertex > next_point):

            #if the angle between prev_point, vertex and next_point is less than 180 degrees
            #then the vertex is a end vertex, this is the same as saying that the turn is 1
            #(clockwise turn)
            if turn == 1:
                return END_VERTEX
            else:
                return MERGE_VERTEX
            
        # the neighbors of the vertex are on the same line as the vertex
        # or one is above and the other is below the vertex
        else:
            return REGULAR_VERTEX



    def add_to_status_tree(self, semiedge: SemiEdge) -> Node1D:

        """
            Add a semiedge to the status tree.
            Wraps a semiedge with a Node1D element and adds it to the tree.
        """
        
        # update the sorted status before adding the semiedge
        if self.status_tree is not None:
            self.sorted_status = self.status_tree.inorder()
        
        #do not add the semiedge if it has already been removed
        if semiedge in self.removed_semiedges:
            return 

        if (self.status_tree is None) or (len(self.sorted_status) == 0):
            # we insert the segment in the status tree, by using the intersection with the sweepline
            # as the value for the node. In this case as there are no other segments in the status 
            # tree we just insert by the xcoordinate of the start point of the segment.
            n = Node1D(semiedge.seg.start[0])
            n.extra = semiedge
            self.status_tree = Tree([n,])
            self.sorted_status = [n,]
        else:
            # if there is an status tree, we need to find the intersection of the segment with the
            # sweepline, and insert the segment in the status tree by the xcoordinate of the
            # intersection.
            intersectx = semiedge.seg.find_intersection(self.sweep_line)[0]
            n = Node1D(intersectx)
            n.extra = semiedge
            self.status_tree.insert(n)
            self.sorted_status = self.status_tree.inorder()

        self.update_status_tree()
        return n


    def remove_from_status_tree(self, semiedge: SemiEdge) -> None:
        
        """
            Remove a node from the status tree. 
            And keep the status tree good structure even if 
            this removed node had childs.
        """
        self.sorted_status = self.status_tree.inorder()

        try:
            idx = [n.extra for n in self.sorted_status].index(semiedge)
        
            #pop the current node (which is and endpoint node) from the status
            self.sorted_status.pop(idx)

            #rebuild the status tree without this endpoint node
            self.status_tree = self.status_tree.build_from_sorted_list(self.sorted_status)

            #add it to the list of removed semiedges
            self.removed_semiedges.append(semiedge)
            self.update_status_tree()

        except ValueError as e:
            if "is not in list" in str(e):
                return 
            else:
                raise e

    def get_left_semiedge_of_vertex(self, vertex: Vector) -> SemiEdge:

        self.sorted_status = self.status_tree.inorder()

        #we want to get the semiedge that is just to the left of the segment, 
        #this is the segment with the smallest magnitude of the horizontal distance and 
        #which has negative horizontal distance
        horizontal_distances = [n.value - vertex[0] for n in self.sorted_status]
        horizontal_distances = [abs(d) if d < 0 else np.inf for d in horizontal_distances]

        if horizontal_distances:
            idx = horizontal_distances.index(min(horizontal_distances))
        else:
            return None

        semiedge_left = self.sorted_status[idx].extra
        return semiedge_left
    
    def get_helper(self, semiedge: SemiEdge) -> Tuple[Vector, int]:
        """
            Gets the helper for a semiedge.
            The helper of 'semiedge' is formally defined as the lowest vertex above the sweepline such that the segment
            from this vertex to the 'semiedge' is interior to the polygon.
            if no such vertex exists, then the helper is the upper vertex of the semiege.
        """

        if semiedge.helper is  None:
            raise ValueError("The helper of the semiedge is None")
        else:
            return semiedge.helper


    def handle_start_vertex(self, vertex: Vector, semiedge: SemiEdge) -> None:

        """
            Handle a start vertex. Add the semiedge to the status tree, and update the helper of the semiedge to 
            the vertex.
        """
        self.add_to_status_tree(semiedge)
        semiedge.helper = (vertex, START_VERTEX)

    def handle_end_vertex(self, vertex: Vector, semiedge: SemiEdge) -> None:

        v, type_ = self.get_helper(semiedge.prev_edge)

        #if the helper of the previous segment is a merge vertex
        #then we new a new diagonal from the vertex to the helper
        if type_ == MERGE_VERTEX:
            self.diagonals.append(SemiEdge(vertex, v, need_cast=True))

        #remove the previous semiedge from the status tree
        self.remove_from_status_tree(semiedge.prev_edge)
    
    def handle_split_vertex(self, vertex: Vector, semiedge: SemiEdge) -> None:
            
        """
            Handle a split vertex. Get the semiedge that is just to the left of the vertex, and add a new diagonal
            from the vertex to the helper of the semiedge that is just to the left of the vertex. Update the helper
            of the semiedge that is just to the left of the vertex to the passed vertex.

            Finally add the segment to the status tree, and update the helper of the semiedge to the vertex.

            Args:
            ------------------
                vertex: vertex to be handled.
                semiedge: semiedge that contains the vertex as origin.
        """

        #gets the segment that is just to the left of the segment
        semiedge_left = self.get_left_semiedge_of_vertex(vertex)

        if semiedge_left is None:
            return

        v2, type_ = self.get_helper(semiedge_left)

        #we add a new diagonal from the vertex to the helper of the semiedge that is just 
        #to the left of the segment
        self.diagonals.append(SemiEdge(vertex, v2, need_cast=True))

        #we update the helper of the segment that is just to the left of the segment
        semiedge_left.set_helper((vertex, SPLIT_VERTEX))

        #we add the semiedge to the status tree
        self.add_to_status_tree(semiedge)
        semiedge.set_helper((vertex, SPLIT_VERTEX))


    def handle_merge_vertex(self, vertex: Vector, semiedge: SemiEdge) -> None:

        """
        """

        #get the helper of the previous segment
        prev_semiedge = semiedge.prev_edge
        v, type_ = self.get_helper(prev_semiedge) 

        #if the helper of the previous segment is a merge vertex
        #then we new a new diagonal from the vertex to the helper
        if type_ == MERGE_VERTEX:
            self.diagonals.append(SemiEdge(vertex, v, need_cast=True))
        
        #remove the previous semiedge from the status tree
        self.remove_from_status_tree(prev_semiedge) 

        #gets the segment that is just to the left of the segment
        semiedge_left = self.get_left_semiedge_of_vertex(vertex)
        
        #if it has no left semiedge then we return
        if semiedge_left is None:
            return 
        
        #otherwise we get the helper of the segment that is just to the left of the segment
        else:
            v2, type_ = self.get_helper(semiedge_left)

            #if the helper of the segment that is just to the left of the segment is a merge vertex
            #then we add a new diagonal from the vertex to the helper
            if type_ == MERGE_VERTEX:
                self.diagonals.append(SemiEdge(vertex, v2, need_cast=True))

        #we update the helper of the segment that is just to the left of the segment
        semiedge_left.set_helper((vertex, MERGE_VERTEX))


    def handle_regular_vertex(self, vertex: Vector, semiedge: SemiEdge) -> None:


        prev = semiedge.prev_edge.origin.point
        origin = semiedge.origin.point
        next_ = semiedge.next_.point
        interior_is_to_the_right = False

        #if i'm going down then the interior of the polygon is to the right of the segment
        #otherwise the interior of the polygon is to the left of the segment,
        #just by thinking of the way the polygon is drawn
        if (prev < origin) and (origin < next_):
            interior_is_to_the_right = True
            print("Interior is to the right")

        #if the interior of the polygon is to the right of the segment (this means we have an anticlockwise 
        #turn) then
        if interior_is_to_the_right:
            v, type_ = self.get_helper(semiedge.prev_edge)

            #if the helper of the previous segment is a merge vertex
            #then we new a new diagonal from the vertex to the helper

            if type_ == MERGE_VERTEX:
                self.diagonals.append(SemiEdge(vertex, v, need_cast=True))

            #delete the previous segment from the status tree
            self.remove_from_status_tree(semiedge.prev_edge)

            #we add the semiedge to the status tree
            semiedge.set_helper((vertex, REGULAR_VERTEX))
            self.add_to_status_tree(semiedge)
            
        #get the segment that is just to the left of the segment
        else:
            semiedge_left = self.get_left_semiedge_of_vertex(vertex)
            
            if semiedge_left is not None:
                v2, type_ = semiedge_left.helper
            else:
                return

            #if the helper of the segment that is just to the left of the segment is a merge vertex
            #then we add a new diagonal from the vertex to the helper
            if type_ == MERGE_VERTEX:
                self.diagonals.append(SemiEdge(vertex, v2, need_cast=True))
            
            #we update the helper of the segment that is just to the left of the segment
            semiedge_left.set_helper((vertex, REGULAR_VERTEX))

    def handle_every_event_point(self, endpoint: Vector, segment: SemiEdge, type_: str) -> None:
        
        if type_ == START_VERTEX:
            print("Processing start vertex")
            self.handle_start_vertex(endpoint, segment)

        elif type_ == END_VERTEX:
            print("Processing end vertex")
            self.handle_end_vertex(endpoint, segment)

        elif type_ == SPLIT_VERTEX:
            print("Processing split vertex")
            self.handle_split_vertex(endpoint, segment)

        elif type_ == MERGE_VERTEX:
            print("Processing merge vertex")
            self.handle_merge_vertex(endpoint, segment)

        elif type_ == REGULAR_VERTEX:
            print("Processing regular vertex")
            self.handle_regular_vertex(endpoint, segment)



    def run(self, plotting: bool = False) -> List[SemiEdge]:

        """
            Run the line sweep algorithm abstraction over the polygon, in 
            order to make it a  y-monotone polygon.

            Returns:
            -----------
                A list of diagonals that turn the polygon into a y-monotone polygon.
        """

        # intersection points list
        self.count = 0
        #self.intersections = []

        # we sort the endpoints
        self.event_points = self.sort_and_classify_endpoints()
        self.event_points_copy = deepcopy(self.event_points)

        # used for delimitation of the sweepline width in the x axis
        self.leftmost_endpoint  = Vector.get_leftmost_point([v for v, s, t in self.event_points])
        self.rightmost_endpoint = Vector.get_rightmost_point([v for v, s, t in self.event_points])

        if plotting:
            self.plot_current_state()

        # we iterate over the endpoints
        while len(self.event_points) > 0:
            print("count: ", self.count)

            endpoint, segment, type_ = self.event_points.pop(0)
            self.update_sweepline(y = endpoint[1], type_= type_)

            # we update the status tree
            if self.status_tree is not None:
                self.update_status_tree()

            # we handle the event point
            self.handle_every_event_point(endpoint, segment, type_)

            print(f"Diagonals: {self.diagonals}")
            print(f"Status tree: {self.sorted_status}")
            print(f"Segments: {[n.extra for n in self.sorted_status]}\n")

            if plotting:
                self.plot_current_state()
            self.count += 1    
        
        return self.diagonals

    def plot_current_state(self):

        """
            Plot the current state of the algorithm.
        """

        PlotMonotonePolygon.plot_polygon(semiedges = self.semiedges,
                                         classifications=self.event_points_copy)
        #dashed sweepline
        if self.sweep_line:
            plt.plot([self.sweep_line.start[0], self.sweep_line.end[0]],
                    [self.sweep_line.start[1], self.sweep_line.end[1]],
                    color='red',
                    linewidth=1.0,
                    linestyle='--',
                    alpha=1.0)

        #dashed black diagonals
        if self.diagonals:
            for diagonal in self.diagonals:
                plt.plot([diagonal.origin[0], diagonal.next_[0]],
                         [diagonal.origin[1], diagonal.next_[1]],
                         color='black',
                         linewidth=1.0,
                         linestyle='--',
                         alpha=1.0)
        
        #text for each vertex
        for n in self.semiedges.list_of_nodes:
            plt.text(n.point[0], n.point[1]+0.10, n.name, fontsize=12)
        
        PlotMonotonePolygon.show()
    
