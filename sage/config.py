import json
from pathlib import Path

from platformdirs import user_config_dir


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
            "nap": {"minutes": 20}
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
    timers[name] = kwargs
    save_timers(timers)
