import curses
import time
from typing import Tuple


class Clock:
    """
    Base clock interface.
    """

    HELP_TEXT = "<q> Quit, <Space> Pause/Resume, <Enter> Increment counter"
    PAUSE_MESSAGE = "Paused"
    REFRESH_RATE_IN_SECONDS = 0.01

    def __init__(self):
        self.counter = 0
        self.paused = False
        self.pause_start = 0
        self.pause_time = 0

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
        self._render_help_text(stdscr, self.HELP_TEXT)
        self._render_counter(stdscr)

    def _get_elapsed_time(self, start_time) -> int:
        """
        Calculate the elapsed time depending on paused status.
        """
        if self.paused:
            return self.pause_start - start_time - self.pause_time
        else:
            return time.perf_counter() - start_time - self.pause_time

    def _handle_paused_on_start(self, stdscr, paused):
        """
        Handle logic for --no-start flag.
        """
        if paused:
            self._toggle_pause(stdscr)
            self._clear_status_text(stdscr)
            self._render_status_text(stdscr, self.PAUSE_MESSAGE)

    def _handle_keystrokes(self, stdscr):
        """
        Handle keystroke logic for curses interface.
        """
        key = stdscr.getch()

        if key == ord(" "):
            self._toggle_pause(stdscr)
            return

        if key == 10 or key == curses.KEY_ENTER:
            self.counter += 1
            self._render_counter(stdscr)
            return

        return key

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

    def _render_clock(self, stdscr, formatted_time: str) -> None:
        """
        Render the clock at window center.
        """
        y, x = self._get_clock_coordinates(formatted_time)
        stdscr.addstr(y, x, formatted_time, curses.color_pair(1))

    def _render_help_text(self, stdscr, help_text: str = HELP_TEXT, color_id: int = 3) -> None:
        """
        Render the help text at the bottom left of window.
        """
        stdscr.addstr(curses.LINES - 1, 1, help_text, curses.color_pair(color_id))

    def _render_status_text(self, stdscr, status_text: str) -> None:
        """
        Render the status text below the clock.
        """
        y, x = self._get_status_coordinates(status_text)
        stdscr.addstr(y, x, status_text, curses.color_pair(4))

    def _render_application_title(self, stdscr, title_text: str = "sage") -> None:
        """
        Render title text at the top left of window.
        """
        stdscr.addstr(1, 1, title_text, curses.color_pair(2))

    def _clear_status_text(self, stdscr) -> None:
        """
        Clear the status text.
        """
        y, x = self._get_status_coordinates()
        stdscr.move(y, x)
        stdscr.clrtoeol()

    def _render_clock_heading(self, stdscr, timer_name: str) -> None:
        """
        Render the timer name in the curses interface.
        """
        y, x = self._get_title_coordinates(timer_name)
        stdscr.addstr(y, x, timer_name, curses.color_pair(2))

    def _render_counter(self, stdscr, counter_text: str = "Counter: 1") -> None:
        """
        Render the lap count at the bottom right of screen.
        """
        counter_text = f"Counter: {self.counter}"
        y = curses.LINES - 1
        x = curses.COLS - len(counter_text) - 1
        stdscr.addstr(y, x, counter_text, curses.color_pair(3))

    def _render_warning(self, stdscr, message: str) -> None:
        """
        Render warning text in upper right corner of screen.
        """
        x = curses.COLS - len(message) - 1
        stdscr.addstr(1, x, message, curses.color_pair(4))
