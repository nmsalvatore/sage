import curses
import math
import time

import click

from .clock import Clock
from ..common import convert, format
from ..config import audio, presets


class Timer(Clock):
    """
    Timer interface.
    """

    TIMES_UP_SOUND_FILENAME = "timesup.mp3"
    TIMES_UP_TEXT = "Time's up!"

    def __init__(self):
        super().__init__()
        self.times_up = False

    def run(self, **kwargs):
        """
        Convenience method to initialize curses interface.
        """
        curses.wrapper(lambda stdscr: self.load(stdscr, **kwargs))

    def load(
        self, stdscr, no_start=False, hours=0, minutes=0, seconds=0, time_string=None
    ):
        """
        Load the timer.
        """
        start_time = time.perf_counter()
        total_seconds = self.get_duration(hours, minutes, seconds, time_string)
        heading_text = self._get_timer_heading_text(time_string, total_seconds)

        self._init_clock_config(stdscr)
        self._render_clock_heading(stdscr, heading_text)
        self._render_clock(stdscr, format.time_as_clock(total_seconds))
        self._handle_no_start(stdscr, no_start)

        try:
            audio.check_sound_path(self.TIMES_UP_SOUND_FILENAME)
        except Exception as e:
            self._render_warning(stdscr, f"Warning: {e}")

        while True:
            if self._handle_keystrokes(stdscr) == ord("q"):
                break

            elapsed = self._get_elapsed_time(start_time)
            time_remaining = total_seconds - elapsed
            display_seconds = math.ceil(time_remaining)
            display_time = format.time_as_clock(display_seconds)
            self._render_clock(stdscr, display_time)

            if time_remaining <= 0:
                self.times_up = True
                break

            time.sleep(self.REFRESH_RATE_IN_SECONDS)
            stdscr.refresh()

        self._handle_timer_completion(stdscr)

    def get_duration(self, hours=0, minutes=0, seconds=0, time_string="") -> int:
        """
        Determine the timer duration.
        """
        if saved_timer := presets.get_one(time_string):
            hours = saved_timer.get("hours", 0)
            minutes = saved_timer.get("minutes", 0)
            seconds = saved_timer.get("seconds", 0)
            return convert.time_units_to_seconds(hours, minutes, seconds)

        if time_string:
            return convert.time_string_to_seconds(time_string)

        return convert.time_units_to_seconds(hours, minutes, seconds)

    def print_duration(self, **duration_params):
        """
        Print the timer duration without loading the timer.
        """
        time_in_seconds = self.get_duration(**duration_params)
        click.echo(format.time_as_clock(time_in_seconds))

    def _get_timer_heading_text(self, time_string, total_seconds):
        """
        Determine the proper heading text for the timer.
        """
        if time_string and presets.get_one(time_string) is not None:
            return time_string
        return format.time_in_english(total_seconds)

    def _handle_timer_completion(self, stdscr):
        """
        Handle logic for timer completion.
        """
        if self.times_up:
            audio.play_sound(self.TIMES_UP_SOUND_FILENAME)
            self._render_status_text(stdscr, self.TIMES_UP_TEXT)
            stdscr.nodelay(0)
            stdscr.getch()
