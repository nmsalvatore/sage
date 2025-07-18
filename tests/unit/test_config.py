from unittest.mock import patch

from sage.config import presets


def test_load_presets_creates_defaults_on_first_run(tmp_path):
    """
    If no presets file exists, it should be created.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        all_presets = presets.load_all()
        assert "pomodoro" in all_presets
        assert all_presets["pomodoro"]["minutes"] == 25


def test_create_and_load_preset(tmp_path):
    """
    A created timer should show up in the list of presets.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        presets.create_one("workout", hours=1, minutes=30)
        all_presets = presets.load_all()
        assert "workout" in all_presets
        assert all_presets["workout"]["hours"] == 1
        assert all_presets["workout"]["minutes"] == 30


def test_get_known_preset_returns_time(tmp_path):
    """
    Retrieving a specific preset should return its correct time.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        presets.create_one("break", minutes=5)
        assert presets.get_one("break") == {"hours": 0, "minutes": 5, "seconds": 0}


def test_get_unknown_preset_returns_nothing(tmp_path):
    """
    Retrieving a nonexistent preset should return nothing.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        nothing = presets.get_one("nothing")
        assert nothing is None


def test_create_preset_overwrites_existing(tmp_path):
    """
    Creating a preset should overwrite an existing preset of the same name.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        presets.create_one("test", minutes=10)
        presets.create_one("test", minutes=20, seconds=30)
        assert presets.get_one("test") == {"hours": 0, "minutes": 20, "seconds": 30}


def test_create_preset_converts_time_string_to_time_units(tmp_path):
    """
    Creating a preset should convert a time string to the correct time
    units.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        presets.create_one("test", time_string="15 minutes")
        assert presets.get_one("test") == {"hours": 0, "minutes": 15, "seconds": 0}


def test_deleted_preset_removed_from_list(tmp_path):
    """
    A deleted preset should not show up in the list of presets.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        presets.create_one("test", time_string="15 minutes")
        assert presets.get_one("test") == {"hours": 0, "minutes": 15, "seconds": 0}

        presets.delete_one("test")
        assert presets.get_one("test") is None


def test_rename_preset_shows_new_name_in_list(tmp_path):
    """
    The new name of a renamed preset should show up in the list of
    presets and return the correct time.
    """
    presets_file = tmp_path / "presets.json"

    with patch("sage.config.presets.get_json_file", return_value=presets_file):
        presets.create_one("test", time_string="15 minutes")
        assert presets.get_one("test") == {"hours": 0, "minutes": 15, "seconds": 0}

        presets.rename_one("test", "beans")
        assert presets.get_one("beans") == {"hours": 0, "minutes": 15, "seconds": 0}
