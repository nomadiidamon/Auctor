"""
@example prompt_03_select.py
Choose from numbered options by number or by name.
"""

import io

from Auctor.Stylus.Prompt import Prompt

colors = ["red", "green", "blue"]

prompt = Prompt(input_stream=io.StringIO("2\nBLUE\n\n"))

print("by number:", prompt.select("Pick a color", colors))
print("by name:", prompt.select("Pick a color", colors))

# An empty answer takes the default, which must be one of the options.
print("default:", prompt.select("Pick a color", colors, default="green"))
