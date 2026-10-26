"""Run the Auctor test suite; currently delegates to Livy. Extra arguments go to pytest."""
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent


def main() -> int:
    print("[Auctor] run tests")
    return subprocess.call([sys.executable, str(TOOLS_DIR / "Livy" / "run_tests.py"), *sys.argv[1:]])


if __name__ == "__main__":
    sys.exit(main())
