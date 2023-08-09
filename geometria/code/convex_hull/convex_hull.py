import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from base import SwissArmyKnifeVector
from base import Vector
from utils import build_many_vectors

class ConvexHull:

    def __init__(self):
        self.util = SwissArmyKnifeVector()

    #========================================
    #           Small subroutines
    #========================================
    def get_stating_point(self, *points: Vector) -> Vector:

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


    def find_repeated_and_unique_slopes(self, *slopes: float) -> list:

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



    def sort_by_slope(self, v0: Vector, *points: Vector) -> list:

        """
            Sorts the points by the slope in ascending order.
            The slope is computed with respect to v0.

            If there are more than one point with the same slope,
            the one further away to v0 is chosen.
        """

        # calculate the slope of each point with respect to v0
        slopes = [self.util.calcutale_slope(v0, point) for point in points]

        # find the repeated slopes indexes
        repeated_slopes, unique_slopes = self.find_repeated_and_unique_slopes(*slopes)

        # list with the points which have a unique slope or the furthest point from v0
        filtered_points = [points[i] for i in unique_slopes]

        # if there are repeated slopes, find the furthest point from v0 to each repeated slope
        for indexes in repeated_slopes:
            repeated_points = [points[i] for i in indexes]
            furthest_point = self.find_furthest_point(v0, *repeated_points)
            filtered_points.append(furthest_point)

        # sort the filtered points by the slope in ascending order
        slopes = [(point, self.util.calcutale_slope(v0, point)) for i, point in enumerate(filtered_points)]
        slopes.sort(key = lambda x: x[1])

        return [point for point, slope in slopes]



    #========================================
    #           Main algorithm
    #========================================

    def convex_hull(self, *points: Vector) -> list:

        """
            Computes the convex hull of a set of points in the plane.
            The points must be given in the form of numpy arrays.
        """

        v0 = self.get_stating_point(*points)
        sorted_points = self.sort_by_slope(v0, *points)
        convex_hull = [v0, sorted_points[0], sorted_points[1]]

        for n in range(2, len(sorted_points)):
            v1 = convex_hull[-2]    # second to last point in the convex hull
            v2 = convex_hull[-1]    # last point in the convex hull
            v3 = sorted_points[n]   # next point to be added to the convex hull

            turn = self.util.turn(v1, v2, v3)
            
            # if v3 is rotated anticlockwise with respect to the v1-v2 line
            # don't add v2 to the convex hull
            if  turn == -1:
                convex_hull.pop()
                convex_hull.append(v3)

            # if v3 is rotated clockwise with respect to the v1-v2 line
            # add v3 to the convex hull and try again with the new v1-v2 line
            elif turn == 1:
                convex_hull.append(v3)

            # if v3 is colineal with respect to the v1-v2 line
            # choose the smallest distance between v0-v2 and v0-v3
            else:
                v0v2 = self.util.calculate_distance(v0, v2)
                v0v3 = self.util.calculate_distance(v0, v3)

                if v0v2 > v0v3:
                    convex_hull.pop()
                    convex_hull.append(v3)

        return convex_hull