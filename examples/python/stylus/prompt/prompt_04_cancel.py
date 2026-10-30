"""
@example prompt_04_cancel.py
Cancelling is an expected outcome: end of input returns None or False instead of raising.
"""

import io

from Auctor.Stylus.Prompt import Prompt

# An empty input stream behaves like Ctrl-D or Ctrl-C at the terminal.
prompt = Prompt(input_stream=io.StringIO(""))

print("ask:", prompt.ask("Name"))
print("confirm:", prompt.confirm("Proceed?", default=True))
print("select:", prompt.select("Pick", ["a", "b"]))
