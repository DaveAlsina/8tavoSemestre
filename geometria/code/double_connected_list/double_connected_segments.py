import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from typing import List, Tuple, Literal, Union
from copy import deepcopy

from base.vector import Vector
from base.segment import Segment
from geometric_node import GeometricNode
from face import Face


#------------------------------------------------------------------------------#
class SemiEdge():

    def __init__ (self, 
                  origin: Union[GeometricNode, Vector],
                  next_: Union[GeometricNode, Vector],
                  incident_face: Face = None, 
                  need_cast: bool = False):


        if need_cast:
            self.origin: GeometricNode = GeometricNode(origin)
            self.next_: GeometricNode = GeometricNode(next_)

        else:
            self.origin: GeometricNode = origin
            self.next_: GeometricNode = next_

        self.seg: Segment = Segment(self.origin.point, self.next_.point)
        self.incident_face: Face = incident_face

        #completely twisted version of self
        self.next_edge: SemiEdge = None
        self.prev_edge: SemiEdge = None
        self.twin: SemiEdge = None
        
        #name of the semiedge
        self.name: str = None
        
        # This is used for the triangulation, the literal part is a constant 
        # that indicates the helper vector type, this could be START_VERTEX,
        # END_VERTEX, SPLIT_VERTEX, MERGE_VERTEX, REGULAR_VERTEX
        self.helper: Tuple[Vector, Literal]= None
    
    @property
    def start(self) -> Vector:
        return self.seg.start
    
    @property
    def end(self) -> Vector:
        return self.seg.end

    def set_next_edge(self, next_edge: 'SemiEdge') -> None:
        self.next_edge = next_edge
    
    def set_prev_edge(self, prev_edge: 'SemiEdge') -> None:
        self.prev_edge = prev_edge
    
    def set_helper(self, helper: Tuple[Vector, int]) -> None:
        self.helper = helper

    def set_twin(self, twin: 'SemiEdge') -> None:
        self.twin = twin
    
    def set_name(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        if self.name != None:
            return f"{self.name}"
        else: 
            return f"SE({self.origin}, {self.next_})"
    
    def __str__(self) -> str:
        if self.name != None:
            return f"{self.name}"
        else: 
            return f"SE({self.origin}, {self.next_})"
    
    def __eq__(self, semiedge: 'SemiEdge') -> bool:
        return self.seg == semiedge.seg 
        
    def __ne__(self, semiedge: 'SemiEdge') -> bool:
        return self.seg != semiedge.seg

    def __hash__(self) -> int:
        return hash(self.seg)

#------------------------------------------------------------------------------#
class SemiEdgeList():

    def __init__(self, list_of_points: List[Vector], name: str):
        
        self.list_of_nodes : List[GeometricNode] = []
        self.semi_edges : List[SemiEdge] = []
        self.faces : List[Face] = []
        self.name = name
        
        self._build_nodes(list_of_points)
        self._build_semi_edges()
    
    def show_data_structure(self) -> pd.DataFrame:
        df = pd.DataFrame(columns = ["name", "origin", "next", "prev_edge", "next_edge", "twin", "prev_edge_twin", "next_edge_twin", "incident_face"])

        for semiedge in self.semi_edges:
            line = pd.DataFrame([{"name": semiedge.name,
                                  "origin": semiedge.origin.name, 
                                  "next": semiedge.next_.name, 
                                  "prev_edge": semiedge.prev_edge, 
                                  "next_edge": semiedge.next_edge,
                                  "twin": semiedge.twin, 
                                  "prev_edge_twin": semiedge.twin.prev_edge,
                                  "next_edge_twin": semiedge.twin.next_edge,
                                  "incident_face": semiedge.incident_face.name},])
            df = pd.concat([df, line])

        df = df.reset_index(drop=True)

        return df

    def add_new_semi_edges(self, semi_edges: List[SemiEdge]) -> None:
        """
            This function adds semi-edges to the list of semi-edges.

            This is a delicate process, because with each semi-edge we add 
            it's necessary to add the next and prev edges of each semi-edge.
            And if this semiedge intersects with another semi-edge, we have to
            add the intersection point to the list of nodes, and add the new
            semi-edges that are created by the intersection.
        """
        
        for semiedge in semi_edges:
            self.add_new_edge(semiedge)

    def _build_nodes(self, list_of_points: List[Vector]) -> None:
        """
            This function builds the nodes from a list of points.
            The name of each node is the index of the point in the list of points.
        """
        self.list_of_nodes = []
        for i in range(len(list_of_points)):
            node = GeometricNode(point = list_of_points[i], name = f"{self.name}N{i}")
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
            twin = SemiEdge(origin = semi_edge.next_, 
                            next_ = semi_edge.origin)

            #handle twins mutually
            semi_edge.set_twin(twin)
            twin.set_twin(semi_edge)

            #add to the list of semi-edges, and set the name
            semi_edge.set_name(f"SE{len(self.semi_edges)}")
            twin.set_name(f"SE{len(self.semi_edges)}''")
            self.semi_edges.append(semi_edge)

        # Set the next and prev edges of each semi-edge
        for i in range(len(self.semi_edges)):
            self.semi_edges[i].set_next_edge(self.semi_edges[(i+1)%len(self.semi_edges)])
            self.semi_edges[i].set_prev_edge(self.semi_edges[(i-1)%len(self.semi_edges)])

            twin_next = SemiEdge(origin = self.semi_edges[i].prev_edge.next_,
                                 next_ = self.semi_edges[i].prev_edge.origin)
            twin_prev = SemiEdge(origin = self.semi_edges[i].next_edge.next_,
                                 next_ = self.semi_edges[i].next_edge.origin)

            twin_next.set_name(f"{self.semi_edges[i].prev_edge.name}''")
            twin_prev.set_name(f"{self.semi_edges[i].next_edge.name}''")

            self.semi_edges[i].twin.set_next_edge(twin_next)
            self.semi_edges[i].twin.set_prev_edge(twin_prev)
        
        # add faces to the semi-edges
        self._set_faces(self.semi_edges)

        return self.semi_edges

    def _set_faces(self, edges: List[SemiEdge]) -> None:
        """
            This function adds the faces to the semi-edges.

            The idea is to take a semi-edge, and iter to the next semi-edge until
            we reach the initial semi-edge. All the semi-edges that we visited until 
            reaching the initial semi-edge form a face.
        """

        faces_count = 0

        # We iterate over the semi-edges
        for semi_edge in edges:

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
                face.add_semi_edge(next_semi_edge)

                # While the next semi-edge is not the initial semi-edge
                while next_semi_edge != semi_edge:
                    #print(f"\t next_semi_edge: {next_semi_edge}, semi_edge: {semi_edge}, face: {face}, face_count: {faces_count}")

                    # We iterate over the next semi-edge
                    next_semi_edge = next_semi_edge.next_edge

                    # We add the face to the semi-edge
                    next_semi_edge.incident_face = face

                    # We add the semi-edge to the face
                    face.add_semi_edge(next_semi_edge)

                face.set_face_type()
                self.faces.append(face)
                faces_count += 1

    def add_new_edge(self, semiedge: SemiEdge) -> None:

        #check if the semiedge is already in the list of semiedges
        if semiedge in self.semi_edges:
            return

        twin = SemiEdge(origin = semiedge.next_,
                        next_  = semiedge.origin)

        #add the twin and semiedge name 
        semiedge.set_name(f"SE{len(self.semi_edges)}")
        twin.set_name(f"SE{len(self.semi_edges)}''")

        #identify the semiedges with origin in any of the ends 
        #of the semiedge I want to add

        #print(f"I want to add {semiedge}")
        related_edges_orig = self.get_incident_edges_of_vertex(semiedge.origin)
        related_edges_next = self.get_incident_edges_of_vertex(semiedge.next_)

        #from those related edges filter the ones that have the same incident face and 
        #that are exterior frontier 
        related_edges_orig = [e for e in related_edges_orig if e.incident_face.face_type == Face.EXTERIOR_FACE]
        related_edges_next = [e for e in related_edges_next if e.incident_face.face_type == Face.EXTERIOR_FACE]

        related_edges = related_edges_orig + related_edges_next
        found = False
        pair: Tuple[SemiEdge, SemiEdge] = ()
        #print(f"RELATED EDGES {related_edges}")

        #search the pair that has the same incident face
        for e1 in related_edges:
            for e2 in related_edges:

                if (e1.incident_face == e2.incident_face) and (e1 != e2):
                    pair = (e1, e2)
                    found = True
                    break
            if found:
                break

        if not found:
            raise Exception("No pair of edges found")
        
        related_a = pair[0] if pair[0].origin == semiedge.origin else pair[1]
        related_b = pair[1] if related_a == pair[0] else pair[0]
        
        #reset prev edge of existent edges in the polygon
        related_a.prev_edge.set_next_edge(semiedge)
        related_b.prev_edge.set_next_edge(twin)

        #set the previous edges of the new semiedges
        semiedge.set_prev_edge( related_a.prev_edge )
        twin.set_prev_edge( related_b.prev_edge )

        #set the next edges of the new semiedges 
        semiedge.set_next_edge( related_b )
        twin.set_next_edge( related_a )

        #reset the prev edge of the existent edges in polygon
        related_b.set_prev_edge(semiedge) 
        related_a.set_prev_edge(twin)   

        semiedge.twin = twin
        self.semi_edges.append(semiedge)
        
        #set origin and next vertex names
        semiedge.origin.name = related_edges_orig[0].origin.name
        semiedge.next_.name = related_edges_next[0].origin.name
        twin.origin.name = related_edges_next[0].origin.name
        twin.next_.name = related_edges_orig[0].origin.name

        #reset the faces of the polygon
        self._reset_faces()

    def get_incident_edges_of_vertex(self, vertex: GeometricNode) -> List[SemiEdge]:

        starts_at_vertex = []

        for semiedge in self.semi_edges:
            if semiedge.origin == vertex:
                starts_at_vertex.append(semiedge)

        return starts_at_vertex

    def _reset_faces(self):
        self.faces = []

        for s in self.semi_edges:
            #remove the face from memory
            del s.incident_face
            del s.twin.incident_face

            #remove the face from attributes
            s.incident_face = None
            s.twin.incident_face = None
        
        self._set_faces(self.semi_edges)

    def __getitem__(self, index: int) -> SemiEdge:
        return self.semi_edges[index]

    def __len__(self) -> int:
        return len(self.semi_edges)
    
    def __iter__(self):
        return iter(self.semi_edges)

    def __str__(self) -> str:
        return f"{self.semi_edges}"
    
    def __repr__(self) -> str:
        return f"{self.semi_edges}"