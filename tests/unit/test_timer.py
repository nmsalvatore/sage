from unittest import TestCase

from fizz.utils import time_in_seconds


class TestTimer(TestCase):
    """
    Testing suite for fizz timer.
    """

    def test_time_in_seconds(self):
        """
        Test utility function `time_in_seconds` which converts hours,
        minutes and seconds to total seconds.
        """
        self.assertEqual(time_in_seconds(hours=1), 3600)
        self.assertEqual(time_in_seconds(hours=1, minutes=30), 5400)
        self.assertEqual(time_in_seconds(hours=2, seconds=5), 7205)
        self.assertEqual(time_in_seconds(minutes=30, seconds=25), 1825)
