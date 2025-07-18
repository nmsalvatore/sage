import curses
import time

from .clock import Clock
from ..common import format


class Stopwatch(Clock):
    """
    Stopwatch interface.
    """

    def run(self, **kwargs):
        """
        Convenience method to initialize curses interface.
        """
        curses.wrapper(lambda stdscr: self.load(stdscr, **kwargs))

    def load(self, stdscr, no_start=False):
        """
        Load the stopwatch.
        """
        start_time = time.perf_counter()
        self._init_clock_config(stdscr)
        self._handle_no_start(stdscr, no_start)

        while True:
            if self._handle_keystrokes(stdscr) == ord("q"):
                break

            time_elapsed = self._get_elapsed_time(start_time)
            ftime_elapsed = format.time_as_clock(
                time_elapsed, include_centiseconds=True
            )

            self._render_clock(stdscr, ftime_elapsed)
            time.sleep(self.REFRESH_RATE_IN_SECONDS)
            stdscr.refresh()
