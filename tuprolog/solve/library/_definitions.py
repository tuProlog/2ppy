"""The JVM types of libraries and runtimes, re-exported by `tuprolog.solve.library`."""

import it.unibo.tuprolog.solve.library as _library  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["Library", "Pluggable", "Runtime"]


Library = _library.Library
"""A library: an aliased bundle of primitives, functions, clauses and operators (a `Pluggable`).

Members: `alias`, and those of `Pluggable`; Python additions: `to_runtime()`, the runtime made of
this library only. Create libraries with `library`.

Examples:
    >>> from tuprolog.solve.library import library
    >>> lib = library("my.lib")
    >>> lib.alias, list(lib.to_runtime().aliases)
    ('my.lib', ['my.lib'])
"""


Pluggable = _library.Pluggable
"""Something a solver can load: the base of `Library` and `Runtime`.

Members: `primitives` and `functions` (JVM maps from signatures), `clauses` (a list),
`operators` (an `OperatorSet`), and the lookups `has_primitive(signature)`,
`has_function(signature)`, `has_rule(signature)`, `rules_signatures`, `has_protected(signature)`
(whether programs cannot change a predicate, e.g. via `assertz/1`).
"""


Runtime = _library.Runtime
"""A runtime: the set of libraries loaded by a solver, a read-only JVM map from aliases.

Members: `aliases`, `libraries`, `runtime[alias]`, `minus(alias)` (a runtime without that
library), and those of `Pluggable`, merging the contents of all the libraries. Python additions:
`runtime + other` merges a library or another runtime, raising
`tuprolog.solve.library.exception.AlreadyLoadedLibraryException` if an alias is already loaded.
Create runtimes with `libraries`.

Examples:
    >>> from tuprolog.solve.library import libraries, library
    >>> runtime = libraries(library("a.lib")) + library("b.lib")
    >>> list(runtime.aliases)
    ['a.lib', 'b.lib']
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.*")
