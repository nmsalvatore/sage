import json
from pathlib import Path
from typing import TypeAlias

import click
from platformdirs import user_config_dir

from ..common import convert


Preset: TypeAlias = dict[str, int]
Presets: TypeAlias = dict[str, Preset]


def get_json_file() -> Path:
    """
    Retrieve path to the JSON file storing presets.
    """
    try:
        config_dir = Path(user_config_dir("sage"))
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "presets.json"

    except OSError as e:
        click.echo(f"Warning: Could not access config directory ({e}). Using home directory.", err=True)
        return Path.home() / ".sage_presets.json"


def create_defaults() -> Presets:
    """
    Create default presets.
    """
    return {
        "pika": {"seconds": 5},
        "johncage": {"minutes": 4, "seconds": 33},
        "pomodoro": {"minutes": 25},
        "potato": {"minutes": 50},
        "rest": {"minutes": 10},
    }


def load_all() -> Presets:
    """
    Load and return presets, creating defaults if the file doesn't exist.
    """
    timers_file = get_json_file()

    if not timers_file.exists():
        default_timers = create_defaults()
        save_all(default_timers)
        return default_timers

    try:
        with open(timers_file, "r") as f:
            return json.load(f)

    except Exception:
        return create_defaults()


def save_all(presets: Presets) -> None:
    """
    Save presets to JSON file.
    """
    presets_file = get_json_file()

    try:
        with open(presets_file, "w") as f:
            json.dump(presets, f, indent=2)

    except Exception as e:
        raise click.ClickException(f"Could not save presets: {e}")


def get_one(preset_name: str) -> Preset | None:
    """
    Get a specific preset by name.
    """
    timers = load_all()
    return timers.get(preset_name)


def create_one(preset_name: str, **kwargs) -> None:
    """
    Create a new preset and save it.
    """
    presets = load_all()
    hours = kwargs.get("hours", 0)
    minutes = kwargs.get("minutes", 0)
    seconds = kwargs.get("seconds", 0)
    time_string = kwargs.get("time_string")

    if time_string:
        hours, minutes, seconds = convert.seconds_to_time_units(
            convert.time_string_to_seconds(time_string)
        )

    presets[preset_name] = {"hours": hours, "minutes": minutes, "seconds": seconds}
    save_all(presets)


def delete_one(preset_name: str) -> None:
    """
    Delete a preset.
    """
    timers = load_all()
    del timers[preset_name]
    save_all(timers)


def rename_one(preset_name: str, new_preset_name: str) -> None:
    """
    Rename a saved timer.
    """
    presets = load_all()
    presets.update({new_preset_name: presets.pop(preset_name)})
    save_all(presets)
