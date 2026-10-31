"""
@example runtime_environment.py
Read and override Auctor-owned settings without changing os.environ.
"""

from Auctor import initialize_auctor, shutdown_auctor
from Auctor.Runtime import get_auctor_environment, set_auctor_environment_value

initialize_auctor()
initial = get_auctor_environment("Stylus.TTY")
print("default force color:", initial["FORCE_COLOR"])

set_auctor_environment_value("Stylus.TTY.FORCE_COLOR", True)
updated = get_auctor_environment("Stylus.TTY")
print("updated force color:", updated["FORCE_COLOR"])
shutdown_auctor()
