# add path with sys
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# standard imports
import bisect
import numpy as np
from matplotlib import pyplot as plt
from typing import Union, List, Tuple

# custom dependencies
from vector  import  Vector
from segment import  Segment
from plotter import  VectorPlotter, SegmentPlotter
from binary_tree import Tree, Node1D

class SweepLine:

    def __init__(self, segments: List[Segment]):

        """
            Implement the line sweep algorithm.

            Args:
                segments: list of segments to be processed.
        """

        self.segments = segments
        self.status_tree = None # type: Tree[Node1D]
        self.event_points = None # type: List[Vector]
        self.sorted_status = None # type: List[Node1D]
        self.intersections = None # type: List[Vector]

        self.leftmost_endpoint = None # type: Vector
        self.rightmost_endpoint = None # type: Vector
        self.sweep_line = None # type: Segment

    def update_sweepline(self, y) -> Segment:

        """
            Update the sweepline to the height y.
        """
        xleft = self.leftmost_endpoint[0] - 1
        xright = self.rightmost_endpoint[0] + 1

        # build the sweepline, from leftmost to rightmost points in the x axis
        # at height y
        self.sweep_line = Segment(Vector(np.array([[xleft], [y]])), Vector(np.array([[xright], [y]])))

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
        
        print("\tupdated nodes: ", updated_nodes)
        
        # rebuild the status tree
        self.status_tree = Tree(updated_nodes)
        self.sorted_status = self.status_tree.inorder() 


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

    def find_intersections_with_sweepline(self, sweepline: Segment) -> List[Tuple[float, Node1D]]:

        """
            Find the intersections of the segments in the status tree with the sweepline.
        """

        intersections = []
        for node in self.status_tree.inorder():
            intersect_in_x = sweepline.find_intersection(node.extra)[0]
            intersections.append( (intersect_in_x, node) )

        return intersections

    def find_intersections_on_left_or_right(self, idx) -> Union[Tuple[Vector, Segment], None]:
        """
            Given a node index, checks its left and right neighborh
            to see if any intersection with one of them.

            Args:
            -----------
                idx: index of the node in the sorted status list.
            
            Returns:
            -----------
                The intersection point of the segment with its neiborhs and the other
                segment it intersects.
        """
        segment = self.sorted_status[idx].extra
        left = idx-1
        right = idx+1

        # if a left segment exists
        if left >= 0:
            left_segment = self.sorted_status[left].extra
            print("\t\thas left")

            #if any intersection go and search for it 
            if left_segment.segments_intersect(segment):
                i = left_segment.get_intersection_of_segments_general(segment)
                print("\t\thas intersection ", i)
                return i, left_segment

        #if a right segment exists
        if right < len(self.sorted_status):
            right_segment = self.sorted_status[right].extra
            print("\t\thas right")

            #if any intersection go and search for it 
            if right_segment.segments_intersect(segment):
                i = right_segment.get_intersection_of_segments_general(segment)
                print("\t\thas intersection ", i)
                return i, right_segment

    def add_to_status_tree(self, segment: Segment) -> Node1D:

        """
            Add a segment to the status tree.
            Wraps a segment with a Node1D element and adds it to the tree.
        """
        if self.status_tree is None:
            # we insert the segment in the status tree, by using the intersection with the sweepline
            # as the value for the node. In this case as there are no other segments in the status 
            # tree we just insert by the xcoordinate of the start point of the segment.
            n = Node1D(segment.start[0])
            n.extra = segment
            self.status_tree = Tree([n,])
            self.sorted_status = [n,]
        else:
            # if there is an status tree, we need to find the intersection of the segment with the
            # sweepline, and insert the segment in the status tree by the xcoordinate of the
            # intersection.
            intersectx = segment.find_intersection(self.sweep_line)[0]
            n = Node1D(intersectx)
            n.extra = segment
            self.status_tree.insert(n)
            self.sorted_status = self.status_tree.inorder()
        return n


    def remove_from_status_tree(self, idx: int) -> None:
        
        """
            Remove a node from the status tree. 
            And keep the status tree good structure even if 
            this removed node had childs.
        """
        
        #pop the current node (which is and endpoint node) from the status
        self.sorted_status.pop(idx)

        #rebuild the status tree without this endpoint node
        self.status_tree = self.status_tree.build_from_sorted_list(self.sorted_status)

        

    def handle_start_endpoint(self, segment: Segment) -> Union[Tuple[Vector, Segment], None]:

        """
            Handle the start endpoint of a segment.
            when we encounter a start endpoint, we insert the segment into the status.

            Args:
            -----------
                segment: segment whose start endpoint is being handled.
            
            Returns:
            -----------
                The intersection point of the segment with its neiborhs.
        """

        #adds a segment to the tree, and get's the node associated to it 
        current_node = self.add_to_status_tree(segment)
        print("\tcurrent node: ", current_node)
        
        #gets the status in order by the intersect with the sweepline
        print("\tsorted status: ", self.sorted_status)

        #gets the index of the current node
        idx = self.sorted_status.index(current_node)

        #with the current node go and check for intersections with 
        #it's neiborhs
        return self.find_intersections_on_left_or_right(idx)
        

    def handle_end_endpoint(self, segment: Segment) -> Union[Tuple[Vector, Segment], None]:

        """
            Handle the end endpoint of a segment.
            when we encounter an end endpoint, we remove the segment from status, after a last check.

            Args:
            -----------
                segment: segment whose end endpoint is being handled.
        """

        #updates the sorted status
        self.sorted_status = self.status_tree.inorder()

        # gets the index node associated to the segment we need remove   
        idx = [n.extra for n in self.sorted_status].index(segment)
        print("\tcurrent node: ", self.sorted_status[idx])
        print("\tsorted status: ", self.sorted_status)

        # checks if the node has left or right neiborhs and if any intersection 
        # with them 
        intersect_tuple = self.find_intersections_on_left_or_right(idx)

        # finally we remove the segment from the status
        self.remove_from_status_tree(idx)

        if intersect_tuple is not None:
            return intersect_tuple[0], intersect_tuple[1]
        else:
            return None

        

    def run(self,
            plotting: bool = False,
            verbose: bool = False) -> List[Vector]:

        """
            Process the segments.

            Returns:
            -----------
                All the intersection points.
        """

        count = 0
        # intersection points list
        self.intersections = []

        # we sort the endpoints
        self.event_points = self.sort_endpoints()
        
        # used for delimitation of the sweepline width in the x axis
        self.leftmost_endpoint  = Vector.get_leftmost_point([v for v, s in self.event_points])
        self.rightmost_endpoint = Vector.get_rightmost_point([v for v, s in self.event_points])

        # we iterate over the endpoints
        while len(self.event_points) > 0:
            print("count: ", count)
            endpoint, segment = self.event_points.pop(0)

            # we update the sweepline y = endpoint[1]
            self.update_sweepline(endpoint[1])

            # we update the status tree
            if self.status_tree is not None:
                self.update_status_tree()

            # if the endpoint is the start of a segment, we handle it
            if endpoint == segment.start:
                print("START ENDPOINT")
                intersect = self.handle_start_endpoint(segment)

            # if the endpoint is the end of a segment, we handle it
            elif endpoint == segment.end:
                print("END ENDPOINT")
                intersect = self.handle_end_endpoint(segment)

            if intersect is not None:
                
                #checks if the intersection is already in the list
                if intersect[0] not in self.intersections:

                    #we choose as segment for the intersection the one with the biggest 
                    #endpoint using the vector own comparison methods, this is because
                    #we want to avoid that the segment associated to the intersection
                    #is deleted from the status tree, and later on the intersection
                    #is left alone
                    intersect_segment = max((segment, intersect[1]), key=lambda w: w.end)

                    # we insert the intersection point in the events list, 
                    # which is already sorted by our lexigraphic vector ordering
                    bisect.insort(self.event_points, (intersect[0], intersect_segment), key=lambda w: w[0])
                    self.intersections.append(intersect[0])
            

            if plotting:
                self.plot_current_state()
            count += 1    

    def plot_current_state(self):

        """
            Plot the current state of the algorithm.
        """

        SegmentPlotter.plot_many_with_intersections(self.segments,
                                                    self.intersections)
        plt.plot([self.sweep_line.start[0], self.sweep_line.end[0]],
                 [self.sweep_line.start[1], self.sweep_line.end[1]],
                 color='r', linestyle='--')
        plt.show()