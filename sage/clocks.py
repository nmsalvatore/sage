import curses
import time
from pathlib import Path
from typing import Tuple

import click
import nava

from .common import (
    convert_time_string_to_seconds,
    convert_time_to_seconds,
    format_time_as_clock,
)
from .config import get_saved_timer


class Clock:
    """
    Base clock interface.
    """
    START_MESSAGE = "Press SPACE to start"
    PAUSE_MESSAGE = "Paused"

    def __init__(self):
        self.paused = False
        self.pause_start = 0
        self.pause_time = 0

    def _get_elapsed_time(self, start_time) -> int:
        """
        Calculate the elapsed time depending on paused status.
        """
        if self.paused:
            return self.pause_start - start_time - self.pause_time
        else:
            return time.perf_counter() - start_time - self.pause_time

    def _toggle_pause(self, stdscr):
        """
        Handle logic for pause toggling.
        """
        if not self.paused:
            self.pause_start = time.perf_counter()
            self.paused = True
            self._render_status_text(stdscr, self.PAUSE_MESSAGE)
        else:
            self.pause_time += time.perf_counter() - self.pause_start
            self.paused = False
            self.pause_start = 0
            self._clear_status_text(stdscr)

    @staticmethod
    def _setup_colors():
        """
        Initialize curses color pairs.
        """
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def _init_clock_config(self, stdscr):
        """
        Initial configurations for the curses interface.
        """
        stdscr.clear()
        curses.curs_set(0)
        stdscr.nodelay(1)
        self._setup_colors()
        self._render_application_title(stdscr)

    @staticmethod
    def _get_center_y_start() -> int:
        """
        Calculate the starting y position of the window center.
        """
        return curses.LINES // 2

    @staticmethod
    def _get_center_x_start(text: str) -> int:
        """
        Calculate the starting x position for a centered text string.
        """
        x = (curses.COLS // 2) - (len(text) // 2)
        return x - 1 if len(text) % 2 else x

    def _get_clock_coordinates(self, text: str) -> Tuple[int, int]:
        """
        Calculate the clock coordinates, window center.
        """
        return (self._get_center_y_start(), self._get_center_x_start(text))

    def _get_status_coordinates(self, text: str = "") -> Tuple[int, int]:
        """
        Calculate the clock status coordinates, below the clock.
        """
        y, x = self._get_clock_coordinates(text)
        x = x if text else 0
        return (y + 1, x)

    def _get_title_coordinates(self, text: str = "") -> Tuple[int, int]:
        """
        Calculate the clock title coordinates, above the clock.
        """
        y, x = self._get_clock_coordinates(text)
        return (y - 1, x)

    def _render_clock(self, stdscr, formatted_time: str):
        """
        Render the clock at window center.
        """
        y, x = self._get_clock_coordinates(formatted_time)
        stdscr.addstr(y, x, formatted_time, curses.color_pair(1))

    def _render_help_text(self, stdscr, help_text: str, color_id: int = 3):
        """
        Render the help text at the bottom left of window.
        """
        stdscr.addstr(curses.LINES - 1, 1, help_text, curses.color_pair(color_id))

    def _render_status_text(self, stdscr, status_text: str):
        """
        Render the status text below the clock.
        """
        y, x = self._get_status_coordinates(status_text)
        stdscr.addstr(y, x, status_text, curses.color_pair(4))

    def _render_application_title(self, stdscr, title_text: str = "sage"):
        """
        Render title text at the top left of window.
        """
        stdscr.addstr(1, 1, title_text, curses.color_pair(2))

    def _clear_status_text(self, stdscr):
        """
        Clear the status text.
        """
        y, x = self._get_status_coordinates()
        stdscr.move(y, x)
        stdscr.clrtoeol()

    @staticmethod
    def _play_sound(filename: str):
        """
        Play a sound file located in the sounds/ directory of the
        project root.
        """
        sound_path = Path("sounds", filename).resolve()
        nava.play(str(sound_path), async_mode=True)


class Stopwatch(Clock):
    """
    Stopwatch interface.
    """
    HELP_TEXT = "<q> Quit, <Space> Pause/Resume, <Enter> Increment counter"

    def __init__(self):
        super().__init__()
        self.counter = 0

    def run(self, **kwargs):
        """
        Convenience method to initialize curses interface.
        """
        curses.wrapper(lambda stdscr: self.load(stdscr, **kwargs))

    def load(self, stdscr, no_start=False):
        """
        Load the stopwatch.
        """
        self._init_clock_config(stdscr)
        start_time = time.perf_counter()
        self._render_counter(stdscr)
        self._render_help_text(stdscr, self.HELP_TEXT)

        if no_start:
            self._toggle_pause(stdscr)
            self._clear_status_text(stdscr)
            self._render_status_text(stdscr, self.START_MESSAGE)

        while True:
            key = stdscr.getch()
            if key == ord("q"):
                break
            elif key == ord(" "):
                self._toggle_pause(stdscr)
            elif key == 10 or key == curses.KEY_ENTER:
                self.counter += 1
                self._render_counter(stdscr)

            time_elapsed = self._get_elapsed_time(start_time)
            ftime_elapsed = format_time_as_clock(
                time_elapsed, include_centiseconds=True
            )
            self._render_clock(stdscr, ftime_elapsed)

    def _render_counter(self, stdscr, counter_text: str = "Counter: 1"):
        """
        Render the lap count at the bottom right of screen.
        """
        counter_text = f"Counter: {self.counter}"
        y = curses.LINES - 1
        x = curses.COLS - len(counter_text) - 1
        stdscr.addstr(y, x, counter_text, curses.color_pair(3))


class Timer(Clock):
    """
    Timer interface.
    """
    HELP_TEXT = "<q> Quit, <Space> Pause/Resume"
    TIME_OFFSET = 0.9
    TIMES_UP_SOUND_FILENAME = "thyme.mp3"
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
        self._init_clock_config(stdscr)
        self._render_help_text(stdscr, self.HELP_TEXT)

        if time_string and get_saved_timer(time_string):
            self._render_timer_name(stdscr, time_string)

        start_time = time.perf_counter()
        total_seconds = self.get_duration(hours, minutes, seconds, time_string)
        self._render_clock(stdscr, format_time_as_clock(total_seconds))

        # since the timer reflects 0 seconds at the moment the seconds
        # remaining are less than 1 (roughly 0.9 seconds) and we want
        # the timer to go off right when the clock reflects 0 seconds,
        # we add 0.9 seconds to the total time.
        total_seconds += self.TIME_OFFSET

        if no_start:
            self._toggle_pause(stdscr)
            self._clear_status_text(stdscr)
            self._render_status_text(stdscr, self.START_MESSAGE)

        while True:
            key = stdscr.getch()

            if key == ord(" "):
                self._toggle_pause(stdscr)
            elif key == ord("q"):
                break

            elapsed = self._get_elapsed_time(start_time)
            time_remaining = total_seconds - elapsed
            ftime_remaining = format_time_as_clock(time_remaining)
            self._render_clock(stdscr, ftime_remaining)

            if time_remaining < 1:
                self.times_up = True
                break

            time.sleep(0.1)
            stdscr.refresh()

        if self.times_up:
            self._play_sound(self.TIMES_UP_SOUND_FILENAME)
            self._render_status_text(stdscr, self.TIMES_UP_TEXT)
            stdscr.nodelay(0)
            stdscr.getch()

    def get_duration(self, hours=0, minutes=0, seconds=0, time_string=None) -> int:
        """
        Determine the timer duration.
        """
        if saved_timer := get_saved_timer(time_string):
            hours = saved_timer.get("hours", 0)
            minutes = saved_timer.get("minutes", 0)
            seconds = saved_timer.get("seconds", 0)
            return convert_time_to_seconds(hours, minutes, seconds)

        if time_string:
            return convert_time_string_to_seconds(time_string)

        return convert_time_to_seconds(hours, minutes, seconds)

    def print_duration(self, **duration_params):
        """
        Print the timer duration without loading the timer.
        """

        time_in_seconds = self.get_duration(**duration_params)
        click.echo(format_time_as_clock(time_in_seconds))

    def _render_timer_name(self, stdscr, timer_name: str):
        """
        Render the timer name in the curses interface.
        """
        y, x = self._get_title_coordinates(timer_name)
        stdscr.addstr(y, x, timer_name, curses.color_pair(2))
