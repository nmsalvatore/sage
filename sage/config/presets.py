import json
from pathlib import Path
from typing import TypeAlias

import click
from platformdirs import user_config_dir

from sage.common.conversions import time_string_to_time_units


Timer: TypeAlias = dict[str, int]
Timers: TypeAlias = dict[str, Timer]


def get_json_file() -> Path:
    """
    Retrieve path to the JSON file storing timers.
    """
    try:
        config_dir = Path(user_config_dir("sage"))
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "timers.json"

    except OSError as e:
        click.echo(f"Warning: Could not access config directory ({e}). Using home directory.", err=True)
        return Path.home() / ".sage_timers.json"


def create_defaults() -> Timers:
    """
    Create and return default timers.
    """
    return {
        "pika": {"seconds": 5},
        "johncage": {"minutes": 4, "seconds": 33},
        "pomodoro": {"minutes": 25},
        "potato": {"minutes": 50},
        "rest": {"minutes": 10},
    }


def load_all() -> Timers:
    """
    Load and return timers, creating defaults if the file doesn't exist.
    """
    presets_file = get_json_file()

    if not presets_file.exists():
        default_timers = create_defaults()
        save_all(default_timers)
        return default_timers

    try:
        with open(presets_file, "r") as f:
            return json.load(f)

    except Exception:
        return create_defaults()


def save_all(timers: Timers) -> None:
    """
    Save timers to JSON file.
    """
    timers_file = get_json_file()

    try:
        with open(timers_file, "w") as f:
            json.dump(timers, f, indent=2)

    except Exception as e:
        raise click.ClickException(f"Could not save presets: {e}")


def get(name: str) -> Timer | None:
    """
    Get a specific timer by name.
    """
    timers = load_all()
    return timers.get(name)


def create(name: str, time_string: str) -> None:
    """
    Create a timer and save it.
    """
    if get(name):
        raise ValueError(f"'{name}' is already a saved preset.")

    hours, minutes, seconds = time_string_to_time_units(time_string)
    timers = load_all()
    timers[name] = {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

    save_all(timers)


def delete(name: str) -> None:
    """
    Delete a timer.
    """
    if get(name) is None:
        raise ValueError(f"'{name}' is not a saved preset.")

    timers = load_all()
    del timers[name]
    save_all(timers)


def rename(name: str, new_name: str) -> None:
    """
    Rename a timer.
    """
    if get(name) is None:
        raise ValueError(f"'{name}' is not a saved preset.")

    presets = load_all()
    presets.update({new_name: presets.pop(name)})
    save_all(presets)
