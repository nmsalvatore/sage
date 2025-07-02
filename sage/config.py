import json
from pathlib import Path

from platformdirs import user_config_dir

from .common import convert_time_string_to_seconds, expand_time_from_seconds


def get_timers_file():
    """
    Retrieve path to the JSON file storing custom timers.
    """
    config_dir = Path(user_config_dir("sage"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "timers.json"


def load_saved_timers():
    """
    Load the saved timers, creating defaults if the file doesn't exist.
    """
    timers_file = get_timers_file()

    if not timers_file.exists():
        default_timers = {
            "pomodoro": {"minutes": 25},
            "potato": {"minutes": 50},
            "johncage": {"minutes": 4, "seconds": 33},
            "pika": {"seconds": 5}
        }
        save_timers(default_timers)
        return default_timers

    with open(timers_file, "r") as f:
        return json.load(f)


def save_timers(timers):
    """
    Save timers to JSON file.
    """
    timers_file = get_timers_file()
    with open(timers_file, "w") as f:
        json.dump(timers, f, indent=2)


def get_saved_timer(name):
    """Get a specific saved timer by name"""
    timers = load_saved_timers()
    return timers.get(name)


def save_timer(name, **kwargs):
    """Save a new timer"""
    timers = load_saved_timers()

    hours = kwargs.get("hours", 0)
    minutes = kwargs.get("minutes", 0)
    seconds = kwargs.get("seconds", 0)
    time_string = kwargs.get("time_string")

    if time_string:
        hours, minutes, seconds = expand_time_from_seconds(
            convert_time_string_to_seconds(time_string)
        )

    timers[name] = {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

    save_timers(timers)
