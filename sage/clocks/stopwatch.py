"""Sage stopwatch implementation."""

import curses
import time

from .clock import Clock
from .constants import REFRESH_RATE_IN_SECONDS
from sage.common.formatting import time_as_clock


class Stopwatch(Clock):
    """
    Stopwatch interface.
    """

    def run(self, **kwargs):
        """
        Convenience method to initialize curses interface.
        """
        curses.wrapper(lambda stdscr: self.load(stdscr, **kwargs))

    def load(self, stdscr, paused):
        """
        Load the stopwatch.
        """
        start_time = time.perf_counter()
        self._init_clock_config(stdscr)
        self._handle_paused_on_start(stdscr, paused)

        while True:
            if self._handle_keystrokes(stdscr) == ord("q"):
                break

            time_elapsed = self._get_elapsed_time(start_time)
            ftime_elapsed = time_as_clock(time_elapsed, include_centiseconds=True)

            self._render_clock(stdscr, ftime_elapsed)
            time.sleep(REFRESH_RATE_IN_SECONDS)
            stdscr.refresh()
