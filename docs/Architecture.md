# Auctor Architecture

Auctor is a standalone utility library for filesystem operations, data interpretation, terminal interaction, and diagnostics. Its components have distinct responsibilities so applications can use them independently and implementations can evolve without importing application-specific policy.

## Component map

```text
Auctor
├── EnvironmentDefaults
├── Runtime
├── Livy
├── Carmen
│   ├── Cicero
│   ├── Ovid
│   └── Herodotus
├── Scriptor
│   ├── JSON
│   ├── Config
│   ├── Parsing
│   └── Fences
└── Stylus
    ├── Colors
    ├── TTY
    ├── Prompt
    └── Spinner
```

| Component | Responsibility | Submodules |
|---|---|---|
| EnvironmentDefaults | Declare immutable, namespaced package settings | Root contract for package default providers |
| Runtime | Aggregate package defaults and coordinate lifecycle | Environment mapping; other managed services as implemented |
| Livy | Logging, categories, diagnostics, and last-failure tracking | `Livy`, `Category`, `Failure` |
| Carmen | Move information between the filesystem and memory | Cicero (read), Ovid (write), Herodotus (discovery, mutation, and operation history) |
| Scriptor | Interpret and transform information in memory | JSON, Config, Parsing, Fences |
| Stylus | Provide terminal-facing utilities | Colors, TTY, Prompt, Spinner |

Package settings stay Auctor-owned. Runtime aggregates package defaults into a namespaced in-memory mapping; Scriptor.Config will provide file persistence later.

The architectural boundary is: **Carmen moves information between the filesystem and memory; Scriptor interprets it in memory; Stylus mediates with the terminal; Livy records what happened.** Runtime coordinates lifecycle rather than owning those domain responsibilities.

## Relationships

- Cicero may delegate format interpretation to Scriptor, such as parsing JSON after reading file contents.
- Ovid may delegate serialization or formatting to Scriptor before writing the result.
- Carmen operations are intended to return simple public outcomes, report diagnostic detail through Livy, and record attempted operations in Herodotus history.
- Stylus is a terminal utility group and does not depend on Livy.
- Consumers choose their own category names and domain meanings; Auctor does not impose application configuration, authorization, or policy.

These are component boundaries, not a requirement that every operation initialize or call every other component. Each subsystem should remain usable on its own where practical.

## Repository layout

```text
README.md          Project overview and entry points
docs/              Architecture, concepts, semantics, and component references
examples/python/   Python examples
examples/cpp/      C++ examples
python/             Python package, tests, and development scripts
cpp/                Reserved for the planned C++ implementation
```

The Python package source is under `python/src/Auctor/`:

```text
Auctor/
├── environment.py
├── Runtime/
├── Livy/
├── Carmen/
│   ├── Cicero/
│   ├── Ovid/
│   └── Herodotus/
├── Scriptor/
└── Stylus/
    ├── Colors/
    ├── TTY/
    ├── Prompt/
    └── Spinner/
```

## Implementation status

The repository is designed for independent Python and C++ implementations of a shared semantic contract. Status is not the same as architectural intent:

| Area | Python | C++ |
|---|---|---|
| Livy | Implemented | Planned |
| Runtime environment defaults | Implemented | Planned |
| Stylus Colors, Prompt, Spinner, TTY | Implemented | Planned |
| Carmen, Scriptor, broader Runtime lifecycle | Planned or skeletal package namespaces | Planned |

The `cpp/` directory is currently empty. The implemented Python Runtime settings, Livy, and Stylus APIs are documented in [Runtime](Runtime.md), [Livy](Livy.md), and [Stylus](Stylus.md). Those references describe current behavior; this architecture describes the broader component model.

## Further reading

- [Concepts](Concepts.md) explains the cross-language API approach and language-independent design ideas.
- [Semantics](Semantics.md) defines expected failures and the shared behavioral contract.
- [Runtime](Runtime.md) documents package environment defaults and current Runtime settings.
- [Livy](Livy.md) documents the implemented Python logging and diagnostics API.
- [Stylus](Stylus.md) documents the implemented Python terminal utilities.