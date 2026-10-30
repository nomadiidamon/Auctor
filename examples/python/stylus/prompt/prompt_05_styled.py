"""
@example prompt_05_styled.py
Color the question text with Stylus.Colors.
"""

import io

from Auctor.Stylus.Colors import Colors
from Auctor.Stylus.Prompt import Prompt

prompt = Prompt(color=Colors.OKCYAN, endc=Colors.ENDC, input_stream=io.StringIO("Ada\n"))
print("name:", prompt.ask("Name"))
