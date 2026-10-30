"""
@example colors_01_palette.py
Print every Colors constant by name, using its own escape sequence.
"""

from Auctor.Stylus.Colors import Colors

names = [name for name in vars(Colors) if name.isupper() and name != "ENDC"]
for name in names:
    print(f"{getattr(Colors, name)}{name}{Colors.ENDC}")
