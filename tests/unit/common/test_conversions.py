from sage.common.conversions import (
    seconds_to_time_units,
    time_units_to_seconds,
    time_string_to_seconds,
    time_string_to_time_units
)


def test_single_time_units_to_seconds():
    """
    Test conversion of single time units to seconds.
    """
    assert time_units_to_seconds(hours=1) == 3600
    assert time_units_to_seconds(minutes=19) == 1140
    assert time_units_to_seconds(seconds=45) == 45


def test_multiple_time_units_to_seconds():
    """
    Test conversion of multiple time units to seconds.
    """
    assert time_units_to_seconds(hours=1, minutes=30) == 5400
    assert time_units_to_seconds(minutes=18, seconds=56) == 1136
    assert time_units_to_seconds(hours=3, minutes=46, seconds=7) == 13567


def test_seconds_to_time_units():
    """
    Test conversion of seconds to time units.
    """
    assert seconds_to_time_units(65) == (0, 1, 5)
    assert seconds_to_time_units(3657) == (1, 0, 57)
    assert seconds_to_time_units(28933) == (8, 2, 13)


def test_convert_time_string_to_seconds():
    """
    Test conversion of time string to seconds.
    """
    assert time_string_to_seconds("2 minutes") == 120
    assert time_string_to_seconds("3min40s") == 220
    assert time_string_to_seconds("17 hours 3 minutes 40 sec") == 61420


def test_convert_time_string_to_time_units():
    """
    Test conversion of time string to hours, minutes, and seconds.
    """
    assert time_string_to_time_units("2 minutes") == (0, 2, 0)
    assert time_string_to_time_units("3min40s") == (0, 3, 40)
    assert time_string_to_time_units("17 hours 3 minutes 40 sec") == (17, 3, 40)
