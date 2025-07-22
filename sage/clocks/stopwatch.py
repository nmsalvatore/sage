"""Sage stopwatch implementation."""

import time

from .clock import Clock
from sage.common.formatting import time_as_clock


class Stopwatch(Clock):
    """
    Stopwatch interface.
    """

    def _run_clock(self, **kwargs):
        """
        Core stopwatch logic.
        """
        self._initialize_stopwatch()

        if kwargs.get("paused"):
            self._on_pause()

        while self._handle_keystrokes() != ord("q"):
            # TODO: listen for window resize and clear the screen if true.
            self._update_display()
            self._sleep_and_refresh()

    def _initialize_stopwatch(self):
        """
        Initialize stopwatch settings.
        """
        self.start_time = time.perf_counter()

    def _update_display(self):
        """
        Update the stopwatch display.
        """
        display_time = self._get_display_time()
        self.renderer.render_clock(display_time)

    def _get_display_time(self):
        """
        Calculate the display time.
        """
        time_elapsed = self._get_elapsed_time(self.start_time)
        return time_as_clock(time_elapsed, include_centiseconds=True)
