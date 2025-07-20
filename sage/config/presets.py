import json
from pathlib import Path
from typing import TypeAlias

import click
from platformdirs import user_config_dir

from sage.common.conversions import time_string_to_time_units


PresetDict: TypeAlias = dict[str, int]
PresetsDict: TypeAlias = dict[str, PresetDict]


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


def create_defaults() -> PresetsDict:
    """
    Create and return default presets.
    """
    return {
        "pika": {"seconds": 5},
        "johncage": {"minutes": 4, "seconds": 33},
        "pomodoro": {"minutes": 25},
        "potato": {"minutes": 50},
        "rest": {"minutes": 10},
    }


def load_all() -> PresetsDict:
    """
    Load and return presets, creating defaults if the file doesn't exist.
    """
    presets_file = get_json_file()

    if not presets_file.exists():
        default_presets = create_defaults()
        save_all(default_presets)
        return default_presets

    try:
        with open(presets_file, "r") as f:
            return json.load(f)

    except Exception:
        return create_defaults()


def save_all(presets: PresetsDict) -> None:
    """
    Save presets to JSON file.
    """
    presets_file = get_json_file()

    try:
        with open(presets_file, "w") as f:
            json.dump(presets, f, indent=2)

    except Exception as e:
        raise click.ClickException(f"Could not save presets: {e}")


def get(name: str) -> PresetDict | None:
    """
    Get a specific preset by name.
    """
    presets = load_all()
    return presets.get(name)


def create(name: str, time_string: str) -> None:
    """
    Create a preset and save it.
    """
    if get(name):
        raise ValueError(f"'{name}' is already a saved preset.")

    hours, minutes, seconds = time_string_to_time_units(time_string)
    presets = load_all()
    presets[name] = {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

    save_all(presets)


def delete(name: str) -> None:
    """
    Delete a preset.
    """
    if get(name) is None:
        raise ValueError(f"'{name}' is not a saved preset.")

    presets = load_all()
    del presets[name]
    save_all(presets)


def rename(name: str, new_name: str) -> None:
    """
    Rename a preset.
    """
    if get(name) is None:
        raise ValueError(f"'{name}' is not a saved preset.")

    presets = load_all()
    presets.update({new_name: presets.pop(name)})
    save_all(presets)
