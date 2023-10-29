#external dependencies
import os, sys
import numpy as np
from matplotlib import pyplot as plt
from typing import Union, List, Tuple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#internal dependencies
from vector import Vector
from segment import Segment

class ConvexHullJarvis:

    def __init__(self):
        """
            Implements the Jarvis algorithm to find the convex hull of a set of points.
        """

        self.fig = plt.figure()
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


    #========================================
    #         Important loops
    #========================================
    def look_for_most_anti_clockwise_point(self,
                                           on_hull: Vector,
                                           points: List[Vector],
                                           plotting: bool = False) -> Vector:
        
        """
            Search for a point 'v' such that the rotation of the triplet (on_hull, points[i], v)
            is anti-clockwise, for all the i in the range [0, len(points)-1].
        """

        #initialize the segment with the first point
        segment = Segment(on_hull, points[0])

        for point in points[1:]:
            
            if plotting:
                self.plot_segment(on_hull, segment.end, point)

            #if the rotation is anti-clockwise, means that there is a point more anti-clockwise
            if segment.direction(point) == -1:
                segment = Segment(on_hull, point)
            
        return segment.end
    
    
    #========================================
    #          Main algorithm
    #========================================
    def convex_hull(self,
                    points: List[Vector], 
                    plotting: bool = False) -> List[Vector]:

        if len(points) < 3:
            raise ValueError("The convex hull can only be computed for 3 or more points.")
        self.points = points

        # get the starting point
        v0 = self.get_starting_point(points)

        # initialize the convex hull
        self.convex_hull = [v0,]

        # get the point with the highest slope
        v1 = self.look_for_most_anti_clockwise_point(v0, points, plotting)

        # while the next point is not the starting point
        while v1 != v0:
            # add the point to the convex hull
            self.convex_hull.append(v1)
            # remove the point from the list of points to check
            points.remove(v1)
            
            # get the next point
            v1 = self.look_for_most_anti_clockwise_point(self.convex_hull[-1], points, plotting)
        
        return self.convex_hull


    #========================================
    #              Animation 
    #========================================

    def plot_segment(self, on_hull: Vector, nextv: Vector, point: Vector):

        self.fig.clear()
        
        #the first segment bewteen on_hull and nextv is red and thick
        plt.plot([on_hull[0], nextv[0]], [on_hull[1], nextv[1]], 'r', linewidth=3)

        #plot the lines in the convex hull with red and thick, same as before
        for i in range(len(self.convex_hull)-1):
            plt.plot([self.convex_hull[i][0], self.convex_hull[i+1][0]],
                     [self.convex_hull[i][1], self.convex_hull[i+1][1]], 'r', linewidth=3)

        #the second segment between on_hull and point is black, thin and dashed
        plt.plot([on_hull[0], point[0]], [on_hull[1], point[1]], 'k--', linewidth=1)

        #the on_hull point and the nextv point are black
        plt.plot(on_hull[0], on_hull[1], 'ko')
        plt.plot(nextv[0], nextv[1], 'ko')

        #plot the rest of the points with a grey x marker
        for p in self.points:
            plt.plot(p[0], p[1], 'x', color='grey')

        plt.draw()
        plt.show()