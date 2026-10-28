"""Clean Python artifacts for every Stylus submodule."""
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SUBMODULES = ["Colors"]


def main() -> int:
    print("[Stylus] clean")
    rc = 0
    for name in SUBMODULES:
        result = subprocess.call([sys.executable, str(TOOLS_DIR / name / "clean.py"), *sys.argv[1:]])
        rc = rc or result
    return rc


if __name__ == "__main__":
    sys.exit(main())
