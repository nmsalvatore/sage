from unittest import TestCase

from sage.common.conversions import (
    seconds_to_time_units,
    time_units_to_seconds,
    time_string_to_seconds
)


class TimeConversionTests(TestCase):
    """
    Test suite for time conversions.
    """

    def test_single_time_units_to_seconds(self):
        """
        Test conversion of single time units to seconds.
        """
        self.assertEqual(time_units_to_seconds(hours=1), 3600)
        self.assertEqual(time_units_to_seconds(minutes=19), 1140)
        self.assertEqual(time_units_to_seconds(seconds=45), 45)

    def test_multiple_time_units_to_seconds(self):
        """
        Test conversion of multiple time units to seconds.
        """
        self.assertEqual(time_units_to_seconds(hours=1, minutes=30), 5400)
        self.assertEqual(time_units_to_seconds(hours=3, seconds=32), 10832)
        self.assertEqual(time_units_to_seconds(minutes=18, seconds=56), 1136)
        self.assertEqual(time_units_to_seconds(hours=3, minutes=46, seconds=7), 13567)

    def test_seconds_to_time_units(self):
        """
        Test conversion of seconds to time units.
        """
        self.assertEqual(seconds_to_time_units(65), (0, 1, 5))
        self.assertEqual(seconds_to_time_units(3657), (1, 0, 57))
        self.assertEqual(seconds_to_time_units(28933), (8, 2, 13))

    def test_convert_time_string_to_seconds(self):
        """
        Test conversion of time string to seconds.
        """
        self.assertEqual(time_string_to_seconds("2 minutes"), 120)
        self.assertEqual(time_string_to_seconds("3min40s"), 220)
        self.assertEqual(time_string_to_seconds("17 hours 3 minutes 40 sec"), 61420)

    def test_time_string_error_conditions(self):
        """
        Test error conditions of time string conversion.
        """
        with self.assertRaises(ValueError):
            time_string_to_seconds("nonsense")
        with self.assertRaises(ValueError):
            time_string_to_seconds("0s")
        with self.assertRaises(ValueError):
            time_string_to_seconds("")
        with self.assertRaises(ValueError):
            time_string_to_seconds("25hrs")
