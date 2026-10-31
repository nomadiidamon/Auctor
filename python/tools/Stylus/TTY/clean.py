"""Clean Python artifacts for Stylus.TTY; the shared clean tool covers the repository."""
import subprocess
import sys
from pathlib import Path

CLEAN_TOOL = Path(__file__).resolve().parents[2] / "Livy" / "clean.py"


def main() -> int:
    print("[Stylus.TTY] clean")
    return subprocess.call([sys.executable, str(CLEAN_TOOL), *sys.argv[1:]])


if __name__ == "__main__":
    sys.exit(main())
