from unittest import TestCase

from fizz.utils import time_in_seconds


class TestTimer(TestCase):
    def test_time_in_seconds(self):
        self.assertEqual(time_in_seconds(1), 3600)
