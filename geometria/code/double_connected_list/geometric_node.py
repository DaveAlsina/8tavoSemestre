import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from copy import deepcopy

from base.vector import Vector
from base.segment import Segment


class GeometricNode():
    """
        This class represents a node in a double connected edge list.
    """

    COLOR1 = 1
    COLOR2 = 2
    COLOR3 = 3

    def __init__(self,
                 point: Vector,
                 name: str = None, 
                 incident_edge: Segment = None,):

        """
            Every node name is a string that represents the name of the node, and
            should have a format like this: 'N1', 'N2', 'N3', etc.
        """
        self.name = name
        self.value = None
        self.point = point
        self.incident_edge = incident_edge
        self.color: int = None

    @property
    def x(self) -> float:
        return float(self.point[0])
    
    @property
    def y(self) -> float:
        return float(self.point[1])

    def set_color(self, color: int) -> None:
        self.color = color

    def __hash__(self) -> int:
        return hash(self.point)

    def __getitem__(self, index: int) -> float:
        return float(self.point[index])
    
    def __repr__(self) -> str:
        return f"{self.name} {self.point}"
    
    def __lt__(self, other_node: 'GeometricNode') -> bool:
        return self.point < other_node.point

    def __le__(self, other_node: 'GeometricNode') -> bool:
        return self.point <= other_node.point
    
    def __gt__(self, other_node: 'GeometricNode') -> bool:
        return self.point > other_node.point

    def __ge__(self, other_node: 'GeometricNode') -> bool:
        return self.point >= other_node.point

    def __eq__(self, other_node: 'GeometricNode') -> bool:
        return self.point == other_node.point
    
    def __ne__(self, other_node: 'GeometricNode') -> bool:
        return self.point != other_node.point