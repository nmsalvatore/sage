"""Sage constants."""

from enum import StrEnum


class DisplayText(StrEnum):
    TITLE = "sage"
    RUNNING_HELP = "<q> Quit, <Space> Pause/Resume, <Enter> Increment counter"
    MISSING_SOUND = "Cannot find sound file. Timer will complete silently."
    PAUSED = "Paused"
    TIMES_UP = "Time's up!"


class SoundFileName(StrEnum):
    TIMES_UP = "timesup.mp3"
