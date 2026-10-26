"""Whole-package Livy scenarios."""

import warnings

from Auctor.Livy import Category, Failure, Livy, shutdown_all


def test_public_exports():
    from Auctor import Livy as package

    assert set(package.__all__) == {"Livy", "Category", "Failure", "shutdown_all"}


def test_end_to_end_workflow(tmp_path):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        livy = Livy("App", tmp_path)
        assert livy.initialize()

        importer = livy.create_category("Importer")
        fs = livy.create_category("Filesystem")
        livy.info("starting")
        importer.info("step 1", n=1)
        fs.error("cannot read", path="a.txt")
        importer.exception(RuntimeError("halt"))

        assert isinstance(fs, Category)
        assert isinstance(livy.get_last_failure(), Failure)
        assert livy.get_last_failure().category == "Importer"
        assert fs.get_last_failure().message == "cannot read path='a.txt'"
        assert importer.get_last_failure().level == "EXCEPTION"

        livy.shutdown()

    text = (tmp_path / "livy.log").read_text()
    assert "[-] starting" in text
    assert "[Importer] step 1 n=1" in text
    assert "[Filesystem] cannot read path='a.txt'" in text
    assert "RuntimeError: halt" in text


def test_two_contexts_stay_independent_and_shutdown_all_closes_both(tmp_path):
    a, b = Livy("A", tmp_path / "a"), Livy("B", tmp_path / "b")
    a.initialize()
    b.initialize()
    a.create_category("X").error("only a")
    assert b.get_last_failure() is None
    assert b.create_category("X").get_last_failure() is None

    shutdown_all()
    assert not a.is_initialized() and not b.is_initialized()
    assert "only a" in (tmp_path / "a" / "livy.log").read_text()
    assert "only a" not in (tmp_path / "b" / "livy.log").read_text()
