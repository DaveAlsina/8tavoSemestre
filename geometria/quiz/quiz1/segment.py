#strandard dependencies
import numpy as np
from typing import Union, List

#custom dependencies
from vector import Vector

class Segment():

    def __init__(self, start: Vector, end: Vector, sort_ends = False) -> None:
        """
            This class is used to represent a segment in 2D space.
            start and end are the vertices of the segment. Starting from start, and ending in end.
        """
        self.start = start
        self.end = end

        #make sure that the start is the lowest leftmost point, 
        #refer to our order operator overload in vector.py
        if sort_ends and (self.start > self.end):
            self.start, self.end = self.end, self.start


    def get_midpoint(self) -> Vector:
        """
            Calculates the midpoint of the segment.
        """
        return (self.start + self.end)/2

    def calcutale_slope(self) -> float:
        """
            Calculates the slope of segment.
        """
        deltas = self.end - self.start

        if deltas[0] == 0:
            return np.inf

        return (deltas[1])/(deltas[0])
        
    def calculate_distance(self) -> float:
        """
            Calculates the distance between end and v2.
        """
        return np.linalg.norm(self.end - self.start)

    
    def on_segment_area(self, v3: Vector) -> bool:
        """
            Checks if v3 is on the segment startend area,
            this area is defined by the rectangle with vertices start and end.
        """
        inx = min(self.start[0], self.end[0]) <= v3[0] <= max(self.start[0], self.end[0]) 
        iny = min(self.start[1], self.end[1]) <= v3[1] <= max(self.start[1], self.end[1])

        if (inx and iny):
            return True
        return False

    def direction(self, vector3: Vector) -> int:
        """
            Given our segment, and a vector3, determine if vector3 is rotated clockwise or anticlockwise, 
            or if they are colineal, with respect to the segment.
        """
        det = np.linalg.det(np.column_stack([(vector3 - self.start).vector, (self.end - self.start).vector]))

        if det < 0:
            return -1
        elif det > 0:
            return 1
        return 0

    def segments_intersect(self, other_segment: 'Segment') -> bool:

        """
            Given one segment, determine if the segments they form intersect.
            Segments are startend from self, and startend from other_segment.
        """

        #directions with respect to other_segment
        dir1 = other_segment.direction(self.start)
        dir2 = other_segment.direction(self.end)
        
        #directions with respect to self
        dir3 = self.direction(other_segment.start)
        dir4 = self.direction(other_segment.end)

        #well behaved case
        if (dir1*dir2 < 0) and (dir3*dir4 < 0):
            return True
    
        #collinear case with respect to other_segment
        elif (dir1 == 0) and (other_segment.on_segment_area(self.start)):
            return True

        elif (dir2 == 0) and (other_segment.on_segment_area(self.end)):
            return True

        #collinear case with respect to self
        elif (dir3 == 0) and (self.on_segment_area(self.on_segment_area.start)):
            return True

        elif (dir4 == 0) and (self.on_segment_area(self.on_segment_area.end)):
            return True
        
        else:
            return False
    
    def find_intersection(self, other_segment: 'Segment') -> Vector:
        """
            Finds the intersection of the lines formed by the segments endv2 and v3v4.
        """

        difference1 = (self.start - self.end).vector
        difference2 = (other_segment.start - other_segment.end).vector
        result = (other_segment.start - self.end).vector

        matrix = np.column_stack([difference1, difference2])
        alpha_beta = np.linalg.solve(matrix, result)

        intersect = self.start*float(alpha_beta[0]) + float(1 - alpha_beta[0])*self.end

        print(f"alpha: {alpha_beta[0]}, beta: {alpha_beta[1]}, intersect: {intersect}")
        print(f"intersect type {alpha_beta[0].shape}")

        return intersect

    @staticmethod
    def build_random_segments(nsegments: int=10)-> List['Segment']:
        """
            Builds nsegments random segments.
        """
        segments = []

        for _ in range(nsegments):
            start = Vector.build_random_vectors(1)[0]
            end = Vector.build_random_vectors(1)[0]
            segments.append(Segment(start, end))

        return segments

    def __repr__(self) -> str:
        return f"Segment({self.start}, {self.end})"