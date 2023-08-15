import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Union, List
from pyparsing import abstractmethod
from abc import ABC

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

        self.sorted_endpoints = self.sort_endpoints()

    def sort_endpoints(self):

        """
            Sort the endpoints of the segments.

            Returns:
                list of endpoints sorted by x coordinate.
        """

        endpoints = []
        for segment in self.segments:
            endpoints.append(Node1D(segment.v0))
            endpoints.append(Node1D(segment.v1))

        tree = Tree(endpoints)
        ordered_segments = tree.inorder()

        return ordered_segments
    
    def process(self) -> bool:

        """
            Process the segments. And tell if there is an intersection.

            Returns:
                True if there is an intersection, False otherwise.
        """

        

