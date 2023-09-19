import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import Vector

from typing import List
from copy import deepcopy


class Face():
    
    INTERIOR_FACE = 1
    EXTERIOR_FACE = 2 

    def __init__(self, name: str = None):

        self.semi_edges: List['SemiEdge'] = []
        self._name: str = name
        self.face_type: int = -1
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_semi_edges(self, semi_edges: List['SemiEdge']) -> None:
        self.semi_edges = semi_edges
        self.set_face_type()

    def add_semi_edge(self, semi_edge: 'SemiEdge') -> None:
        self.semi_edges.append(semi_edge)
    
    def set_face_type(self):
        
        #get the leftmost point among the set of points in the polygon
        points = [semiedge.origin.point for semiedge in self.semi_edges]
        left_most_point = Vector.get_leftmost_point(points)
        
        #get the index corresponding to the segment that has that point as 
        #orgin
        idx = points.index(left_most_point)
        left_most_semiedge = self.semi_edges[idx]

        #get the origin point, the previous and the next of these
        origin = left_most_semiedge.start
        prev = left_most_semiedge.prev_edge.start
        next_ = left_most_semiedge.end

        #get the way the face is turning 
        turn = Vector.calculate_turn(prev, origin, next_)

        if turn == 1:
            self.face_type = Face.EXTERIOR_FACE
        elif turn == -1:
            self.face_type = Face.INTERIOR_FACE

    def __str__(self) -> str:
        return f"{self._name}"
    
    def __repr__(self) -> str:
        return f"{self._name}"