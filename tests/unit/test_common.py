from unittest import TestCase

from sage.common import (
    convert_time_string_to_seconds,
    convert_time_to_seconds,
    expand_time_from_seconds,
    format_time_as_clock,
    format_time_as_english,
)


class TestTimer(TestCase):
    """
    Testing suite for common functions.
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

    def test_convert_time_string_to_seconds(self):
        """
        Test utility function `convert_time_string_to_seconds` which
        takes a human-readable time string and converts it to total
        seconds.
        """
        self.assertEqual(convert_time_string_to_seconds("2 minutes"), 120)
        self.assertEqual(convert_time_string_to_seconds("3min40s"), 220)

    def test_convert_time_string_to_seconds_invalid_string(self):
        """
        Test that `convert_time_string_to_seconds` raises a ValueError
        if string is invalid.
        """
        with self.assertRaises(ValueError):
            convert_time_string_to_seconds("hello")

    def test_convert_time_string_to_seconds_invalid_type(self):
        """
        Test that `convert_time_string_to_seconds` raises a TypeError
        if the the argument is not a string.
        """
        with self.assertRaises(TypeError):
            convert_time_string_to_seconds(5)

    def test_format_time_as_clock(self):
        """
        Test that `format_time_as_clock` takes a time in seconds,
        converts it to the correct time units (hours, minutes, seconds)
        and formats it into 00:00:00 format.
        """
        self.assertEqual(format_time_as_clock(185), "00:03:05")

    def test_format_time_as_english(self):
        """
        Test that `format_time_as_english` takes a time in seconds,
        converts it to the correct time units (hours, minutes, seconds)
        and formats it into English.
        """
        self.assertEqual(format_time_as_english(112), "1 minute 52 seconds")
