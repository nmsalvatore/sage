"""Sage stopwatch implementation."""

import time

from .clock import Clock
from .constants import REFRESH_RATE_IN_SECONDS
from sage.common.formatting import time_as_clock


class Stopwatch(Clock):
    """
    Stopwatch interface.
    """

    def _run_clock(self, **kwargs):
        """
        Core stopwatch logic.
        """
        start_time = time.perf_counter()

        if kwargs.get("paused"):
            self._on_pause()

        while self._handle_keystrokes() != ord("q"):
            # TODO: listen for window resize and clear the screen if true.

            time_elapsed = self._get_elapsed_time(start_time)
            ftime_elapsed = time_as_clock(time_elapsed, include_centiseconds=True)
            self.renderer.render_clock(ftime_elapsed)

            time.sleep(REFRESH_RATE_IN_SECONDS)
            self.renderer.stdscr.refresh()
