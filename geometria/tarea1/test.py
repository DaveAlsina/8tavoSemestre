import unittest
import numpy as np
from segment import Segment
from vector import Vector

class TestSegment(unittest.TestCase):

    def test_intersect_of_two_segments(self):
        
        pair_point1 = (Vector(np.array([[0],[0]])), Vector(np.array([[1],[1]])))
        pair_point2 = (Vector(np.array([[0],[1]])), Vector(np.array([[1],[0]])))

        segment1 = Segment(pair_point1[0], pair_point1[1])
        segment2 = Segment(pair_point2[0], pair_point2[1])
        self.assertTrue(segment1.segments_intersect(segment2))

        # segments sharing an endpoint, and collineal
        pair_point3 = (Vector(np.array([[0],[0]])), Vector(np.array([[1],[1]])))
        pair_point4 = (Vector(np.array([[1],[1]])), Vector(np.array([[2],[2]])))

        segment3 = Segment(pair_point3[0], pair_point3[1])
        segment4 = Segment(pair_point4[0], pair_point4[1])

        self.assertTrue(segment3.segments_intersect(segment4))

    
    def test_no_intersect_of_two_segments(self):
            
        pair_point1 = (Vector(np.array([[0],[0]])), Vector(np.array([[1],[1]])))
        pair_point2 = (Vector(np.array([[0],[2]])), Vector(np.array([[1],[3]])))

        segment1 = Segment(pair_point1[0], pair_point1[1])
        segment2 = Segment(pair_point2[0], pair_point2[1])
        self.assertFalse(segment1.segments_intersect(segment2))

    def test_find_intersect(self):
        pair_point1 = (Vector(np.array([[0],[0]])), Vector(np.array([[1],[1]])))
        pair_point2 = (Vector(np.array([[0],[1]])), Vector(np.array([[1],[0]])))

        segment1 = Segment(pair_point1[0], pair_point1[1])
        segment2 = Segment(pair_point2[0], pair_point2[1])
        self.assertEqual(segment1.find_intersection(segment2), Vector(np.array([[0.5],[0.5]]))) 

        # perpendicular segments
        pair_point3 = (Vector(np.array([[0],[-1]])), Vector(np.array([[0],[1]])))
        pair_point4 = (Vector(np.array([[-1],[0]])), Vector(np.array([[1],[0]])))

        segment3 = Segment(pair_point3[0], pair_point3[1])
        segment4 = Segment(pair_point4[0], pair_point4[1])
        self.assertEqual(segment3.find_intersection(segment4), Vector(np.array([[0],[0]])))
    
        # segments sharing an endpoint
        pair_point5 = (Vector(np.array([[0],[0]])), Vector(np.array([[1],[1]])))
        pair_point6 = (Vector(np.array([[1],[1]])), Vector(np.array([[2],[2]])))

        segment5 = Segment(pair_point5[0], pair_point5[1])
        segment6 = Segment(pair_point6[0], pair_point6[1])

        self.assertEqual(segment5.find_intersection(segment6), Vector(np.array([[1],[1]])))
    
    def test_find_interval_intersect(self):
        #segment 1 shares an interval with segment 2
        pair_point1 = (Vector(np.array([[0],[0]])), Vector(np.array([[2],[2]])))
        pair_point2 = (Vector(np.array([[1],[1]])), Vector(np.array([[3],[3]])))

        segment1 = Segment(pair_point1[0], pair_point1[1])
        segment2 = Segment(pair_point2[0], pair_point2[1])
        self.assertEqual(segment1.find_interval_intersection(segment2), Segment(pair_point2[0], pair_point1[1]))

        #segment 4 is "contained" in segment 3
        pair_point3 = (Vector(np.array([[-2],[0]])), Vector(np.array([[2],[0]])))
        pair_point4 = (Vector(np.array([[-1],[0]])), Vector(np.array([[1],[0]])))

        segment3 = Segment(pair_point3[0], pair_point3[1])
        segment4 = Segment(pair_point4[0], pair_point4[1])
        self.assertEqual(segment3.find_interval_intersection(segment4), segment4)

        #segment 5 is the same as segment 5
        pair_point5 = (Vector(np.array([[0],[0]])), Vector(np.array([[1],[1]])))
        segment5 = Segment(pair_point5[0], pair_point5[1])
        self.assertEqual(segment5.find_interval_intersection(segment5), segment5)


    def test_no_find_interval_intersect(self):
        pair_point1 = (Vector(np.array([[0],[0]])), Vector(np.array([[1],[1]])))
        pair_point2 = (Vector(np.array([[0],[2]])), Vector(np.array([[1],[3]])))

        segment1 = Segment(pair_point1[0], pair_point1[1])
        segment2 = Segment(pair_point2[0], pair_point2[1])
        self.assertIsNone(segment1.find_interval_intersection(segment2))

    
if __name__ == '__main__':
    unittest.main()