from vector import Vector
from segment import Segment
from typing import List
from convex_hull import ConvexHull

class Poligon:

    def __init__(self, vertex_set: List[Vector]):
        self.vertex_set = vertex_set
        self.convex_hull = ConvexHull()

    def __str__(self):
        return str(self.vertex_set)
    
    def __repr__(self):
        return str(self.vertex_set)

    def check_directions(self, directions: list[int]) -> bool:
        """
            Checks if there is at least one direction which goes the opposite to the rest.
        """
        count = {0: 0, 1: 0, -1: 0}

        for direction in directions:
            count[direction] += 1

        if (count[1] * count[-1]) > 0:
            return True
        return False

    def is_convex(self):

        #gets the leftmost lowest point
        self.starting_point = self.convex_hull.get_starting_point(self.vertex_set)

        #based on this leftmost lowest point, sort the points by the slope in ascending order
        self.vertex_set = self.convex_hull.sort_by_slope(self.starting_point, self.vertex_set)

        #get the first two points
        v1 = self.vertex_set[0]
        v2 = self.vertex_set[1]

        print(f"type of v1: {type(v1)}")
        directions = []

        for v in self.vertex_set[2:]:
            segment = Segment(v1, v2)
            directions.append(segment.direction(v))
            print(directions)

            v1 = v2
            v2 = v

            #if there is at least one turn which goes the opposite to the rest 
            #then the poligon is not convex
            if (len(directions) > 1) and self.check_directions(directions):
                return False

        return True   
         
