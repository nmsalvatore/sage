from unittest import TestCase

from sage.clocks.timer import Timer


class TestTimer(TestCase):
    """
    Testing suite for sage timer.
    """

    def test_get_timer_duration(self):
        """
        Test that `get_duration` gets the correct time, depending
        on how the arguments are passed to `sage timer`.
        """
        timer = Timer()
        self.assertEqual(timer.get_duration("2m3sec"), 123)
        self.assertEqual(timer.get_duration("1hr"), 3600)
        self.assertEqual(timer.get_duration("5 minutes"), 300)
        self.assertEqual(timer.get_duration("2 minute 60s"), 180)
