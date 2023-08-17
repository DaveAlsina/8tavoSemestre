import os, sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Union, List, Tuple

from base import Vector, Segment
from binary_tree import Tree, Node1D

class LineSweep:

    def __init__(self, segments: List[Segment]):

        """
            Implement the line sweep algorithm.

            Args:
                segments: list of segments to be processed.
        """

        self.segments = segments
        self.status = None # type: Tree
        self.events = None # type: List[Vector]


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
    
    def find_intersections_with_sweepline(self, sweepline_position: float) -> List[Segment]:

        sweepline_start = Vector(np.array([[-np.inf], [sweepline_position]]))
        sweepline_end   = Vector(np.array([[np.inf], [sweepline_position]]))
        sweepline = Segment(sweepline_start, sweepline_end)

        intersections = []
        for segment in self.status.inorder():

            interect = sweepline.find_intersection(segment)
            intersections.append( (interect[0], segment) )
    
    def add_to_status_tree(self, segment: Segment) -> None:

        """
            Add a segment to the status tree.
        """

        if self.status is not None:
            self.status.insert(Node1D(segment))
        else:
            self.status = Tree(Node1D(segment))
        return 
    
    def remove_from_status_tree(self, segment: Segment) -> None:
        return 

    def order_by_intersect_with_sweep_line(self, sweepline_position: float) -> List[Segment]:
        return 


    def handle_start_endpoint(self, segment: Segment) -> bool:

        """
            Handle the start endpoint of a segment.
            when we encounter a start endpoint, we insert the segment into the status.

            Args:
                segment: segment whose start endpoint is being handled.
        """

        self.add_to_status_tree(segment)
        
        # check for intersections, for this we need to check to the left and right of the segment
        # in the status

        #if there is a segment to the left of the current segment, and they intersect we return True

        #if there is a segment to the right of the current segment, and they intersect we return True
        

    def handle_end_endpoint(self, segment: Segment) -> bool:

        """
            Handle the end endpoint of a segment.
            when we encounter an end endpoint, we remove the segment from status, after a last check.

            Args:
                segment: segment whose end endpoint is being handled.
        """

        # if both the segment to the left and to the right exist, and they intersect, we return True

        # finally we remove the segment from the status
        self.status.remove(segment)


    def process(self) -> bool:

        """
            Process the segments.

            Returns:
                True if there is an intersection, False otherwise.
        """

        # we sort the endpoints
        self.events = self.sort_endpoints()

        # we iterate over the endpoints
        for endpoint, segment in self.events:

            # if the endpoint is the start of a segment, we handle it
            if endpoint == segment.start:
                self.handle_start_endpoint(segment)

            # if the endpoint is the end of a segment, we handle it
            else:
                self.handle_end_endpoint(segment)

        # if we reach this point, there are no intersections
        return False