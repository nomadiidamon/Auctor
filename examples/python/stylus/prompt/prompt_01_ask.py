"""
@example prompt_01_ask.py
Read a line of text, with and without a default. Input is scripted so the example never blocks.
"""

import io

from Auctor.Stylus.Prompt import Prompt

# Pass a real terminal by leaving out input_stream; here the answers are scripted.
prompt = Prompt(input_stream=io.StringIO("Ada\n\n"))

name = prompt.ask("Name")
print("name:", name)

# An empty answer returns the default.
city = prompt.ask("City", default="London")
print("city:", city)
