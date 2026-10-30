import io

import pytest

from Auctor.Stylus.Prompt import Prompt


def make(answers="", **kwargs):
    out = io.StringIO()
    return Prompt(stream=out, input_stream=io.StringIO(answers), **kwargs), out


# -- ask ---------------------------------------------------------------


def test_ask_returns_the_answer():
    prompt, out = make("Ada\n")
    assert prompt.ask("Name") == "Ada"
    assert out.getvalue() == "Name: "


def test_ask_strips_whitespace_and_line_endings():
    prompt, _ = make("  Ada  \r\n")
    assert prompt.ask("Name") == "Ada"


def test_ask_empty_answer_without_default_is_empty_string():
    prompt, _ = make("\n")
    assert prompt.ask("Name") == ""


def test_ask_empty_answer_returns_default_and_shows_it():
    prompt, out = make("\n")
    assert prompt.ask("Name", default="Ada") == "Ada"
    assert out.getvalue() == "Name [Ada]: "


def test_ask_answer_overrides_default():
    prompt, _ = make("Grace\n")
    assert prompt.ask("Name", default="Ada") == "Grace"


def test_ask_cancel_on_end_of_input_returns_none():
    prompt, out = make("")
    assert prompt.ask("Name", default="Ada") is None
    assert out.getvalue().endswith("\n")


# -- confirm -----------------------------------------------------------


@pytest.mark.parametrize("answer", ["y", "Y", "yes", "YES", " Yes "])
def test_confirm_yes(answer):
    prompt, _ = make(answer + "\n")
    assert prompt.confirm("Go?") is True


@pytest.mark.parametrize("answer", ["n", "N", "no", "NO"])
def test_confirm_no(answer):
    prompt, _ = make(answer + "\n")
    assert prompt.confirm("Go?", default=True) is False


@pytest.mark.parametrize("default", [True, False])
def test_confirm_empty_answer_returns_default(default):
    prompt, _ = make("\n")
    assert prompt.confirm("Go?", default=default) is default


def test_confirm_hint_shows_the_default():
    prompt, out = make("\n")
    prompt.confirm("Go?", default=True)
    assert out.getvalue() == "Go? [Y/n]: "
    prompt, out = make("\n")
    prompt.confirm("Go?")
    assert out.getvalue() == "Go? [y/N]: "


def test_confirm_invalid_answer_reprompts():
    prompt, out = make("maybe\ny\n")
    assert prompt.confirm("Go?") is True
    assert out.getvalue().count("Please answer yes or no.") == 1


def test_confirm_cancel_returns_false_even_with_true_default():
    prompt, _ = make("")
    assert prompt.confirm("Go?", default=True) is False


def test_confirm_cancel_after_invalid_answer():
    prompt, _ = make("maybe\n")
    assert prompt.confirm("Go?", default=True) is False


# -- select ------------------------------------------------------------


def test_select_by_number():
    prompt, out = make("2\n")
    assert prompt.select("Pick", ["red", "green", "blue"]) == "green"
    assert out.getvalue() == "Pick\n  1. red\n  2. green\n  3. blue\nChoose 1-3: "


def test_select_by_text_ignores_case():
    prompt, _ = make("BLUE\n")
    assert prompt.select("Pick", ["red", "green", "blue"]) == "blue"


@pytest.mark.parametrize("bad", ["0", "4", "-1", "purple", "1.5"])
def test_select_invalid_answer_reprompts_without_relisting(bad):
    prompt, out = make(f"{bad}\n3\n")
    assert prompt.select("Pick", ["red", "green", "blue"]) == "blue"
    assert out.getvalue().count("1. red") == 1
    assert "Enter a number from 1 to 3." in out.getvalue()


def test_select_empty_answer_returns_default_and_shows_it():
    prompt, out = make("\n")
    assert prompt.select("Pick", ["red", "green"], default="green") == "green"
    assert out.getvalue().endswith("Choose 1-2 [2]: ")


def test_select_empty_answer_without_default_reprompts():
    prompt, _ = make("\n1\n")
    assert prompt.select("Pick", ["red", "green"]) == "red"


def test_select_cancel_returns_none():
    prompt, _ = make("")
    assert prompt.select("Pick", ["red"], default="red") is None


def test_select_numeric_answer_is_a_position_not_option_text():
    prompt, _ = make("2\n")
    assert prompt.select("Pick", ["10", "20"]) == "20"


@pytest.mark.parametrize("bad", [[], "abc", [1, 2], None])
def test_select_invalid_options_raise(bad):
    prompt, _ = make("1\n")
    with pytest.raises(ValueError):
        prompt.select("Pick", bad)


def test_select_default_must_be_an_option():
    prompt, _ = make("1\n")
    with pytest.raises(ValueError):
        prompt.select("Pick", ["red"], default="blue")


# -- shared behaviour --------------------------------------------------


def test_color_wraps_the_question_only():
    prompt, out = make("x\n", color="<c>", endc="</c>")
    prompt.ask("Name")
    assert out.getvalue() == "<c>Name</c>: "


def test_color_applies_to_confirm_and_select_messages():
    prompt, out = make("y\n", color="<c>", endc="</c>")
    prompt.confirm("Go?")
    assert out.getvalue().startswith("<c>Go?</c> ")
    prompt, out = make("1\n", color="<c>", endc="</c>")
    prompt.select("Pick", ["a"])
    assert out.getvalue().startswith("<c>Pick</c>\n")


def test_keyboard_interrupt_is_a_cancel():
    class Interrupting(io.StringIO):
        def readline(self, *args):
            raise KeyboardInterrupt

    out = io.StringIO()
    prompt = Prompt(stream=out, input_stream=Interrupting())
    assert prompt.ask("Name") is None
    assert prompt.confirm("Go?", default=True) is False
    assert prompt.select("Pick", ["a"]) is None


def test_closed_input_is_a_cancel():
    source = io.StringIO()
    source.close()
    prompt = Prompt(stream=io.StringIO(), input_stream=source)
    assert prompt.ask("Name") is None


def test_closed_output_is_a_cancel():
    out = io.StringIO()
    out.close()
    prompt = Prompt(stream=out, input_stream=io.StringIO("yes\n"))
    assert prompt.confirm("Go?", default=True) is False


def test_default_streams_are_resolved_at_call_time(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("Ada\n"))
    assert Prompt().ask("Name") == "Ada"
    assert capsys.readouterr().out == "Name: "


def test_successive_calls_read_successive_lines():
    prompt, _ = make("Ada\ny\n2\n")
    assert prompt.ask("Name") == "Ada"
    assert prompt.confirm("Go?") is True
    assert prompt.select("Pick", ["a", "b"]) == "b"
