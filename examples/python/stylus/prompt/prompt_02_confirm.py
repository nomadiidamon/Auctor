"""
@example prompt_02_confirm.py
Ask yes/no questions; invalid answers are asked again.
"""

import io

from Auctor.Stylus.Prompt import Prompt

prompt = Prompt(input_stream=io.StringIO("maybe\nyes\n\n"))

# "maybe" is rejected and the question is repeated.
print("proceed:", prompt.confirm("Proceed?"))

# An empty answer takes the default.
print("overwrite:", prompt.confirm("Overwrite?", default=True))
