"""Run every Stylus sub-suite in order; extra arguments are passed to pytest."""
import os
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = TOOLS_DIR.parent.parent / "tests" / "test_output.txt"
SUBMODULES = ["Colors", "Spinner", "Prompt"]


def main() -> int:
    print("[Stylus] run tests")
    if not os.environ.get("AUCTOR_TEST_APPEND"):
        OUTPUT_FILE.write_text("", encoding="utf-8")
    env = {**os.environ, "AUCTOR_TEST_APPEND": "1"}
    rc = 0
    for name in SUBMODULES:
        result = subprocess.call(
            [sys.executable, str(TOOLS_DIR / name / "run_tests.py"), *sys.argv[1:]], env=env
        )
        rc = rc or result
    return rc


if __name__ == "__main__":
    sys.exit(main())
