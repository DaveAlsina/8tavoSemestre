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
        
        self._fix_orientation(list_of_points)
        self._build_nodes(list_of_points)
        self._build_semi_edges()
    
    def _fix_orientation(self, list_of_points: List[Vector]) -> None:
        """
            This method reverses the orientation of the polygon if it's clockwise.
            Otherwise, it does nothing.
        """

        #get the leftmost point of the polygon which is one of the points of the
        #convex hull, by looking at the prev and next points of the leftmost point
        #and then computing the turn of the three points (prev, leftmost, next)
        #we can determine if the polygon is clockwise or counterclockwise
        envelope_component = Vector.get_leftmost_point(list_of_points)

        #get the index of the leftmost point
        index = list_of_points.index(envelope_component)

        #get the prev and next points of the leftmost point
        prev_point = list_of_points[(index-1)%len(list_of_points)]
        next_point = list_of_points[(index+1)%len(list_of_points)]

        #get the turn of the three points
        turn = Vector.calculate_turn(prev_point, envelope_component, next_point)

        if turn == Vector.CLOCKWISE_TURN:
            list_of_points.reverse()

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

        #

        for i in range(len(list_of_points)):
            node = GeometricNode(point = list_of_points[i], name = f"{self.name}N{i}")

            #avoid adding repeated nodes
            if node not in self.list_of_nodes:
                self.list_of_nodes.append(node)
            else:
                raise Exception("Repeated node, watch out!")

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

        # Set the next and prev edges of each twin semi-edge
        for i in range(len(self.semi_edges)):
            self.semi_edges[i].twin.set_next_edge(self.semi_edges[(i-1)%len(self.semi_edges)].twin) 
            self.semi_edges[i].twin.set_prev_edge(self.semi_edges[(i+1)%len(self.semi_edges)].twin)
        
        # add faces to the semi-edges
        self._set_faces(self.semi_edges)
        self._set_faces(self.semi_edges, twins=True)

        return self.semi_edges

    def _reset_faces(self):
        """
            This function resets the faces of the polygon.
            This is necessary because when we add a new edge, we have to
            reset the faces of the polygon, because the faces are not correct
            anymore.
        """
        self.faces = []

        for s in self.semi_edges:
            #remove the face from memory
            del s.incident_face
            del s.twin.incident_face

            #remove the face from attributes
            s.incident_face = None
            s.twin.incident_face = None
        
        self._set_faces(self.semi_edges)
        self._set_faces(self.semi_edges, twins=True)

    def _set_faces(self, 
                   edges: List[SemiEdge], 
                   twins: bool = False) -> None:
        """
            This function adds the faces to the semi-edges.

            The idea is to take a semi-edge, and iter to the next semi-edge until
            we reach the initial semi-edge. All the semi-edges that we visited until 
            reaching the initial semi-edge form a face.

            Input:
            --------
                edges: List[SemiEdge]
                    The list of semi-edges to which we want to add the faces
                
                twins: bool
                    If True, then it's referring to add the faces to the twins of the
                    semi-edges. If False, then it's referring to add the faces to the
                    semi-edges.
        """

        faces_count = 0

        # We iterate over the semi-edges
        for semi_edge in edges:

            if twins:
                semi_edge = semi_edge.twin

            #print(f"iterating over semi-edge {semi_edge}, face: {semi_edge.incident_face}, face_count: {faces_count}")
            # If the semi-edge doesn't have a face, then we add a face
            if semi_edge.incident_face == None:
                
                # We create a new face
                if twins:
                    face_name = f"{semi_edge.twin.name}''" #name for twin face
                else:
                    face_name = f"{self.name}:F{faces_count}" #name for face

                face = Face(name = face_name)

                # We iterate over the next semi-edge
                next_semi_edge = semi_edge.next_edge

                # We set the face to the semi-edge
                semi_edge.incident_face = face
                next_semi_edge.incident_face = face

                # We add the semi-edge to the face
                face.add_semi_edge(semi_edge)
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
                faces_count += 1

                if not twins:
                    self.faces.append(face)

    def add_new_edge(self, semiedge: SemiEdge) -> None:
        """
            This function adds a new edge to the list of semi-edges.
            This is a delicate process, because with each semi-edge we add
            it's necessary to add the next and prev edges of each semi-edge.
        """

        #check if the semiedge is already in the list of semiedges
        if semiedge in self.semi_edges:
            print("The semiedge is already in the list of semiedges")
            return

        twin = SemiEdge(origin = semiedge.next_,
                        next_  = semiedge.origin)

        #add the twin and semiedge name 
        semiedge.set_name(f"SE{len(self.semi_edges)}")
        twin.set_name(f"SE{len(self.semi_edges)}''")

        #identify the semiedges with origin in any of the ends 
        #of the semiedge I want to add

        print(f"I want to add {semiedge}, {semiedge.seg}")
        related_edges_orig = self.get_incident_edges_of_vertex(semiedge.origin)
        related_edges_next = self.get_incident_edges_of_vertex(semiedge.next_)

        #from those related edges filter the ones that have the same incident face and 
        #that are exterior frontier 
        related_edges_orig = [e for e in related_edges_orig if e.incident_face.face_type == Face.EXTERIOR_FACE]
        related_edges_next = [e for e in related_edges_next if e.incident_face.face_type == Face.EXTERIOR_FACE]

        related_edges = related_edges_orig + related_edges_next
        found = False
        pair: Tuple[SemiEdge, SemiEdge] = ()
        print(f"RELATED EDGES {related_edges}")

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
        """
            This function returns the edges that have the vertex as origin.

            Input:
            -------
                vertex: GeometricNode
                    The vertex to which the edges start

            Output:
            -------
                starts_at_vertex: List[SemiEdge]
                    The list of edges that start at the vertex
        """

        starts_at_vertex = []

        for semiedge in self.semi_edges:
            if semiedge.origin == vertex:
                starts_at_vertex.append(semiedge)
            elif semiedge.twin.origin == vertex:
                starts_at_vertex.append(semiedge.twin)

        return starts_at_vertex

    def resync(self) -> None:
        """this function resyncs the list of nodes and semi-edges, 
           this is necessary when we deal with copies of the nodes and maybe two 
           semiedges share an end but they are not the same object"""
        
        #get the list of nodes
        self.list_of_nodes = [semiedge.origin for semiedge in self.semi_edges]
        
        #drop the repeated nodes
        self.list_of_nodes = list(set(self.list_of_nodes))

        #for each incident edge of each node we set the origin and next vertex
        #to the node that is in the list of nodes

        for node in self.list_of_nodes:
            incident_edges = self.get_incident_edges_of_vertex(node)

            for incident_edge in incident_edges:
                incident_edge.origin = node

            for incident_edge in incident_edges:
                #seach the incident_edge.next_ in the list of nodes
                idx = self.list_of_nodes.index(incident_edge.next_)
                incident_edge.next_ = self.list_of_nodes[idx]


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