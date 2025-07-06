import curses
import time

from .common import format_time_as_clock, get_curses_center_positions, set_curses_colors

class Stopwatch:
    def load(self, stdscr):
        """
        Load curses interface for stopwatch.
        """
        set_curses_colors()

        stdscr.clear()
        curses.curs_set(0)
        stdscr.nodelay(1)

        start_time = time.perf_counter()

        while True:
            key = stdscr.getch()
            if key == ord("q"):
                break

            time_elapsed = time.perf_counter() - start_time
            ftime_elapsed = format_time_as_clock(time_elapsed)
            y, x = get_curses_center_positions(ftime_elapsed)
            stdscr.addstr(y, x, ftime_elapsed, curses.color_pair(2))
