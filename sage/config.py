import json
from pathlib import Path

import click
import nava
from nava.errors import NavaBaseError
from nava.params import SOUND_FILE_EXIST_ERROR
from platformdirs import user_config_dir

from .common import convert_time_string_to_seconds, expand_time_from_seconds


def get_timers_file():
    """
    Retrieve path to the JSON file storing custom timers.
    """
    try:
        config_dir = Path(user_config_dir("sage"))
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "timers.json"

    except OSError as e:
        click.echo(f"Warning: Could not access config directory ({e}). Using home directory.", err=True)
        return Path.home() / ".sage_timers.json"


def create_default_timers():
    """
    Create and return the default timer configuration.
    """
    return {
        "pika": {"seconds": 5},
        "johncage": {"minutes": 4, "seconds": 33},
        "pomodoro": {"minutes": 25},
        "potato": {"minutes": 50},
        "rest": {"minutes": 10},
    }


def load_saved_timers():
    """
    Load the saved timers, creating defaults if the file doesn't exist.
    """
    timers_file = get_timers_file()
    if not timers_file.exists():
        default_timers = create_default_timers()
        save_timers(default_timers)
        return default_timers

    try:
        with open(timers_file, "r") as f:
            return json.load(f)

    except Exception:
        return create_default_timers()


def save_timers(timers):
    """
    Save timers to JSON file.
    """
    timers_file = get_timers_file()

    try:
        with open(timers_file, "w") as f:
            json.dump(timers, f, indent=2)

    except Exception as e:
        raise click.ClickException(f"Could not save timers file: {e}")


def get_saved_timer(name):
    """
    Get a specific saved timer by name.
    """
    timers = load_saved_timers()
    return timers.get(name)


def save_timer(name, **kwargs):
    """
    Save a new timer.
    """
    timers = load_saved_timers()
    hours = kwargs.get("hours", 0)
    minutes = kwargs.get("minutes", 0)
    seconds = kwargs.get("seconds", 0)
    time_string = kwargs.get("time_string")

    if time_string:
        hours, minutes, seconds = expand_time_from_seconds(
            convert_time_string_to_seconds(time_string)
        )

    timers[name] = {"hours": hours, "minutes": minutes, "seconds": seconds}
    save_timers(timers)


def delete_timer(name):
    """
    Delete a saved timer.
    """
    timers = load_saved_timers()
    del timers[name]
    save_timers(timers)


def rename_timer(name, new_name):
    """
    Rename a saved timer.
    """
    timers = load_saved_timers()
    timers.update({new_name: timers.pop(name)})
    save_timers(timers)


def get_sound_file(filename: str) -> Path:
    """
    Retrieve path to the given sound file.
    """
    project_root = Path(__file__).parent.parent
    return Path(project_root, "sounds", filename).resolve()


def sound_path_check(filename: str):
    """
    Check that sound file exists, so that the user can be
    immediately alerted if no sound is going to be played with the
    timer completes.
    """
    sound_path = get_sound_file(filename)
    if not sound_path.exists():
        raise NavaBaseError(SOUND_FILE_EXIST_ERROR)


def play_sound(filename: str):
    """
    Play a sound file located in the sounds/ directory of the
    project root.
    """
    try:
        sound_path = get_sound_file(filename)
        nava.play(str(sound_path), async_mode=True)

    except NavaBaseError:
        # by this point, the user should have already been alerted if
        # the sound file doesn't exist, so fail silently.
        pass
