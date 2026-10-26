"""
@example 04_categories.py
Group messages under externally named categories.
"""

import tempfile

from Auctor.Livy import Livy

with tempfile.TemporaryDirectory() as tmp:
    with Livy("Example", path=tmp) as livy:
        # Category names are plain strings chosen by the consumer.
        importer = livy.create_category("Importer")
        filesystem = livy.create_category("Filesystem")

        # The same name always returns the same category.
        assert livy.create_category("Importer") is importer

        livy.info("no category")
        importer.info("step complete", step=1)
        filesystem.warning("slow disk")

    print(livy.log_file.read_text())
