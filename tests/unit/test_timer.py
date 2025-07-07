from unittest import TestCase

from sage.clocks import Timer


class TestTimer(TestCase):
    """
    Testing suite for sage timer.
    """

    def test_get_timer_duration(self):
        """
        Test that `get_timer_duration` gets the correct time, depending
        on how the arguments are passed to `sage timer`.
        """
        timer = Timer()
        self.assertEqual(timer.get_timer_duration(time_string="2m 3s"), 123)
        self.assertEqual(timer.get_timer_duration(hours=1), 3600)
        self.assertEqual(timer.get_timer_duration(0, 5), 300)
        self.assertEqual(timer.get_timer_duration(time_string="2 minute 60s"), 180)
