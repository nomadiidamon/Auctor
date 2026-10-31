# Auctor Concepts

Auctor is a standalone mechanism library: it provides reusable operations without taking ownership of an application's domain model, configuration meaning, or policy. It was developed by extracting common logic from [Domus-AI](https://github.com/nomadiidamon/Domus-AI), but does not require Domus-AI.

## One contract, idiomatic implementations

Python and C++ are independent implementations of one language-neutral semantic contract. The contract is about observable behavior, not identical source code or a shared runtime.

Equivalent public concepts should remain recognizable across languages while following local conventions. For example:

| Concept | Python style | C++ style |
|---|---|---|
| Read text | `read_text()` | `ReadText()` |
| Create category | `create_category()` | `CreateCategory()` |
| Retrieve last failure | `get_last_failure()` | `GetLastFailure()` |

Return types use each language's normal vocabulary while preserving the same semantic outcome. A failed optional read can be `None` in Python and an empty `std::optional` in C++; a failed mutation is `False` / `false`. The shared contract is documented in [Semantics](Semantics.md).

## Language-independent boundaries

- **Carmen is filesystem I/O.** Its `root` argument, where offered, is path context (`root / path`), not an authorization or permission system.
- **Scriptor is interpretation.** It parses, serializes, and recognizes structured content in memory; it does not own file access.
- **Stylus is terminal interaction.** It handles terminal-oriented presentation and input without imposing application workflow.
- **Livy is diagnostics.** A Livy instance owns its logging and last-failure context; it is not a factory for a global logger.
- **Runtime is lifecycle coordination.** It initializes and shuts down infrastructure that needs process-level coordination.

The intended flow is to compose these responsibilities: read data with Carmen, interpret it with Scriptor, present or request input with Stylus, and record diagnostics with Livy. Applications remain responsible for their own policies and decisions.

## Generic, not domain-specific

Auctor APIs should describe reusable operations rather than encode meanings from a consuming application. Configuration access, for example, can read or set a key without knowing what that key means. Category names are selected by consumers. A filesystem root provides context but does not grant or restrict authority.

This separation keeps the package useful outside its source project and allows each component to be adopted independently.

## Further reading

- [Architecture](Architecture.md) describes the component tree, module boundaries, repository layout, and implementation status.
- [Semantics](Semantics.md) describes the shared failure contract.
- [Livy](Livy.md) and [Stylus](Stylus.md) describe their current Python APIs.