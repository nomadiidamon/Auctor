"""Clean Python artifacts produced by Auctor root tests."""
import subprocess
import sys
from pathlib import Path

CLEAN_TOOL = Path(__file__).resolve().parents[1] / "Livy" / "clean.py"


def main() -> int:
    print("[Auctor.Environment] clean")
    return subprocess.call([sys.executable, str(CLEAN_TOOL), *sys.argv[1:]])


if __name__ == "__main__":
    sys.exit(main())
