# Auctor

A standalone logging, filesystem, parsing, and terminal utility library with a shared semantic API implemented independently in Python and C++.

Auctor was developed by abstracting useful and common logic from Domus-AI [Domus-AI](https://github.com/nomadiidamon/Domus-AI).

## Components

| Component | Purpose |
|---|---|
| Runtime | Initializes and shuts down Auctor-wide infrastructure |
| Livy | Logging, diagnostics, categories, last-failure tracking |
| Carmen | Filesystem interaction: Cicero (read), Ovid (write), Herodotus (discovery, mutation, operation history) |
| Scriptor | JSON, configuration, parsing, and fenced blocks |
| Stylus | Colors, TTY, prompting, and spinner |

Carmen moves information between the filesystem and memory; Scriptor interprets it in memory; Stylus mediates with the terminal; Livy records what happened.

## Livy

Livy is implemented in Python. See the [Livy README](python/src/Auctor/Livy/README.md), the [Livy documentation](docs/Livy.md) and the [Livy examples](examples/python/livy).

## Failure semantics

- Expected read/discovery/parse failures return `None` or an empty value.
- Expected mutation failures return `False`.
- Programming errors raise exceptions.

## Layout

```text
python/     Python package and tests
cpp/        C++ implementation (Premake 5, planned)
examples/   Python and C++ examples
docs/       Documentation
```

## Python

```bash
cd python
pip install -e .
```

Requires Python 3.10+.

### Development

```bash
cd python
pip install -e ".[dev]"
pytest
```

## Status

Early development.
