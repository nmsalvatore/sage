"""Sage timer implementation."""

import curses
import math
import time

import click

from .clock import Clock
from .constants import (
    REFRESH_RATE_IN_SECONDS,
    TIMES_UP_SOUND_FILENAME,
    TIMES_UP_TEXT,
)
from sage.common.conversions import get_duration
from sage.common.formatting import time_as_clock, time_in_english
from sage.config import sounds, presets


class Timer(Clock):
    """
    Timer interface.
    """

    def __init__(self):
        super().__init__()
        self.times_up = False

    def run(self, **kwargs):
        """
        Convenience method to initialize curses interface.
        """
        curses.wrapper(lambda stdscr: self.load(stdscr, **kwargs))

    def load(self, stdscr, time_string, paused):
        """
        Load the timer.
        """
        start_time = time.perf_counter()
        total_seconds = get_duration(time_string)
        heading_text = self._get_timer_heading_text(time_string, total_seconds)

        self._init_clock_config(stdscr)
        self._render_clock_heading(stdscr, heading_text)
        self._render_clock(stdscr, time_as_clock(total_seconds))
        self._handle_paused_on_start(stdscr, paused)

        if not sounds.file_exists(TIMES_UP_SOUND_FILENAME):
            self._render_warning(
                stdscr, "Warning: Cannot find sound file. Timer will complete silently."
            )

        while True:
            if self._handle_keystrokes(stdscr) == ord("q"):
                break

            elapsed = self._get_elapsed_time(start_time)
            time_remaining = total_seconds - elapsed
            display_seconds = math.ceil(time_remaining)
            display_time = time_as_clock(display_seconds)
            self._render_clock(stdscr, display_time)

            if time_remaining <= 0:
                self.times_up = True
                break

            time.sleep(REFRESH_RATE_IN_SECONDS)
            stdscr.refresh()

        self._handle_timer_completion(stdscr)

    def print_duration(self, time_string: str) -> None:
        """
        Print the timer duration without loading the timer.
        """
        time_in_seconds = get_duration(time_string)
        click.echo(time_as_clock(time_in_seconds))

    def _get_timer_heading_text(self, time_string: str, total_seconds: float):
        """
        Determine the proper heading text for the timer.
        """
        if time_string and presets.get(time_string) is not None:
            return time_string
        return time_in_english(total_seconds)

    def _handle_timer_completion(self, stdscr):
        """
        Handle logic for timer completion.
        """
        if self.times_up:
            sounds.play_file(TIMES_UP_SOUND_FILENAME)
            self._render_status_text(stdscr, TIMES_UP_TEXT)
            stdscr.nodelay(0)
            stdscr.getch()
