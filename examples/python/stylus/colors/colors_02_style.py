"""
@example colors_02_style.py
Wrap text with Style(); the reset sequence is appended automatically.
"""

from Auctor.Stylus.Colors import Colors, Style

print(Style("error: something failed", Colors.FAIL))
print(Style("combined codes", Colors.BOLD, Colors.OKCYAN))

# With no codes the text is returned unchanged.
assert Style("plain") == "plain"
