"""JVM types of theories, re-exported from 2P-Kt's `it.unibo.tuprolog.theory`."""

import it.unibo.tuprolog.theory as _theory  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["MutableTheory", "RetractResult", "Theory"]


Theory = _theory.Theory
"""An ordered collection of clauses, i.e. a logic program or knowledge base.

Plain theories are immutable: the operations "changing" them return new theories. Clauses must be
well-formed (e.g. their heads must be structures, not variables or numbers), or adding them raises
an `IllegalArgumentException`.

Python protocols (see `tuprolog.theory._adapters`):
    - `len(theory)`: the amount of clauses.
    - `item in theory`: whether a clause is in the theory, any clause has the given head (a
      `tuprolog.core.Struct`), or any clause has the given predicate indicator (e.g. `parent/2`).
    - `theory[key]`: the clauses unifying with a clause, the rules whose head unifies with a
      structure, or the rules of a predicate indicator, as a lazy iterable.
    - `theory + other`: a theory with the clauses of `other` (a theory or a clause) appended.
    - `==`: the theories have equal clauses, in the same order; immutable theories are hashable.

Members:
    - `clauses`, `rules`, `directives`: the (lazy) iterables of all clauses, of rules (facts
      included, as they are rules whose body is `true`), and of directives.
    - `size`, `is_empty`, `is_non_empty`, `is_mutable`: the amount of clauses, and flags.
    - `unificator`, `set_unificator(unificator)`: the `tuprolog.unify.Unificator` matching
      clauses, and a copy of the theory using another one.
    - `assert_a(clause, ...)`, `assert_z(clause, ...)`: the theory with clauses (or facts, from
      structures) added at its beginning or at its end.
    - `retract(clause, ...)`, `retract_all(clause)`: the `RetractResult` of removing the first
      clause unifying with each template, or all of them.
    - `abolish(name, arity)`, `abolish(indicator=...)`: the theory without the clauses of a
      predicate.
    - `to_mutable_theory()`, `to_immutable_theory()`, `clone()`: conversions and copies.
    - `to_string(as_prolog_text=False)`: the theory as a string, or as Prolog source code.

Examples:
    >>> from tuprolog.core import fact, struct, var
    >>> from tuprolog.theory import theory
    >>> kb = theory(fact(struct("f", "a")), fact(struct("f", "b")))
    >>> kb.assert_a(struct("f", "c"))
    IndexedTheory{ f(c) :- true. f(a) :- true. f(b) :- true }
    >>> len(kb)
    2

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.theory.Theory` interface, whose static factories (e.g.
    `Theory.empty()`, `Theory.indexedOf(unificator, clauses)`, `Theory.listedOf(unificator,
    clauses)`) are available too.
"""

MutableTheory = _theory.MutableTheory
"""A `Theory` which changes in place.

`assert_a`, `assert_z`, `retract`, `retract_all` and `abolish` modify the theory itself (and
return it, or a `RetractResult` wrapping it), which is cheaper than building new theories when
clauses change often: every reference to the theory sees the changes. Mutable theories are not
hashable, as their equality depends on their changing clauses.

Examples:
    >>> from tuprolog.core import struct
    >>> from tuprolog.theory import mutable_theory
    >>> kb = mutable_theory()
    >>> _ = kb.assert_z(struct("f", "a"))
    >>> len(kb)
    1

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.theory.MutableTheory` interface.
"""

RetractResult = _theory.RetractResult
"""The outcome of retracting clauses from a `Theory` (see `Theory.retract` and
`Theory.retract_all`).

It is either a `RetractResult.Success`, if some clauses were removed, or a
`RetractResult.Failure`, if no clause matched.

Members:
    - `is_success`, `is_failure`: which outcome it is.
    - `theory`: the theory resulting from the operation (unchanged on failure).
    - `clauses`: the removed clauses (None on failure).
    - `first_clause`: the first removed clause (None on failure).

Examples:
    >>> from tuprolog.core import struct, var
    >>> from tuprolog.theory.parsing import parse_theory
    >>> kb = parse_theory("f(a). f(b).")
    >>> result = kb.retract(struct("f", var("X")))
    >>> result.is_success, result.first_clause, len(result.theory)
    (True, f(a) :- true, 1)
    >>> kb.retract(struct("g", var("X"))).is_failure
    True

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.theory.RetractResult` sealed class.
"""

logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.*")
