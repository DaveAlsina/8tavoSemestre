#strandard dependencies
import numpy as np
from typing import Union, List

#custom dependencies
from vector import Vector

class Segment():

    def __init__(self, v0: Vector, v1: Vector) -> None:
        """
            This class is used to represent a segment in 2D space.
            v0 and v1 are the vertices of the segment. Starting from v0, and ending in v1.
        """
        self.v0 = v0
        self.v1 = v1

    def __repr__(self) -> str:
        return f"Segment({self.v0}, {self.v1})"

    def get_midpoint(self) -> Vector:
        """
            Calculates the midpoint of the segment.
        """
        return (self.v0 + self.v1)/2

    def calcutale_slope(self) -> float:
        """
            Calculates the slope of segment.
        """
        deltas = self.v1 - self.v0

        if deltas[0] == 0:
            return np.inf

        return (deltas[1])/(deltas[0])
        
    def calculate_distance(self) -> float:
        """
            Calculates the distance between v1 and v2.
        """
        return np.linalg.norm(self.v1 - self.v0)

    
    def on_segment_area(self, v3: Vector) -> bool:
        """
            Checks if v3 is on the segment v0v1 area,
            this area is defined by the rectangle with vertices v0 and v1.
        """
        inx = min(self.v0[0], self.v1[0]) <= v3[0] <= max(self.v0[0], self.v1[0]) 
        iny = min(self.v0[1], self.v1[1]) <= v3[1] <= max(self.v0[1], self.v1[1])

        if (inx and iny):
            return True
        return False

    def direction(self, vector3: Vector) -> int:
        """
            Given our segment, and a vector3, determine if vector3 is rotated clockwise or anticlockwise, 
            or if they are colineal, with respect to the segment.
        """
        det = np.linalg.det(np.column_stack([(vector3 - self.v0).vector, (self.v1 - self.v0).vector]))

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0

    def segments_intersect(self, other_segment: 'Segment') -> bool:

        """
            Given one segment, determine if the segments they form intersect.
            Segments are v0v1 from self, and v0v1 from other_segment.
        """

        #directions with respect to other_segment
        dir1 = other_segment.direction(self.v0)
        dir2 = other_segment.direction(self.v1)
        
        #directions with respect to self
        dir3 = self.direction(other_segment.v0)
        dir4 = self.direction(other_segment.v1)

        #well behaved case
        if (dir1*dir2 < 0) and (dir3*dir4 < 0):
            return True
    
        #collinear case with respect to other_segment
        elif (dir1 == 0) and (other_segment.on_segment_area(self.v0)):
            return True

        elif (dir2 == 0) and (other_segment.on_segment_area(self.v1)):
            return True

        #collinear case with respect to self
        elif (dir3 == 0) and (self.on_segment_area(self.on_segment_area.v0)):
            return True

        elif (dir4 == 0) and (self.on_segment_area(self.on_segment_area.v1)):
            return True
        
        else:
            return False
    
    def find_intersection(self, other_segment: 'Segment') -> Vector:
        """
            Finds the intersection of the lines formed by the segments v1v2 and v3v4.
        """

        difference1 = (self.v0 - self.v1).vector
        difference2 = (other_segment.v0 - other_segment.v1).vector

        matrix = np.column_stack([difference1, difference2])
        result = self.v0 - other_segment.v0
        intersection = np.linalg.solve(matrix, result)

        return Vector(intersection)

    @staticmethod
    def build_random_segments(nsegments: int=10):
        """
            Builds nsegments random segments.
        """
        segments = []

        for _ in range(nsegments):
            v0 = Vector.build_random_vectors(1)[0]
            v1 = Vector.build_random_vectors(1)[0]
            segments.append(Segment(v0, v1))

        return segments