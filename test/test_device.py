import unittest
from src.main import LinkStation, Device

class TestStation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.linkstations = [
            LinkStation(21, 0, 15),
            LinkStation(0, 13, 22),
            LinkStation(20, 12, 1)
        ]
    
    def test_best_station(self):
        device = Device(21, 13)
        station, power = device.get_best_station(self.linkstations)

        self.assertEqual(station, self.linkstations[0])
        self.assertEqual(power, 4)

    def test_no_station(self):
        device = Device(123, 34)
        station, power = device.get_best_station(self.linkstations)

        self.assertIsNone(station)
        self.assertEqual(power, 0)

if __name__ == "__main__":
    unittest.main()