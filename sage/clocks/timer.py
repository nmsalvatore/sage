"""Sage timer implementation."""

import math
import time

import click

from .clock import Clock
from .constants import (
    MISSING_SOUND_MESSAGE,
    TIMES_UP_SOUND,
    TIMES_UP_MESSAGE,
)
from sage.common.conversions import time_string_to_seconds, time_units_to_seconds
from sage.common.formatting import time_as_clock
from sage.config import sounds, presets


class Timer(Clock):
    """
    Timer interface.
    """

    def __init__(self):
        super().__init__()
        self.times_up = False

    def print_duration(self, time_input) -> None:
        """
        Print the timer duration without loading the timer.
        """
        time_in_seconds = self._get_total_seconds(time_input)
        click.echo(time_as_clock(time_in_seconds))

    def _load_clock(self, **kwargs):
        """
        Initialize and start the timer.
        """
        self._initialize_timer(**kwargs)
        self._setup_timer_display()
        self._handle_pause_on_start(**kwargs)
        self._start()

    def _initialize_timer(self, **kwargs):
        """
        Initialize timer settings.
        """
        time_input = kwargs.get("time_input", "")
        self.time_input = time_input
        self.start_time = time.perf_counter()
        self.total_seconds = self._get_total_seconds(time_input)

    def _get_total_seconds(self, time_input):
        """
        Determine the timer duration in seconds based on whether the string
        represents a preset or not.
        """
        if preset := presets.get(time_input):
            seconds = time_units_to_seconds(**preset)
        else:
            seconds = time_string_to_seconds(time_input)

        self._validate_total_seconds(seconds)
        return seconds

    def _validate_total_seconds(self, total_seconds):
        """
        Validation check that total seconds is within the required
        range from 1 second to 24 hours.
        """
        if total_seconds <= 0:
            raise ValueError("Duration must be greater than 0 seconds.")
        if total_seconds > 86400:
            raise ValueError("Duration cannot exceed 24 hours.")

    def _setup_timer_display(self):
        """
        Initial setup of the timer display.
        """
        self._check_for_heading()
        self._check_for_sound_warning()
        self._update_display()

    def _check_for_heading(self):
        """
        Check if timer is a preset and render heading if so.
        """
        if presets.get(self.time_input):
            self.renderer.render_heading(self.time_input)

    def _check_for_sound_warning(self):
        """
        Check for missing sound file and render warning if so.
        """
        if not sounds.file_exists(TIMES_UP_SOUND):
            self.renderer.render_warning(MISSING_SOUND_MESSAGE)

    def _start(self):
        """
        Start the timer.
        """
        while self._listen_for_keys() != ord("q"):
            self._update_display()
            self._check_if_time_is_up()
            self._sleep_and_refresh()

    def _listen_for_keys(self):
        """
        Turn off pause and counter handling once timer has completed.
        """
        if self.times_up:
            key = self.renderer.stdscr.getch()
            return key if key == ord("q") else -1
        return super()._listen_for_keys()

    def _update_display(self):
        """
        Update the timer display, as long as timer hasn't completed.
        """
        if not self.times_up:
            display_time = self._get_display_time()
            self.renderer.render_clock(display_time)

    def _get_display_time(self):
        """
        Calculate and return the display time.
        """
        time_remaining = self._get_time_remaining()
        display_seconds = math.ceil(time_remaining)
        return time_as_clock(display_seconds)

    def _get_time_remaining(self):
        """
        Calculate and return time remaining.
        """
        elapsed = self._get_elapsed_time()
        return self.total_seconds - elapsed

    def _check_if_time_is_up(self):
        """
        Check if timer has completed and complete if so.
        """
        time_remaining = self._get_time_remaining()
        if not self.times_up and time_remaining <= 0:
            self._complete_timer()

    def _complete_timer(self):
        """
        Handle logic for timer completion.
        """
        self.times_up = True
        self.renderer.render_status(TIMES_UP_MESSAGE)
        self.renderer.stdscr.nodelay(0)
        sounds.play_file(TIMES_UP_SOUND)
