"""Factories of theories."""

from collections.abc import Iterable

from tuprolog.core import Clause
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.unify import Unificator

from ._definitions import MutableTheory, Theory

__all__ = ["mutable_theory", "theory"]


def theory(*clauses: Clause | Iterable[Clause]) -> Theory:
    """Creates an immutable, indexed theory containing the given clauses.

    Args:
        *clauses: The clauses, in order, either as arguments or as one iterable.

    Returns:
        The theory, whose clauses are matched by the default `tuprolog.unify.Unificator`.

    Raises:
        IllegalArgumentException: If some clause is not well-formed (e.g. its head is a variable).

    Examples:
        >>> from tuprolog.core import atom, fact, rule, struct, var
        >>> X = var("X")
        >>> theory(fact(struct("human", "socrates")), rule(struct("mortal", X), struct("human", X)))
        IndexedTheory{ human(socrates) :- true. mortal(X_...) :- human(X_...) }
        >>> len(theory([fact(atom("a")), fact(atom("b"))]))
        2
        >>> len(theory())
        0

    See Also:
        `mutable_theory`, and `tuprolog.theory.parsing.parse_theory` to parse theories.

    Note:
        Wraps 2P-Kt's `Theory.of`.
    """
    return iterable_or_varargs(clauses, lambda ts: Theory.of(jiterable(ts)))


def mutable_theory(*clauses: Clause | Iterable[Clause]) -> MutableTheory:
    """Creates a mutable, indexed theory containing the given clauses.

    Args:
        *clauses: The clauses, in order, either as arguments or as one iterable.

    Returns:
        The mutable theory, whose clauses are matched by the default `tuprolog.unify.Unificator`.

    Raises:
        IllegalArgumentException: If some clause is not well-formed.

    Examples:
        >>> from tuprolog.core import fact, struct
        >>> kb = mutable_theory(fact(struct("f", "a")))
        >>> _ = kb.assert_z(fact(struct("f", "b")))
        >>> kb
        MutableIndexedTheory{ f(a) :- true. f(b) :- true }

    See Also:
        `theory`, for immutable theories.

    Note:
        Wraps 2P-Kt's `MutableTheory.of`.
    """
    return iterable_or_varargs(
        clauses, lambda ts: MutableTheory.of(Unificator.getDefault(), jiterable(ts))
    )
