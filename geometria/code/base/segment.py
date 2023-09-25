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

    
    def on_segment(self, v3: Vector) -> bool:
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

            Output:
                1: if the walk is a left turn
                -1: if the walk is a right turn
                0: if the points are collinear
        """
        det = np.linalg.det(np.column_stack([(vector3 - self.start).vector, (self.end - self.start).vector]))
        return np.sign(det)

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
        elif (dir1 == 0) and (other_segment.on_segment(self.start)):
            return True

        elif (dir2 == 0) and (other_segment.on_segment(self.end)):
            return True

        #collinear case with respect to self
        elif (dir3 == 0) and (self.on_segment(self.start)):
            return True

        elif (dir4 == 0) and (self.on_segment(self.end)):
            return True
        
        else:
            return False
    
    def get_intersection_of_segments_general(self, other_segment: 'Segment') -> Union['Segment', Vector]:

        """
            This method uses the find_intersection_on_endpoints, 
            the find_intersection, and the find_interval_intersection methods,
            which respectively get the intersect on endpoints (if any),
            the intersection between segments (if any), 
            and the intersection on an interval (if any).
        """
    
        # Find the intersection point (if any)
        intersection = self.find_intersection(other_segment)

        # Find the intersection on endpoints (if any)
        intersection_on_endpoints = self.find_intersection_on_endpoints(other_segment)

        # Find the intersection on segments (if any)
        intersection_on_segments = self.find_interval_intersection(other_segment)

        if intersection_on_segments is not None:
            return intersection_on_segments
        elif intersection_on_endpoints is not None:
            return intersection_on_endpoints
        else:
            return intersection


    
    def find_intersection_on_endpoints(self, other_segment: 'Segment') -> Union['Segment', None]:
        """
            Finds the intersection of the segments on the endpoints.
        """
        if (self.start == other_segment.start) or (self.start == other_segment.end):
            return self.start
        elif (self.end == other_segment.start) or (self.end == other_segment.end):
            return self.end
        else:
            return None
    
    def find_intersection(self, other_segment: 'Segment') -> Vector:
        """
            Finds the intersection of the lines formed by the segments endv2 and v3v4.
        """

        difference1 = (self.start - self.end).vector
        difference2 = (other_segment.start - other_segment.end).vector
        result = (other_segment.start - self.end).vector

        matrix = np.column_stack([difference1, difference2])
        
        #if the matrix is singular, then the lines are parallel, 
        # but they might intersect on the endpoints
        try:
            alpha_beta = np.linalg.solve(matrix, result).reshape(2,)

        except np.linalg.LinAlgError as e:
            if 'Singular matrix' in str(e):
                return self.find_intersection_on_endpoints(other_segment)
            else: 
                raise e
            
        intersect = self.start.times_scalar(alpha_beta[0]) + self.end.times_scalar(float(1 - alpha_beta[0]))

        return intersect
    
    def find_interval_intersection(self, other_segment: 'Segment') -> Union['Segment', None]:
        """
            Finds the interval intersection of the segments.
            If there is no intersection, return None.
        """

        #check if the segments have the same slope
        same_slope = self.calcutale_slope() == other_segment.calcutale_slope()

        # given that they have the same slope, check one of the 
        # segments is contained in the other, we do this by taking the endpoints of the segments
        # and checking if they are contained in the other segment
        p0_on_segment = other_segment.on_segment(self.start)
        p1_on_segment = other_segment.on_segment(self.end)
        p2_on_segment = self.on_segment(other_segment.start)
        p3_on_segment = self.on_segment(other_segment.end)
        ans = None

        if same_slope:
            if (p0_on_segment and p1_on_segment):
                ans =  Segment(self.start, self.end)
            elif (p2_on_segment and p3_on_segment):
                ans = Segment(other_segment.start, other_segment.end)
            elif (p0_on_segment and p3_on_segment):
                ans = Segment(self.start, other_segment.end)
            elif (p2_on_segment and p1_on_segment):
                ans = Segment(other_segment.start, self.end)
            else:
                return ans
        else:
            return ans

        #there could be a posibility that it matches as a segment
        #something that it's indeed a point
        if ans.start == ans.end:
            return None 
        else:
            return ans

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
    
    def __eq__(self, other_segment: 'Segment') -> bool:

        if (self is not None and other_segment is None) or (self is None and other_segment is not None):
            return False

        self_set = set([self.start, self.end])
        other_set = set([other_segment.start, other_segment.end])
        return self_set == other_set
        
    def __ne__(self, other_segment: 'Segment') -> bool:
        return not self.__eq__(other_segment)
    
    def __hash__(self):
        return hash((self.start, self.end))