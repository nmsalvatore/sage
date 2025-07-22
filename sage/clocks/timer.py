"""Sage timer implementation."""

import math
import time

import click

from .clock import Clock
from .constants import (
    TIMES_UP_SOUND_FILENAME,
    TIMES_UP_TEXT,
)
from sage.common.conversions import get_duration
from sage.common.formatting import time_as_clock
from sage.config import sounds, presets


class Timer(Clock):
    """
    Timer interface.
    """

    def __init__(self):
        super().__init__()
        self.times_up = False

    def print_duration(self, time_input: str) -> None:
        """
        Print the timer duration without loading the timer.
        """
        time_in_seconds = get_duration(time_input)
        click.echo(time_as_clock(time_in_seconds))

    def _load_clock(self, **kwargs):
        """
        Core timer logic.
        """
        self._initialize_timer(**kwargs)
        self._setup_timer_display()
        self._handle_pause_on_start(**kwargs)
        self._start()

    def _initialize_timer(self, **kwargs):
        """
        Initialize timer settings.
        """
        self.time_input = kwargs.get("time_input", "")
        self.start_time = time.perf_counter()
        self.total_seconds = get_duration(self.time_input)

    def _setup_timer_display(self):
        """
        Initial paint of timer display.
        """
        if presets.get(self.time_input):
            self.renderer.render_heading(self.time_input)

        if not sounds.file_exists(TIMES_UP_SOUND_FILENAME):
            self.renderer.render_warning(
                "Warning: Cannot find sound file. "
                "Timer will complete silently."
            )

        initial_time = time_as_clock(self.total_seconds)
        self.renderer.render_clock(initial_time)

    def _start(self):
        """
        Start the timer.
        """
        while self._handle_keystrokes() != ord("q"):
            self._update_display()
            self._check_if_time_is_up()
            self._sleep_and_refresh()

    def _update_display(self):
        """
        Update the timer display.
        """
        display_time = self._get_display_time()
        self.renderer.render_clock(display_time)

    def _get_display_time(self):
        """
        Calculate the display time.
        """
        time_remaining = self._get_time_remaining()
        display_seconds = math.ceil(time_remaining)
        return time_as_clock(display_seconds)

    def _get_time_remaining(self):
        """
        Calculate time remaining.
        """
        elapsed = self._get_elapsed_time()
        return self.total_seconds - elapsed

    def _check_if_time_is_up(self):
        """
        Check if timer has completed.
        """
        time_remaining = self._get_time_remaining()
        if not self.times_up and time_remaining <= 0:
            self._complete_timer()

    def _complete_timer(self):
        """
        Handle logic for timer completion.
        """
        self.times_up = True
        self.renderer.render_status(TIMES_UP_TEXT)
        self.renderer.stdscr.nodelay(0)
        sounds.play_file(TIMES_UP_SOUND_FILENAME)
