# Auctor Semantics

This document describes the intended behavior shared by Auctor implementations. Python and C++ should express the same outcomes using their native types and conventions. Component references document implementation-specific details.

## Operational failures and programming errors

Auctor distinguishes expected environmental or operational failures from defects in the call or implementation:

> **An expected operational failure is represented by the operation's normal failure value. A programming error or violated invariant is an exception.**

Examples of expected operational failures include an unreadable file, a missing discovery target, or a destination that cannot be written. Examples of programming errors include invalid arguments, malformed internal state, or an impossible violated invariant.

| Operation family | Success | Expected operational failure |
|---|---|---|
| Read and discovery | Content, a value, or a collection | `None`, an empty collection, or the language-equivalent empty/non-value |
| Mutation | `True` | `False` |
| Parse or serialization | Parsed value or serialized representation | `None` or the language-equivalent empty/non-value |

Python uses appropriate values such as `None`, empty collections, and `False`. C++ uses corresponding values such as `std::optional` with no value, empty collections, and `false`. The precise return type belongs to each operation's API; callers should not infer that every read-like operation uses the same sentinel.

## Diagnostics and operation history

Simple return values keep callers from needing a general public Result/Error framework. Detailed diagnostic information is separate from the public outcome:

- **Livy** explains what failed and retains last-failure information.
- **Herodotus** is intended to record which Carmen operation was attempted and its outcome.
- **Carmen** exposes the operation's simple success or failure value.

For example, an expected text-read failure is intended to return a non-value, with the cause available through diagnostics and the failed attempt represented in Carmen history. These diagnostic and history integrations are architectural intent; they are not yet implemented for Carmen in this repository.

Livy itself has component-specific behavior: failed initialization or shutdown records a failure; `error()` and `exception()` update last-failure state, while `debug()`, `info()`, and `warning()` do not. See the [Livy reference](Livy.md) for its instance and category rules.

## Cancellation and invalid input

Cancellation is not automatically an operational failure or programming error. A component may define it as an ordinary domain outcome. For example, Stylus Prompt treats end-of-input, Ctrl-C, and closed or broken streams as cancellation: `ask()` and `select()` return `None`, while `confirm()` returns `False`.

Invalid arguments remain programming errors. For example, Prompt's `select()` raises `ValueError` for an empty or invalid options sequence or a default not present in the options. See [Stylus](Stylus.md) for the full Prompt contract.

## Cross-language consistency

Equivalent operations must agree on their observable meaning: what constitutes success, what the expected failure value means, which inputs are valid, and what side effects occur. Type names, casing, overloads, and idiomatic representations may differ by language. See [Concepts](Concepts.md) for the API design principles.