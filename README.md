# Auctor

Auctor is a standalone library of reusable logging, filesystem, parsing, and terminal utilities. It separates these responsibilities into components that can be used independently and is designed around a shared semantic contract with idiomatic Python and C++ implementations.

Auctor was developed by extracting common logic from [Domus-AI](https://github.com/nomadiidamon/Domus-AI), but it has no dependency on that project or its application-specific policies.

## Documentation

- [Architecture](docs/Architecture.md): components, submodules, boundaries, repository layout, and implementation status.
- [Concepts](docs/Concepts.md): language-independent design and cross-language API approach.
- [Semantics](docs/Semantics.md): expected failure values, programming errors, and diagnostic responsibilities.
- [Livy](docs/Livy.md): Python logging and diagnostics reference.
- [Stylus](docs/Stylus.md): Python terminal utility reference.

## Project status

The Python package is the current implementation. Livy and Stylus Colors, Prompt, and Spinner are implemented; other Python component namespaces are skeletal or planned. The `cpp/` directory is reserved for the planned C++ implementation and is currently empty. See [Architecture](docs/Architecture.md) for the component-by-component status.

## Python

The current Python package requires Python 3.10 or newer. It is not yet published on PyPI; install it from the repository:

```bash
cd python
pip install -e .
```

For the development environment and test setup, see [Contributing: Development Setup](CONTRIBUTING.md#development-setup).

Examples are under `examples/python/`; component-specific references include their example and test locations.

See [CONTRIBUTING](CONTRIBUTING.md) for development guidance.
