# add path with sys
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# standard imports
import bisect
import numpy as np
from typing import Union, List, Tuple

# custom dependencies
from vector  import  Vector
from segment import  Segment
from binary_tree import Tree, Node1D

class LineSweep:

    def __init__(self, segments: List[Segment]):

        """
            Implement the line sweep algorithm.

            Args:
                segments: list of segments to be processed.
        """

        self.segments = segments
        self.status_tree = None # type: Tree
        self.event_points = None # type: List[Vector]
        self.sorted_status = None # type: List[Node1D]

        self.leftmost_endpoint = None # type: Vector
        self.rightmost_endpoint = None # type: Vector
        self.sweep_line = None # type: Segment

    def update_sweepline(self, y) -> Segment:
        xleft = float(self.leftmost_endpoint[0]) - 1
        xright = float(self.rightmost_endpoint[0]) + 1

        # build the sweepline, from leftmost to rightmost points in the x axis
        # at height y
        self.sweep_line = Segment(Vector(np.array([[xleft], [y]])), Vector(np.array([[xright], [y]])))


    def sort_endpoints(self) -> List[Tuple[Vector, Segment]]:

        """
            Sort the endpoints of the segments.
            Used mainly to build the events list.

            Returns:
                list of tuples (endpoint, segment) sorted by endpoint, which is a vector.
                this sorting is done by using the vector own comparison methods.
        """
        endpoints = []
        for segment in self.segments:
            endpoints.append((segment.start, segment))
            endpoints.append((segment.end, segment))

        # sort by using the vector own comparison methods
        endpoints.sort(key=lambda w: w[0])
        return endpoints
    
    def find_intersections_with_sweepline(self, sweepline: Segment) -> List[Tuple(float, Node1D)]:

        """
            Find the intersections of the segments in the status tree with the sweepline.
        """

        intersections = []
        for node in self.status.inorder():
            intersect_in_x = sweepline.find_intersection(node.extra)[0]
            intersections.append( (intersect_in_x, node) )

        return intersections
    
    def find_intersections_on_left_or_right(self, idx) -> Union[Vector, None]:
        """
            Given a node index, checks its left and right neighborh
            to see if any intersection with one of them.
        """
        segment = self.sorted_status[idx]
        left = idx-1
        right = idx+1

        # if a left segment exists
        if left >= 0:
            left_segment = self.sorted_status[left].extra

            #if any intersection go and search for it 
            if left_segment.segments_intersect(segment):
                return left_segment.get_intersection_of_segments_general(segment)

        #if a right segment exists
        if right < len(self.sorted_status):
            right_segment = self.sorted_status[right].extra

            #if any intersection go and search for it 
            if right_segment.segments_intersect(segment):
                return right_segment.get_intersection_of_segments_general(segment)
    
    def add_to_status_tree(self, segment: Segment) -> Node1D:

        """
            Add a segment to the status tree.
            Wraps a segment with a Node1D element and adds it to the tree.
        """
        if self.status_tree is None:
            # we insert the segment in the status tree, by using the intersection with the sweepline
            # as the value for the node. In this case as there are no other segments in the status 
            # tree we just insert by the xcoordinate of the start point of the segment.
            n = Node1D(float(segment.start[0]))
            n.extra = segment
            self.status = Tree([n,])
        else:
            # if there is an status tree, we need to find the intersection of the segment with the
            # sweepline, and insert the segment in the status tree by the xcoordinate of the
            # intersection.
            intersectx = segment.find_intersection(self.sweep_line)[0]
            n = Node1D(intersectx)
            n.extra = segment
            self.status.insert(n)
        return n

    
    def remove_from_status_tree(self, node: Node1D) -> None:
        
        """
            Remove a node from the status tree. 
            And keep the status tree good structure even if 
            this removed node had childs.
        """
        
        #reorder the status 
        self.sorted_status = self.status.inorder()
        
        #find any intersection on the neighborhs of the current node
        idx = self.sorted_status.index(node)

        #pop the current node (which is and endpoint node) from the status
        self.sorted_status.pop(idx)

        #rebuild the status tree without this endpoint node
        self.status = Tree.build_from_sorted_list(self.sorted_status)

        

    def handle_start_endpoint(self, segment: Segment) -> Vector:

        """
            Handle the start endpoint of a segment.
            when we encounter a start endpoint, we insert the segment into the status.

            Args:
                segment: segment whose start endpoint is being handled.
        """

        #adds a segment to the tree, and get's the node associated to it 
        current_node = self.add_to_status_tree(segment)
        
        #gets the status in order by the intersect with the sweepline
        self.sorted_status = self.status.inorder()

        #gets the index of the current node
        idx = self.sorted_status.index(current_node)

        #with the current node go and check for intersections with 
        #it's neiborhs
        return self.find_intersections_on_left_or_right(idx)
        

    def handle_end_endpoint(self, segment: Segment) -> bool:

        """
            Handle the end endpoint of a segment.
            when we encounter an end endpoint, we remove the segment from status, after a last check.

            Args:
                segment: segment whose end endpoint is being handled.
        """

        # gets the index node associated to the segment we need remove   

        # checks if the node has left or right neiborhs and if any intersection 
        # with them 


        # finally we remove the segment from the status
        self.remove_from_status_tree()


    def process(self) -> List[Vector]:

        """
            Process the segments.

            Returns:
                All the intersection points.
        """

        # intersection points list
        intersections = []

        # we sort the endpoints
        self.events = self.sort_endpoints()

        # we iterate over the endpoints
        while len(self.events) > 0:
            endpoint, segment = self.events.pop(0)

            # if the endpoint is the start of a segment, we handle it
            if endpoint == segment.start:
                intersect = self.handle_start_endpoint(segment)

            # if the endpoint is the end of a segment, we handle it
            else:
                intersect = self.handle_end_endpoint(segment)

            if intersect is not None:
                # we insert the intersection point in the events list, 
                # which is already sorted by our lexigraphic vector ordering
                bisect.insort(self.events, (intersect, segment), key=lambda w: w[0])
                intersections.append(intersect)
                
            

        # if we reach this point, there are no intersections
        return False
    

    #=============================================================
    #                      HELPER METHODS
    #=============================================================

    def get_extremes_in_xaxis(self) -> None:
        """
        """
        self.leftmost_endpoint  = Vector.get_leftmost_point(self.event_points)
        self.rightmost_endpoint = Vector.get_rightmost_point(self.event_points)