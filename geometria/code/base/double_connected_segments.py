from typing import List
from copy import deepcopy

#
from vector import Vector
from segment import Segment


class GeometricNode():
    """
        This class represents a node in a double connected edge list.
    """

    def __init__(self,
                 point: Vector,
                 name: str, 
                 incident_edge: str = None, 
                 twin: str = None):

        """
            Every node name is a string that represents the name of the node, and
            should have a format like this: 'N1', 'N2', 'N3', etc.

            The incident edge is generated automatically if not provided,
            and has the format: 'N11', 'N21', 'N31' by default.

            The twin is generated automatically if not provided,
            and has the format: 'N12', as twin for 'N11', 'N22' as twin for 'N21', etc.
        """

        self.point = point
        self.name = name
        self.incident_edge = None
        self.twin = None 

    @staticmethod
    def build_twin(semiedge: 'SemiEdge') -> 'SemiEdge':
        """
            This method builds the twin of a given semi-edge.
        """
        twin = deepcopy(semiedge)
        twin.origin = semiedge.origin
        twin.next = semiedge.prev
        twin.prev = semiedge.next
        return twin

    def __repr__(self) -> str:
        return f"GeometryNode({self.point}) <- {self.incident_edge}"

    def __getitem__(self, index: int) -> float:
        return self.point[index]


class SemiEdge():

    def __init__ (self, 
                  origin: GeometricNode,
                  next: GeometricNode,
                  prev: GeometricNode,
                  incident_face: 'Face' = None):

        self.origin = origin

        self.twin = self.origin.twin
        self.next = next.incident_edge
        self.prev = prev.incident_edge
        self.face = incident_face
    
    def __repr__(self) -> str:
        return f"SemiEdge({self.origin} >> {self.next})"
    
    def __eq__(self, semiedge: 'SemiEdge') -> bool:
        return (self.origin == semiedge.origin) and (self.next == semiedge.next) and (self.prev == semiedge.prev)
        
    def __ne__(self, semiedge: 'SemiEdge') -> bool:
        return not self.__eq__(semiedge)



class SemiEdgeList():

    def __init__(self, list_of_nodes: list[GeometricNode]):
        
        self.list_of_nodes = list_of_nodes
        self.semi_edges = []

        self.build_semi_edges()
        self.add_incident_edge()
        self.add_twin()
        self.build_semi_edges()

    def build_semi_edges(self) -> List[SemiEdge]:
        """
            This method builds the semi-edges of a given list of nodes.
        """
        self.semi_edges = []
        
        for i in range(len(self.list_of_nodes)):
            semi_edge = SemiEdge(origin = self.list_of_nodes[i], 
                                 next = self.list_of_nodes[(i+1)%len(self.list_of_nodes)], 
                                 prev = self.list_of_nodes[i-1])
            self.semi_edges.append(semi_edge)

        return self.semi_edges
    
    def add_incident_edge(self) -> None:
        """
            This method adds the incident edge to each node in the list of nodes.
            The incident edge is the semi-edge that has the node as origin.
        """
        for i in range(len(self.list_of_nodes)):
            self.list_of_nodes[i].incident_edge = self.semi_edges[i]

    def add_twin(self) -> None:
        """
            This method adds the twin to each node in the list of nodes.
            The twin is the semi-edge that has the node as origin, but in the opposite direction.
        """
        for i in range(len(self.list_of_nodes)):
            self.list_of_nodes[i].twin = GeometricNode.build_twin(self.semi_edges[i])




class Face():
    def __init__(self, name: str,
                       incident_edge: str):
        self.name = name
        self.incident_edge = incident_edge