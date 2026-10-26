import pytest

from Auctor.Livy import Category, Livy


@pytest.fixture
def livy(tmp_path):
    with Livy("Cat", tmp_path) as instance:
        yield instance


def test_name_and_identity(livy):
    cat = livy.create_category("Importer")
    assert isinstance(cat, Category)
    assert cat.name == "Importer"
    assert livy.create_category("Importer") is cat


@pytest.mark.parametrize("name", ["", None, 5])
def test_invalid_name_raises(livy, name):
    with pytest.raises(ValueError):
        livy.create_category(name)


def test_levels_write_category_tag(livy):
    cat = livy.create_category("Parser")
    cat.debug("d")
    cat.info("i")
    cat.warning("w")
    cat.error("e")
    livy.shutdown()
    text = livy.log_file.read_text()
    for level, msg in [("DEBUG", "d"), ("INFO", "i"), ("WARNING", "w"), ("ERROR", "e")]:
        assert f"[{level}] [Parser] {msg}" in text


def test_context_is_appended(livy):
    livy.create_category("Net").info("sent", bytes=3)
    livy.shutdown()
    assert "sent bytes=3" in livy.log_file.read_text()


def test_exception_records_traceback(livy):
    cat = livy.create_category("UI")
    cat.exception(ValueError("bad"))
    failure = cat.get_last_failure()
    assert failure.level == "EXCEPTION"
    assert "ValueError" in failure.exception


def test_last_failure_is_per_category(livy):
    a, b = livy.create_category("A"), livy.create_category("B")
    assert a.get_last_failure() is None
    a.error("one")
    assert a.get_last_failure().message == "one"
    assert b.get_last_failure() is None
    b.error("two")
    assert a.get_last_failure().message == "one"


def test_info_does_not_set_failure(livy):
    cat = livy.create_category("A")
    cat.info("fine")
    assert cat.get_last_failure() is None
