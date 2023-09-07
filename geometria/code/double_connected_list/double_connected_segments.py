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

    def __init__(self,
                 point: Vector,
                 name: str, 
                 incident_edge: Segment = None,):

        """
            Every node name is a string that represents the name of the node, and
            should have a format like this: 'N1', 'N2', 'N3', etc.
        """
        self.point = point
        self.name = name
        self.incident_edge = incident_edge


#------------------------------------------------------------------------------#

class SemiEdge():

    def __init__ (self, 
                  origin: GeometricNode,
                  next_: GeometricNode,
                  incident_face: 'Face' = None):

        self.origin = origin
        self.seg = Segment(origin.point, next_.point)
        self.twin = Segment(next_.point, origin.point)
        self.incident_face = incident_face

        self.next_edge = None
        self.prev_edge = None

    def set_next_edge(self, next_edge: 'SemiEdge') -> None:
        self.next_edge = next_edge
    
    def set_prev_edge(self, prev_edge: 'SemiEdge') -> None:
        self.prev_edge = prev_edge

    def __repr__(self) -> str:
        return f"{self.seg} {self.incident_face}"
    
    def __str__(self) -> str:
        return f"{self.seg} {self.incident_face}"
    
    def __eq__(self, semiedge: 'SemiEdge') -> bool:
        return self.seg == semiedge.seg 
        
    def __ne__(self, semiedge: 'SemiEdge') -> bool:
        return self.seg != semiedge.seg

#------------------------------------------------------------------------------#

class SemiEdgeList():

    def __init__(self, list_of_points: List[Vector], name: str = None):
        
        self.list_of_nodes : List[GeometricNode] = []
        self.semi_edges : List[SemiEdge] = []
        self.faces : List[Face] = []
        self.name = name
        
        self._build_nodes(list_of_points)
        self._build_semi_edges()

    def add_semi_edges(self, semi_edges: List[SemiEdge]) -> None:
        """
            This function adds semi-edges to the list of semi-edges.

            This is a delicate process, because with each semi-edge we add 
            it's necessary to add the next and prev edges of each semi-edge.
            And if this semiedge intersects with another semi-edge, we have to
            add the intersection point to the list of nodes, and add the new
            semi-edges that are created by the intersection.
        """
        pass


    def _build_nodes(self, list_of_points: List[Vector]) -> None:
        """
            This function builds the nodes from a list of points.
            The name of each node is the index of the point in the list of points.
        """
        self.list_of_nodes = []
        for i in range(len(list_of_points)):
            node = GeometricNode(point = list_of_points[i], name = f"N{i}")
            self.list_of_nodes.append(node)

    def _build_semi_edges(self) -> List[SemiEdge]:
        """
            This function builds the semi-edges from the list of nodes.
            This assumes that the list of nodes is ordered in a way that
            the next node is the next node in the polygon (this is true just 
            at first build time).

            The function builds the semi-edges, the next and prev edges of each
            semi-edge, and the faces of each semi-edge.
        """
        self.semi_edges = []
        
        # Create the semi-edges from the list of nodes
        for i in range(len(self.list_of_nodes)):
            semi_edge = SemiEdge(origin = self.list_of_nodes[i], 
                                 next_ = self.list_of_nodes[(i+1)%len(self.list_of_nodes)])
            self.semi_edges.append(semi_edge)

        # Set the next and prev edges of each semi-edge
        for i in range(len(self.semi_edges)):
            self.semi_edges[i].set_next_edge(self.semi_edges[(i+1)%len(self.semi_edges)])
            self.semi_edges[i].set_prev_edge(self.semi_edges[(i-1)%len(self.semi_edges)])
        
        # add faces to the semi-edges
        self._set_faces()

        return self.semi_edges

    def _set_faces(self) -> None:
        """
            This function adds the faces to the semi-edges.

            The idea is to take a semi-edge, and iter to the next semi-edge until
            we reach the initial semi-edge. All the semi-edges that we visited until 
            reaching the initial semi-edge form a face.
        """

        faces_count = 0

        # We iterate over the semi-edges
        for semi_edge in self.semi_edges:

            #print(f"iterating over semi-edge {semi_edge}, face: {semi_edge.incident_face}, face_count: {faces_count}")
            # If the semi-edge doesn't have a face, then we add a face
            if semi_edge.incident_face == None:
                # We create a new face
                face = Face(name = f"{self.name}:F{faces_count}")

                # We add the semi-edge to the face
                face.add_semi_edge(semi_edge)
                # We iterate over the next semi-edge
                next_semi_edge = semi_edge.next_edge
                # We add the face to the semi-edge
                semi_edge.incident_face = face
                next_semi_edge.incident_face = face

                # While the next semi-edge is not the initial semi-edge
                while next_semi_edge != semi_edge:
                    #print(f"\t next_semi_edge: {next_semi_edge}, semi_edge: {semi_edge}, face: {face}, face_count: {faces_count}")

                    # We iterate over the next semi-edge
                    next_semi_edge = next_semi_edge.next_edge

                    # We add the face to the semi-edge
                    next_semi_edge.incident_face = face

                self.faces.append(face)
                faces_count += 1


    def __str__(self) -> str:
        return f"{self.semi_edges}"
    
    def __repr__(self) -> str:
        return f"{self.semi_edges}"


#------------------------------------------------------------------------------#

class Face():
    def __init__(self, name: str = None):
        self.semi_edges = []
        self._name = name
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_semi_edges(self, semi_edges: List[SemiEdge]) -> None:
        self.semi_edges = semi_edges

    def add_semi_edge(self, semi_edge: SemiEdge) -> None:
        self.semi_edges.append(semi_edge)
    
    def __str__(self) -> str:
        return f"{self._name}"
    
    def __repr__(self) -> str:
        return f"{self._name}"