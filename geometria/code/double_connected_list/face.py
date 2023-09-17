import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from copy import deepcopy


class Face():
    def __init__(self, name: str = None):
        self.semi_edges = []
        self._name = name
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_semi_edges(self, semi_edges: List['SemiEdge']) -> None:
        self.semi_edges = semi_edges

    def add_semi_edge(self, semi_edge: 'SemiEdge') -> None:
        self.semi_edges.append(semi_edge)
    
    def __str__(self) -> str:
        return f"{self._name}"
    
    def __repr__(self) -> str:
        return f"{self._name}"