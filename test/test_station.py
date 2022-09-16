import unittest
from src.main import LinkStation, Device

class TestStation(unittest.TestCase):
    def test_power_in_reach(self):
        l = LinkStation(1,6,8)
        d = Device(1,6)
        power = l.get_power(d)

        self.assertEqual(power, 64)

    def test_power_not_in_reach(self):
        l = LinkStation(1,2,5)
        d = Device(7,8)
        power = l.get_power(d)

        self.assertEqual(power, 0)

if __name__ == "__main__":
    unittest.main()