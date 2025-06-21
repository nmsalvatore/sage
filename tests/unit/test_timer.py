from unittest import TestCase

from fizz.utils import convert_time_to_seconds, expand_time_from_seconds


class TestBasicTimer(TestCase):
    """
    Testing suite for fizz timer.
    """

    def test_convert_time_to_seconds(self):
        """
        Test utility function `convert_time_to_seconds` which converts hours,
        minutes and seconds to total seconds.
        """
        self.assertEqual(convert_time_to_seconds(hours=1), 3600)
        self.assertEqual(convert_time_to_seconds(hours=1, minutes=30), 5400)
        self.assertEqual(convert_time_to_seconds(hours=2, seconds=5), 7205)
        self.assertEqual(convert_time_to_seconds(minutes=30, seconds=25), 1825)

    def test_expand_time_from_seconds(self):
        """
        Test utility function `expand_time_from_seconds` which expands
        a time in seconds to hours, minutes, and seconds.
        """
        self.assertEqual(expand_time_from_seconds(65), (0, 1, 5))
        self.assertEqual(expand_time_from_seconds(3657), (1, 0, 57))
        self.assertEqual(expand_time_from_seconds(28933), (8, 2, 13))
