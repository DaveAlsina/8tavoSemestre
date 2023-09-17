# add path with sys
import os, sys
from copy import deepcopy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import Vector, Segment
from sweep_line import SweepLine
from double_connected_segments import GeometricNode, SemiEdge, SemiEdgeList


#Things we need for passing to this class:
# 1. the list of semiedges that form the subdivision, should have it's faces 
#    already set and properly labeled.
# 2. with this list of subdivisions we gotta copy the internal information 
#    of them into a new list of semiedges that will be the overlay.
# 3. with this information we now have to convert the overlay into a valid one
#    for this we first need to: 
#   3.1. get the intersection points of the semiedges of the overlay.
#   3.2. get the new semiedges that are created by the intersection points.

class OverlayOfSubdivisions():

    def __init__(self, 
                 subdivisions: list[SemiEdgeList],
                 name: str):

        self.name = name
        self.subdivisions: list[SemiEdgeList] = deepcopy(subdivisions)
        self.overlay : SemiEdgeList = None

        self.list_of_segments: list[Segment] = None
        self.overlay_intersections: list[Vector] = None

        self.merge_semi_edge_lists()
        self.build_list_of_segments_from_semiedge_list()

    def merge_semi_edge_lists(self) -> None:
        """
            This method merges the semi edge lists in the list of subdivisions
            into a single semi edge list.
        """
        self.overlay = SemiEdgeList(list_of_points=[])

        for subdivision in self.subdivisions:
            self.overlay.faces.extend(subdivision.faces)
            self.overlay.semi_edges.extend(subdivision.semi_edges)
            self.overlay.list_of_nodes.extend(subdivision.list_of_nodes)
    
    def build_list_of_segments_from_semiedge_list(self) -> None:
        """
            This method builds the list of segments from the semi edge list.
        """

        # This is a list of segments that will be used by the sweep line algorithm
        # it's important to sort the ends of the segments, following the lexicographic
        # ordering we've built in the Segment class.
        self.list_of_segments = [Segment(semiedge.seg.start, semiedge.seg.end, sort_ends=True) for semiedge in self.overlay.semi_edges]
    
    def find_subdivisions_intersections(self, plotting: bool = False) -> None:
        """
            This method finds the intersections between the segments of the 
            subdivisions.
        """
        self.overlay_intersections = SweepLine(self.list_of_segments).run(plotting=plotting)

        #notice that every endpoint of subdivision is also an intersection point
        self.overlay_intersections.extend([n.point for n in self.overlay.list_of_nodes])

        #now we need to keep only the unique intersection points
        self.overlay_intersections = list(set(self.overlay_intersections))