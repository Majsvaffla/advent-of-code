import unittest

from part_one import decode_seat


class TestPartOne(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(decode_seat("FBFBBFFRLR"), (44, 5, 357))
        self.assertEqual(decode_seat("BFFFBBFRRR"), (70, 7, 567))
        self.assertEqual(decode_seat("FFFBBBFRRR"), (14, 7, 119))
        self.assertEqual(decode_seat("BBFFBBFRLL"), (102, 4, 820))

if __name__ == '__main__':
    unittest.main()
