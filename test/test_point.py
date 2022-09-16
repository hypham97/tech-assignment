import unittest
from src.main import Point

class TestPoint(unittest.TestCase):
    def test_equal(self):
        p1 = Point(3, 3)
        p2 = Point(8, 10)
        p3 = Point(3, 3)

        self.assertEqual(p1,p3)
        self.assertNotEqual(p2,p1)

    def test_validity(self):
        p = Point(8, 10)
        self.assertEqual(p.x, 8)
        self.assertEqual(p.y, 10)

    def test_distance(self):
        p1 = Point(0, 0)
        p2 = Point(4, 3)

        res = p1.get_distance(p2)
        self.assertEqual(res, 5)

if __name__ == "__main__":
    unittest.main()