import pytest

from Auctor.Stylus.Colors import Colors, Style

EXPECTED_VALUES = {
    "HEADER": "\033[95m",
    "FAIL": "\033[91m",
    "WARNING": "\033[93m",
    "OKGREEN": "\033[92m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKYELLOW": "\033[93m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "ITALICS": "\033[3m",
    "UNDERLINE": "\033[4m",
}


@pytest.mark.parametrize("name,value", EXPECTED_VALUES.items())
def test_constant_value(name, value):
    assert getattr(Colors, name) == value


def test_no_unexpected_constants():
    assert {n for n in vars(Colors) if n.isupper()} == set(EXPECTED_VALUES)


def test_style_wraps_and_resets():
    assert Style("hi", Colors.FAIL) == "\033[91mhi\033[0m"


def test_style_combines_codes_in_order():
    assert Style("hi", Colors.BOLD, Colors.OKCYAN) == "\033[1m\033[96mhi\033[0m"


def test_style_without_codes_is_unchanged():
    assert Style("hi") == "hi"


def test_style_empty_text_still_wrapped():
    assert Style("", Colors.BOLD) == "\033[1m\033[0m"
