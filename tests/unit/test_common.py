from sage.common import convert, format


def test_convert_time_units_to_seconds():
    """
    Conversion function 'time_units_to_seconds' should convert hours,
    minutes, and seconds to total seconds.
    """
    assert convert.time_units_to_seconds(hours=1) == 3600
    assert convert.time_units_to_seconds(hours=1, minutes=30) == 5400
    assert convert.time_units_to_seconds(hours=2, seconds=5) == 7205
    assert convert.time_units_to_seconds(minutes=30, seconds=25) == 1825


def test_convert_seconds_to_time_units():
    """
    Conversion function 'seconds_to_time_units' should convert total
    seconds to hours, minutes, and seconds.
    """
    assert convert.seconds_to_time_units(65) == (0, 1, 5)
    assert convert.seconds_to_time_units(3657) == (1, 0, 57)
    assert convert.seconds_to_time_units(28933) == (8, 2, 13)


def test_convert_time_string_to_seconds():
    """
    Conversion function 'time_string_to_seconds' should take a
    human-readable time string and convert it to total seconds.
    """
    assert convert.time_string_to_seconds("2 minutes") == 120
    assert convert.time_string_to_seconds("3min40s") == 220


def test_format_time_as_clock():
    """
    Formatting function 'time_as_clock' should take a time in seconds,
    convert it to the correct time units (hours, minutes, seconds),
    and format it into 00:00:00 format.
    """
    assert format.time_as_clock(185) == "00:03:05"


def test_format_time_as_clock_with_centiseconds():
    """
    When centiseconds are specified, formatting function
    'time_as_clock' should take a time in seconds, convert it to the
    correct time units (hours, minutes, seconds, centiseconds), and
    format it into 00:00:00:00 format.
    """
    assert format.time_as_clock(133.23, include_centiseconds=True) == "00:02:13:23"


def test_format_time_in_english():
    """
    Formatting function 'time_in_english' should take a time in seconds,
    convert it to the correct time units (hours, minutes, seconds) and
    format it into English.
    """
    assert format.time_in_english(112) == "1 minute 52 seconds"
