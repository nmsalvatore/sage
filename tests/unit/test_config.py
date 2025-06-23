from unittest.mock import patch

from sage.config import load_saved_timers, save_timer, get_saved_timer


def test_load_saved_timers_creates_defaults_on_first_run(tmp_path):
    """
    When no timers file exists, `load_saved_timers` should return
    defaults.
    """
    fake_timers_file = tmp_path / "timers.json"

    with patch("sage.config.get_timers_file", return_value=fake_timers_file):
        timers = load_saved_timers()

        assert "pomodoro" in timers
        assert timers["pomodoro"]["minutes"] == 25


def test_save_and_load_timer(tmp_path):
    """
    Test saving a timer and loading it back.
    """
    fake_timers_file = tmp_path / "timers.json"

    with patch("sage.config.get_timers_file", return_value=fake_timers_file):
        save_timer("workout", hours=1, minutes=30)

        timers = load_saved_timers()
        assert "workout" in timers
        assert timers["workout"]["hours"] == 1
        assert timers["workout"]["minutes"] == 30
        assert "pomodoro" in timers


def test_get_saved_timer(tmp_path):
    """
    Test retrieving a specific saved timer.
    """
    fake_timers_file = tmp_path / "timers.json"

    with patch("sage.config.get_timers_file", return_value=fake_timers_file):
        save_timer("break", minutes=5)
        save_timer("meeting", minutes=15)

        break_timer = get_saved_timer("break")
        assert break_timer == {"minutes": 5}

        meeting_timer = get_saved_timer("meeting")
        assert meeting_timer == {"minutes": 15}

        nonexistent = get_saved_timer("doesntexist")
        assert nonexistent is None


def test_save_timer_overwrites_existing(tmp_path):
    """
    Test that saving a timer with existing name overwrites it.
    """
    fake_timers_file = tmp_path / "timers.json"

    with patch("sage.config.get_timers_file", return_value=fake_timers_file):
        save_timer("test", minutes=10)
        save_timer("test", minutes=20, seconds=30)

        timer = get_saved_timer("test")
        assert timer == {"minutes": 20, "seconds": 30}
