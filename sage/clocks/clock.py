"""Sage base clock."""

import curses
import time

from .constants import PAUSE_MESSAGE
from .renderer import ClockRenderer


class Clock:
    """
    Base clock interface inherited by Timer and Stopwatch.
    """

    def __init__(self):
        self.count = 0
        self.paused = False
        self.pause_start = 0
        self.pause_time = 0

    def run(self, **kwargs):
        """
        Initialize curses and load the application.
        """
        curses.wrapper(lambda stdscr: self._run_with_curses(stdscr, **kwargs))

    def _run_with_curses(self, stdscr, **kwargs):
        """
        Run the application with curses initialized.
        """
        self.setup_components(stdscr)
        self.setup_display()
        self._run_clock(**kwargs)

    def setup_components(self, stdscr):
        """
        Set up clock component classes.
        """
        self.renderer = ClockRenderer(stdscr)

    def setup_display(self):
        """
        Initialize the sage display.
        """
        self.renderer.initialize_curses_window()
        self.renderer.render_app_title()
        self.renderer.render_help_text()
        self.renderer.render_counter()

    def _run_clock(self):
        """
        Run clock's core logic.
        """
        raise NotImplementedError("Subclasses must implement '_run_clock'.")

    def _get_elapsed_time(self, start_time) -> int:
        """
        Calculate the elapsed time depending on paused status.
        """
        if self.paused:
            return self.pause_start - start_time - self.pause_time
        else:
            return time.perf_counter() - start_time - self.pause_time

    def _on_pause(self):
        """
        Handle paused state changes.
        """
        if not self.paused:
            self.pause_start = time.perf_counter()
            self.paused = True
            self.renderer.render_status(PAUSE_MESSAGE)
        else:
            self.pause_time += time.perf_counter() - self.pause_start
            self.paused = False
            self.pause_start = 0
            self.renderer.clear_status()

    def _handle_keystrokes(self):
        """
        Handle keystroke logic for curses interface.
        """
        key = self.renderer.stdscr.getch()

        if key == ord(" "):
            self._on_pause()
            return

        if key == 10 or key == curses.KEY_ENTER:
            self.count += 1
            self.renderer.render_counter(self.count)
            return

        return key
