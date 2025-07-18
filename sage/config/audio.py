from pathlib import Path

from nava import play
from nava.errors import NavaBaseError
from nava.params import SOUND_FILE_EXIST_ERROR


def get_sound_file(filename: str) -> Path:
    """
    Retrieve path to the given sound file.
    """
    project_root = Path(__file__).parent.parent.parent
    return Path(project_root, "sounds", filename).resolve()


def check_sound_path(filename: str):
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
        play(str(sound_path), async_mode=True)

    except NavaBaseError:
        # by this point, the user should have already been alerted if
        # the sound file doesn't exist, so fail silently.
        pass
