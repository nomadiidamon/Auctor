"""
@example tty_02_override.py
Set an Auctor-owned color override without changing process environment variables.
"""

from Auctor import initialize_auctor
from Auctor.Runtime import set_auctor_environment_value
from Auctor.Stylus.TTY import TTY

initialize_auctor()
set_auctor_environment_value("Stylus.TTY.FORCE_COLOR", True)
print("forced color support:", TTY().supports_color())
