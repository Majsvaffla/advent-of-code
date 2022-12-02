import unittest

from part_one import count_unique_positive_answers


class TestPartOne(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(count_unique_positive_answers(["abc"]), 3)
        self.assertEqual(count_unique_positive_answers(["a", "b", "c"]), 3)
        self.assertEqual(count_unique_positive_answers(["ab", "ac"]), 3)
        self.assertEqual(count_unique_positive_answers(["a", "a", "a", "a"]), 1)
        self.assertEqual(count_unique_positive_answers(["b"]), 1)

if __name__ == '__main__':
    unittest.main()
