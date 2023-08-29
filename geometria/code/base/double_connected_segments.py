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

        if incident_edge is None:
            self.incident_edge = str(self.name) + "1"
        else:
            self.incident_edge = incident_edge

        if twin is None:
            self.twin = GeometricNode.build_twin(self.name)
        else:
            self.twin = twin

    @staticmethod
    def build_twin(name):
        if name[-1] == "2":
            return name[:-1] + "1"
        else:
            return name[:-1] + "2"

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
        self.next = next
        self.prev = prev
        self.face = incident_face
    
    def __repr__(self) -> str:
        return f"SemiEdge({self.origin} >> {self.next})"


class Face():
    def __init__(self, name: str,
                       incident_edge: str):
        self.name = name
        self.incident_edge = incident_edge