import curses
import time
from pathlib import Path
from typing import Tuple

import nava

from .common import format_time_as_clock
from .config import get_saved_timer
from .timer import get_timer_duration


class Clock:
    """
    Base clock interface.
    """
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
        self._setup_colors()
        stdscr.clear()
        curses.curs_set(0)
        stdscr.nodelay(1)

    @staticmethod
    def _get_center_y_start() -> int:
        return curses.LINES // 2

    @staticmethod
    def _get_center_x_start(text: str) -> int:
        x = (curses.COLS // 2) - (len(text) // 2)
        return x - 1 if len(text) % 2 else x

    def _get_clock_positions(self, text: str) -> Tuple[int, int]:
        return (
            self._get_center_y_start(),
            self._get_center_x_start(text)
        )

    def _get_status_positions(self, text: str = "") -> Tuple[int, int]:
        y, x = self._get_clock_positions(text)
        x = x if text else 0
        return (y + 1, x)

    def _get_title_positions(self, text: str = "") -> Tuple[int, int]:
        y, x = self._get_clock_positions(text)
        return (y - 1, x)

    def _render_clock(self, stdscr, formatted_time: str):
        y, x = self._get_clock_positions(formatted_time)
        stdscr.addstr(y, x, formatted_time, curses.color_pair(1))

    def _render_help_text(self, stdscr, help_text: str):
        stdscr.addstr(curses.LINES - 1, 1, help_text, curses.color_pair(3))

    def _render_status(self, stdscr, status_text: str):
        y, x = self._get_status_positions(status_text)
        stdscr.addstr(y, x, status_text, curses.color_pair(4))

    def _clear_status(self, stdscr):
        y, x = self._get_status_positions()
        stdscr.move(y, x)
        stdscr.clrtoeol()

    @staticmethod
    def _play_sound(filename: str):
        sound_path = Path("sounds", filename)
        nava.play(str(sound_path.resolve()), async_mode=True)


class Stopwatch(Clock):
    def load(self, stdscr):
        """
        Load clock interface for the stopwatch.
        """
        self._init_clock_config(stdscr)
        start_time = time.perf_counter()

        while True:
            key = stdscr.getch()
            if key == ord("q"):
                break

            time_elapsed = time.perf_counter() - start_time
            ftime_elapsed = format_time_as_clock(time_elapsed)
            y, x = self._get_clock_positions(ftime_elapsed)
            stdscr.addstr(y, x, ftime_elapsed, curses.color_pair(1))


class Timer(Clock):
    TIME_OFFSET = 0.9

    def __init__(self):
        self.pause_start = 0
        self.pause_time = 0
        self.paused = False
        self.times_up = False

    def _get_elapsed_time(self, start_time) -> int:
        if self.paused:
            return self.pause_start - start_time - self.pause_time
        else:
            return time.perf_counter() - start_time - self.pause_time

    def _handle_pause_toggle(self, stdscr):
        if not self.paused:
            self.pause_start = time.perf_counter()
            self.paused = True
            self._render_status(stdscr, "Paused")
        else:
            self.pause_time += time.perf_counter() - self.pause_start
            self.paused = False
            self.pause_start = 0
            self._clear_status(stdscr)

    def load(self, stdscr, hours=0, minutes=0, seconds=0, time_string=None):
        """
        Load the clock interface for the timer.
        """
        self._init_clock_config(stdscr)
        self._render_help_text(stdscr, "<q> Quit, <Space> Pause/Resume")

        if time_string and get_saved_timer(time_string):
            self._render_timer_name(stdscr, time_string)

        start_time = time.perf_counter()
        total_seconds = get_timer_duration(hours, minutes, seconds, time_string)
        self._render_clock(stdscr, format_time_as_clock(total_seconds))

        # since the timer reflects 0 seconds at the moment the seconds
        # remaining are less than 1 (roughly 0.9 seconds) and we want
        # the timer to go off right when the clock reflects 0 seconds,
        # we add 0.9 seconds to the total time.
        total_seconds += self.TIME_OFFSET

        while True:
            key = stdscr.getch()
            if key == ord(" "):
                self._handle_pause_toggle(stdscr)
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
            self._play_sound("thyme.mp3")
            self._render_status(stdscr, "Time's up!")
            stdscr.nodelay(0)
            stdscr.getch()

    def _render_timer_name(self, stdscr, timer_name: str):
        y, x = self._get_title_positions(timer_name)
        stdscr.addstr(y, x, timer_name, curses.color_pair(2))
