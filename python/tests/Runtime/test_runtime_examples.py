import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "examples" / "python" / "runtime"
SRC_DIR = REPO_ROOT / "python" / "src"
EXAMPLES = sorted(EXAMPLES_DIR.glob("*.py"))


def test_examples_are_discovered():
    assert len(EXAMPLES) >= 2


@pytest.mark.parametrize("example", EXAMPLES, ids=lambda path: path.name)
def test_example_runs_cleanly(example, tmp_path):
    env = {**os.environ, "PYTHONPATH": str(SRC_DIR)}
    result = subprocess.run(
        [sys.executable, "-W", "error", str(example)],
        cwd=tmp_path,
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert list(tmp_path.iterdir()) == []
