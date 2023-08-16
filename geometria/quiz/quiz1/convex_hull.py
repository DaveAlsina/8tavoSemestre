import os, sys
import numpy as np
from typing import Union, List, Tuple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vector import Vector
from segment import Segment

class ConvexHull:

    def __init__(self):
        pass

    #========================================
    #           Small subroutines
    #========================================
    def get_starting_point(self, points: List[Vector]) -> Vector:
        """
            Returns the smallest point in the x coordinate, if there are more than one,
            returns the smallest in the y coordinate.
        """

        minimumx = min([point[0] for point in points])
        indexesx = [i for i, p in enumerate(points) if p[0] == minimumx]
        minimum_x_points = [points[i] for i in indexesx]

        #if there are more than one point with the smallest x coordinate
        minimumy = min([point[1] for point in minimum_x_points])
        indexesy = [i for i, p in enumerate(minimum_x_points) if p[1] == minimumy]

        return minimum_x_points[indexesy[0]]


    def find_repeated_and_unique_slopes(self, slopes: List[float]) -> Tuple[List[int], List[int]]:

        """
            Finds the indexes of the repeated slopes.

            Returns:
                all_repeated_indexes: list of lists with the indexes of the repeated slopes. Each sublist corresponds to a group of repeated slopes.
                all_unique_indexes: list with the indexes of the unique slopes.     
        """

        # list of lists, each sublist corresponds to a group of indexes of repeated slopes
        all_repeated_indexes = []
        # list of indexes of unique slopes
        all_unique_indexes = []

        for i, slope in enumerate(slopes):
            indexes = [j for j, s in enumerate(slopes) if s == slope and j != i]

            if indexes:
                all_repeated_indexes.append(indexes)
            else:
                all_unique_indexes.append(i)

        
        return all_repeated_indexes, all_unique_indexes



    def sort_by_slope(self, v0: Vector, points: List[Vector]) -> list:

        """
            Sorts the points by the slope in ascending order.
            The slope is computed with respect to v0.

            If there are more than one point with the same slope,
            the one further away to v0 is chosen.
        """

        # calculate the slope of each point with respect to v0
        slopes = [v0.calculate_slope(point) for point in points]

        # find the repeated slopes indexes
        repeated_slopes_idx, unique_slopes_idx = self.find_repeated_and_unique_slopes(slopes)

        # list with the points which have a unique slope or the furthest point from v0
        filtered_points = [points[i] for i in unique_slopes_idx]

        # if there are repeated slopes, find the furthest point from v0 to each repeated slope
        # and prefer it over the other points with the same slope
        for indexes in repeated_slopes_idx:
            repeated_points = [points[i] for i in indexes]
            furthest_point = v0.get_furthest_point(repeated_points)
            filtered_points.append(furthest_point)

        # sort the filtered points by the slope in ascending order
        slopes = [(point, v0.calculate_slope(point)) for i, point in enumerate(filtered_points)]
        slopes.sort(key = lambda x: x[1])

        return [point for point, slope in slopes]


    #========================================
    #           Main algorithm
    #========================================

    def convex_hull(self, points: List[Vector]) -> list:

        """
            Computes the convex hull of a set of points in the plane.
            The points must be given in the form of numpy arrays.
        """

        #gets the leftmost lowest point
        v0 = self.get_stating_point(points)

        #based on this leftmost lowest point, sort the points by the slope in ascending order
        sorted_points = self.sort_by_slope(v0, points)

        #initialize the convex hull with the first three points
        convex_hull = [v0, sorted_points[0], sorted_points[1]]

        for n in range(2, len(sorted_points)):

            v1 = convex_hull[-2]    # second to last point in the convex hull
            v2 = convex_hull[-1]    # last point in the convex hull
            v3 = sorted_points[n]   # next point to be added to the convex hull
            
            #This loop is what i'd call the fixing mistakes (or dropping) loop:

            # while there are more than two points in the convex hull
            # and v3 is rotated anticlockwise with respect to the v1-v2 line
            while len(convex_hull) > 2 and (Segment(v1, v2).direction(v3) >= 0):
                # remove v2 from the convex hull,
                # because it is not part of the convex hull                
                convex_hull.pop()       
                                        
                v1 = convex_hull[-2]
                v2 = convex_hull[-1]
            
            # add v3 to the convex hull
            convex_hull.append(v3)


        return convex_hull