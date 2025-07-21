from unittest import TestCase

from sage.common.formatting import time_as_clock, time_in_english


class TimeFormattingTests(TestCase):
    """
    Test suite for time formatting.
    """

    def test_clock_format(self):
        """
        Test proper formatting of clock, provided given seconds.
        """
        self.assertEqual(time_as_clock(185), "00:03:05")
        self.assertEqual(time_as_clock(25200), "07:00:00")
        self.assertEqual(time_as_clock(4), "00:00:04")
        self.assertEqual(time_as_clock(1500), "00:25:00")

    def test_clock_format_with_centiseconds(self):
        """
        Test proper formatting of clock with centiseconds.
        """
        self.assertEqual(time_as_clock(133.23, include_centiseconds=True), "00:02:13:23")
        self.assertEqual(time_as_clock(185.11, include_centiseconds=True), "00:03:05:11")
        self.assertEqual(time_as_clock(4, include_centiseconds=True), "00:00:04:00")
        self.assertEqual(time_as_clock(10800.7, include_centiseconds=True), "03:00:00:70")

    def test_format_time_in_english(self):
        """
        Test proper formatting of time into English.
        """
        self.assertEqual(time_in_english(112),"1 minute 52 seconds")
        self.assertEqual(time_in_english(10800),"3 hours")
        self.assertEqual(time_in_english(1501),"25 minutes 1 second")
        self.assertEqual(time_in_english(3960),"1 hour 6 minutes")
