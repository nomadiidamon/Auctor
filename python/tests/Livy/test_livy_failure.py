from datetime import datetime

from Auctor.Livy import Failure


def test_fields_and_defaults():
    f = Failure(level="ERROR", message="m", category=None, timestamp="t")
    assert f.exception is None
    assert (f.level, f.message, f.category, f.timestamp) == ("ERROR", "m", None, "t")


def test_to_dict():
    f = Failure("EXCEPTION", "m", "Cat", "t", "trace")
    assert f.to_dict() == {
        "level": "EXCEPTION",
        "message": "m",
        "category": "Cat",
        "timestamp": "t",
        "exception": "trace",
    }


def test_is_immutable():
    f = Failure("ERROR", "m", None, "t")
    try:
        f.message = "x"
    except AttributeError:
        return
    raise AssertionError("Failure should be frozen")


def test_timestamp_is_iso_when_recorded(tmp_path):
    from Auctor.Livy import Livy

    with Livy(path=tmp_path) as livy:
        livy.error("x")
        datetime.fromisoformat(livy.get_last_failure().timestamp)
