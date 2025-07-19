from functools import wraps


def validate_seconds(func):
    """
    Decorator to check that total seconds is between 1 and 86400
    seconds (24 hours).
    """
    @wraps(func)
    def wrapper(total_seconds, *args, **kwargs):
        if total_seconds <= 0 or total_seconds > 86400:
            raise ValueError("total seconds must be greater than 0 and less than or equal to 86400.")
        return func(total_seconds, *args, **kwargs)
    return wrapper
