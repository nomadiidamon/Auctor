import io
import re
import time

import pytest

from Auctor.Stylus.Spinner import DEFAULT_FRAMES, Spinner, format_elapsed


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def wait_for(predicate, timeout=2.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.002)
    return False


def make(stream=None, **kwargs):
    stream = stream if stream is not None else io.StringIO()
    kwargs.setdefault("interval", 0.005)
    return Spinner(stream=stream, **kwargs), stream


def run_briefly(spinner, stream):
    spinner.start()
    assert wait_for(lambda: "\r" in stream.getvalue())


# -- construction ------------------------------------------------------


def test_default_frames_are_the_nine_frame_sweep():
    assert len(DEFAULT_FRAMES) == 9
    assert Spinner().frames == DEFAULT_FRAMES


@pytest.mark.parametrize("bad", [0, -1])
def test_interval_must_be_positive(bad):
    with pytest.raises(ValueError):
        Spinner(interval=bad)


@pytest.mark.parametrize("bad", [[], "abc", [1, 2]])
def test_invalid_frames_rejected(bad):
    with pytest.raises(ValueError):
        Spinner(frames=bad)


def test_not_running_before_start():
    spinner, stream = make()
    assert not spinner.is_running()
    assert stream.getvalue() == ""


# -- lifecycle ---------------------------------------------------------


def test_start_and_stop():
    spinner, stream = make(message="working")
    spinner.start()
    assert spinner.is_running()
    assert wait_for(lambda: "working" in stream.getvalue())
    spinner.stop()
    assert not spinner.is_running()


def test_start_while_running_is_safe():
    spinner, stream = make()
    spinner.start()
    thread = spinner._thread
    spinner.start()
    assert spinner._thread is thread
    spinner.stop()


def test_stop_when_not_running_writes_nothing():
    spinner, stream = make(stop_frame="[done]", final_message="bye")
    spinner.stop()
    assert stream.getvalue() == ""


def test_stop_clears_the_line():
    spinner, stream = make(message="working")
    run_briefly(spinner, stream)
    spinner.stop()
    assert re.search(r"\r {7,}\r$", stream.getvalue())


def test_stop_waits_for_the_thread():
    spinner, stream = make()
    run_briefly(spinner, stream)
    thread = spinner._thread
    spinner.stop()
    assert not thread.is_alive()


def test_no_output_after_stop():
    spinner, stream = make()
    run_briefly(spinner, stream)
    spinner.stop()
    snapshot = stream.getvalue()
    time.sleep(0.03)
    assert stream.getvalue() == snapshot


def test_restart_keeps_configuration():
    spinner, stream = make(message="again", frames=["a", "b"])
    spinner.start()
    spinner.stop()
    stream.truncate(0)
    stream.seek(0)
    spinner.start()
    assert wait_for(lambda: "again" in stream.getvalue())
    spinner.stop()
    assert spinner.frames == ("a", "b")


def test_color_wraps_frames():
    spinner, stream = make(color="<c>", endc="</c>", frames=["x"])
    run_briefly(spinner, stream)
    spinner.stop()
    assert "<c>x</c>" in stream.getvalue()


def test_default_stream_is_resolved_at_write_time(capsys):
    spinner = Spinner(interval=0.005, frames=["x"])
    spinner.start()
    time.sleep(0.05)
    spinner.stop()
    assert "x" in capsys.readouterr().out


# -- context manager ---------------------------------------------------


def test_context_manager_starts_and_stops():
    spinner, stream = make()
    with spinner as entered:
        assert entered is spinner
        assert spinner.is_running()
    assert not spinner.is_running()


def test_context_manager_stops_on_exception_and_propagates():
    spinner, stream = make(final_message="failed")
    with pytest.raises(RuntimeError):
        with spinner:
            raise RuntimeError("boom")
    assert not spinner.is_running()
    assert "failed\n" in stream.getvalue()


# -- update ------------------------------------------------------------


def test_update_changes_message():
    spinner, stream = make(message="one")
    spinner.start()
    spinner.update("two")
    assert wait_for(lambda: "two" in stream.getvalue())
    spinner.stop()
    assert spinner.message == "two"


def test_shorter_message_is_padded_over_the_old_one():
    spinner, stream = make(message="long message", frames=["x"])
    spinner.start()
    assert wait_for(lambda: "long message" in stream.getvalue())
    spinner.update("s")
    assert wait_for(lambda: "\rx s" + " " * 10 in stream.getvalue())
    spinner.stop()


# -- frames ------------------------------------------------------------


def test_frames_from_constructor():
    spinner, stream = make(frames=["<1>", "<2>"])
    run_briefly(spinner, stream)
    spinner.stop()
    assert "<1>" in stream.getvalue()


def test_frames_changed_before_start():
    spinner, stream = make()
    spinner.frames = ["A", "B"]
    run_briefly(spinner, stream)
    spinner.stop()
    assert "A" in stream.getvalue()
    assert DEFAULT_FRAMES[0] not in stream.getvalue()


def test_frames_changed_while_running_apply_on_next_tick():
    spinner, stream = make(frames=["old"])
    spinner.start()
    assert wait_for(lambda: "old" in stream.getvalue())
    spinner.frames = ["new"]
    assert wait_for(lambda: "new" in stream.getvalue())
    spinner.stop()


def test_setting_invalid_frames_keeps_existing():
    spinner, _ = make(frames=["ok"])
    with pytest.raises(ValueError):
        spinner.frames = []
    assert spinner.frames == ("ok",)


# -- stop frame and final message -------------------------------------


def test_no_stop_frame_leaves_only_cleared_line():
    spinner, stream = make(frames=["x"])
    run_briefly(spinner, stream)
    spinner.stop()
    assert not stream.getvalue().endswith("\n")


def test_stop_frame_from_constructor():
    spinner, stream = make(stop_frame="[done]")
    run_briefly(spinner, stream)
    spinner.stop()
    assert stream.getvalue().endswith("[done]\n")


def test_stop_frame_set_before_stop():
    spinner, stream = make()
    run_briefly(spinner, stream)
    spinner.stop_frame = "[ok]"
    spinner.stop()
    assert stream.getvalue().endswith("[ok]\n")


def test_stop_frame_written_once_across_double_stop():
    spinner, stream = make(stop_frame="[done]")
    run_briefly(spinner, stream)
    spinner.stop()
    spinner.stop()
    assert stream.getvalue().count("[done]") == 1


def test_stop_frame_is_colored():
    spinner, stream = make(stop_frame="[done]", color="<c>", endc="</c>")
    run_briefly(spinner, stream)
    spinner.stop()
    assert stream.getvalue().endswith("<c>[done]</c>\n")


def test_final_message_alone():
    spinner, stream = make(final_message="finished")
    run_briefly(spinner, stream)
    spinner.stop()
    assert stream.getvalue().endswith("finished\n")


def test_final_message_follows_stop_frame():
    spinner, stream = make(stop_frame="[done]", final_message="finished")
    run_briefly(spinner, stream)
    spinner.stop()
    assert stream.getvalue().endswith("[done] finished\n")


def test_stop_argument_overrides_configured_message_for_one_call():
    spinner, stream = make(final_message="default")
    run_briefly(spinner, stream)
    spinner.stop("override")
    assert stream.getvalue().endswith("override\n")
    stream.truncate(0)
    stream.seek(0)
    run_briefly(spinner, stream)
    spinner.stop()
    assert stream.getvalue().endswith("default\n")


def test_final_message_not_replayed_when_not_running():
    spinner, stream = make(final_message="finished")
    run_briefly(spinner, stream)
    spinner.stop()
    spinner.stop("again")
    assert stream.getvalue().count("finished") == 1
    assert "again" not in stream.getvalue()


def test_final_message_may_contain_other_braces():
    spinner, stream = make(final_message="{x} {0} {elapsed}")
    run_briefly(spinner, stream)
    spinner.stop()
    assert "{x} {0} " in stream.getvalue()


@pytest.mark.parametrize("value", [1, ["a"]])
def test_invalid_stop_frame_and_message_rejected(value):
    with pytest.raises(ValueError):
        Spinner(stop_frame=value)
    with pytest.raises(ValueError):
        Spinner(final_message=value)


# -- timer -------------------------------------------------------------


def test_elapsed_is_zero_before_start():
    assert Spinner().elapsed == 0.0


def test_elapsed_tracks_clock_while_running_and_freezes_after_stop():
    clock = FakeClock()
    spinner, stream = make(clock=clock)
    spinner.start()
    clock.now += 2.5
    assert spinner.elapsed == pytest.approx(2.5)
    clock.now += 1.0
    spinner.stop()
    clock.now += 50.0
    assert spinner.elapsed == pytest.approx(3.5)


def test_restart_resets_the_timer():
    clock = FakeClock()
    spinner, stream = make(clock=clock)
    spinner.start()
    clock.now += 5
    spinner.stop()
    assert spinner.elapsed == pytest.approx(5)
    spinner.start()
    assert spinner.elapsed == pytest.approx(0)
    spinner.stop()


def test_elapsed_placeholder_in_final_message():
    clock = FakeClock()
    spinner, stream = make(clock=clock, stop_frame="[done]", final_message="Done in {elapsed}")
    spinner.start()
    clock.now += 12.34
    spinner.stop()
    assert stream.getvalue().endswith("[done] Done in 12.3s\n")


def test_update_does_not_affect_the_timer():
    clock = FakeClock()
    spinner, _ = make(clock=clock)
    spinner.start()
    clock.now += 1
    spinner.update("later")
    clock.now += 1
    assert spinner.elapsed == pytest.approx(2)
    spinner.stop()


@pytest.mark.parametrize(
    "seconds,expected",
    [(0, "0.0s"), (0.84, "0.8s"), (12.3, "12.3s"), (59.9, "59.9s"), (60, "1m 00s"), (65, "1m 05s"), (3725, "62m 05s")],
)
def test_format_elapsed(seconds, expected):
    assert format_elapsed(seconds) == expected


def test_closed_stream_does_not_raise():
    spinner, stream = make()
    spinner.start()
    stream.close()
    spinner.stop()
    assert not spinner.is_running()
