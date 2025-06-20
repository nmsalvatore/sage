def time_in_seconds(hours=0, minutes=0, seconds=0):
    """
    Converts hours, minutes, and seconds to total seconds.
    """
    return int(hours * 3600) + int(minutes * 60) + int(seconds)
