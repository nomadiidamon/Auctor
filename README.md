# Auctor

Auctor: A standalone utility library for diagnostics, filesystem operations, data processing, and terminal interaction. It separates these responsibilities into components that can be used independently and is designed around a shared semantic contract for Python and C++ implementations

Auctor was developed by extracting common logic from [Domus-AI](https://github.com/nomadiidamon/Domus-AI), but it has no dependency on that project or its application-specific policies.

## Documentation

- [Architecture](docs/Architecture.md): components, submodules, boundaries, repository layout, and implementation status.
- [Concepts](docs/Concepts.md): language-independent design and cross-language API approach.
- [Semantics](docs/Semantics.md): expected failure values, programming errors, and diagnostic responsibilities.
- [Runtime](docs/Runtime.md): package environment defaults and Runtime settings.
- [Livy](docs/Livy.md): Python logging and diagnostics reference.
- [Stylus](docs/Stylus.md): Python terminal utility reference.

## Project status

The Python package is the current implementation. Livy and Stylus Colors, Prompt, Spinner, and TTY are implemented. Runtime provides package environment-default aggregation; broader Runtime lifecycle, Carmen, and Scriptor features remain planned or skeletal. The `cpp/` directory is reserved for the planned C++ implementation and is currently empty. See [Architecture](docs/Architecture.md) for component status.

## Python

The current Python package requires Python 3.10 or newer. It is not yet published on PyPI.

For the development environment and test setup, see [Contributing: Development Setup](CONTRIBUTING.md#development-setup).

Examples are under `examples/python/`; component-specific references include their example and test locations.
Examples are under `examples/python/`; component-specific references include their example and test locations. Auctor defaults examples are in [examples/python/auctor](examples/python/auctor), and Runtime lifecycle/settings examples are in [examples/python/runtime](examples/python/runtime).

See [CONTRIBUTING](CONTRIBUTING.md) for development guidance.
