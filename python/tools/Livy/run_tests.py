"""Run the Livy test suite; extra arguments are passed to pytest."""
import os
import subprocess
import sys
from pathlib import Path

PYTHON_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_FILE = PYTHON_DIR / "tests" / "test_output.txt"
TEST_DIR = Path("tests") / "Livy"


def main() -> int:
    print("[Livy] run tests")
    cmd = [sys.executable, "-m", "pytest", str(TEST_DIR), *sys.argv[1:]]
    # Overwrites the previous run's output unless an aggregate runner asks to accumulate.
    mode = "a" if os.environ.get("AUCTOR_TEST_APPEND") else "w"
    with open(OUTPUT_FILE, mode, encoding="utf-8") as out:
        proc = subprocess.Popen(
            cmd,
            cwd=PYTHON_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        for line in proc.stdout:
            sys.stdout.write(line)
            out.write(line)
        return proc.wait()


if __name__ == "__main__":
    sys.exit(main())
