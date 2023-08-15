#standard imports
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Union, List
from pyparsing import abstractmethod
from abc import ABC

#custom imports
from base import Vector, Segment

class Node(ABC):

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"

    #classes inheriting from this class must implement these methods
    @abstractmethod
    def __gt__(self, other):
        raise NotImplementedError
    
    @abstractmethod
    def __lt__(self, other):
        raise NotImplementedError
    
    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError
    
    @abstractmethod
    def __ge__(self, other):
        raise NotImplementedError
    
    @abstractmethod
    def __le__(self, other):
        raise NotImplementedError
    
    @staticmethod
    def cast_to_nodes(values: List) -> List['Node']:
        raise NotImplementedError


class Node1D(Node):

    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None

    #=====================================
    #       order comparison methods
    #=====================================
    def __gt__(self, other: 'Node1D'):
        return self.value > other.value

    def __lt__(self, other: 'Node1D'):
        return self.value < other.value

    def __eq__(self, other: 'Node1D'):
        return self.value == other.value

    def __ge__(self, other: 'Node1D'):
        return self.value >= other.value
    
    def __le__(self, other: 'Node1D'):
        return self.value <= other.value

    @staticmethod
    def cast_to_nodes(values: List[float]) -> List['Node1D']:
        return [Node1D(v) for v in values]


class Node2D(Node):
    
        def __init__(self, value: tuple):
            """
                Creates a node with a value of 2 elements.

                value: tuple of 2 elements, where the first element is the x coordinate 
                and the second element is the y coordinate.
            """

            self.value = value
            self.left = None
            self.right = None
    
        #=====================================
        #       order comparison methods
        #=====================================
        def __gt__(self, other: 'Node2D'):
            if self.value[1] > other.value[1]:
                return True
            elif self.value[1] == other.value[1]:
                return self.value[0] < other.value[0]
    
        def __lt__(self, other: 'Node2D'):
            
            if self.value[1] > other.value[1]:
                return True
            elif self.value[1] == other.value[1]:
                return self.value[0] > other.value[0]
    
        def __eq__(self, other: 'Node2D'):
            return self.value == other.value
    
        def __ge__(self, other: 'Node2D'):
            return (self > other) or (self == other)
        
        def __le__(self, other: 'Node2D'):
            return (self < other) or (self == other)
    
        @staticmethod
        def cast_to_nodes(values: List[float]) -> List['Node2D']:
            return [Node2D(v) for v in values]

