"""The rules of the standard library, i.e. its predicates written in Prolog.

Each constant is a rule with a `signature` (its name and arity in Prolog), and an
`implementation`, i.e. the clause defining it; predicates defined by several clauses (`append/3`,
`member/2`, `;/2`) are classes grouping them. They are loaded by default in Prolog solvers.

Examples:
    >>> Once.implementation
    once(G_...) :- (ensure_executable(G_...), call(G_...), '!')
    >>> Append.SIGNATURE
    Signature(name=append, arity=3, vararg=false)
"""

import it.unibo.tuprolog.solve.stdlib.rule as _rule  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.solve import signature

__all__ = [
    "Append",
    "Arrow",
    "CurrentPrologFlag",
    "Member",
    "Not",
    "Once",
    "Semicolon",
    "SetPrologFlag",
]


_Append = _rule.Append


class Append:
    """The rules of `append/3`: a list is the concatenation of two others.

    Attributes:
        FUNCTOR: The name, `append`.
        ARITY: The arity, 3.
        SIGNATURE: The signature, `append/3`.
        Base: The base case, `append([], X, X).`
        Recursive: The recursive case, `append([X | Y], Z, [X | W]) :- append(Y, Z, W).`
    """

    FUNCTOR = _Append.FUNCTOR

    ARITY = _Append.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    Base = _Append.Base.INSTANCE

    Recursive = _Append.Recursive.INSTANCE


Arrow: _rule.Arrow = _rule.Arrow.INSTANCE
"""The rule of `->/2`: if-then, i.e. `(C -> T)` proves `T` if `C` holds (once)."""


CurrentPrologFlag: _rule.CurrentPrologFlag = _rule.CurrentPrologFlag.INSTANCE
"""The rule of `current_prolog_flag/2`: a flag and its value (see `tuprolog.solve.flags`)."""


_Member = _rule.Member


class Member:
    """The rules of `member/2`: a term is an element of a list.

    Attributes:
        FUNCTOR: The name, `member`.
        ARITY: The arity, 2.
        SIGNATURE: The signature, `member/2`.
        Base: The base case, `member(H, [H | _]).`
        Recursive: The recursive case, `member(H, [_ | T]) :- member(H, T).`
    """

    FUNCTOR = _Member.FUNCTOR

    ARITY = _Member.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    Base = _Member.Base.INSTANCE

    Recursive = _Member.Recursive.INSTANCE


Not: _rule.Not = _rule.Not.INSTANCE
"""The rule of `not/1`: negation as failure, like `\\+/1`."""


Once: _rule.Once = _rule.Once.INSTANCE
"""The rule of `once/1`: proves a goal, keeping its first solution only."""


_Semicolon = _rule.Semicolon


class Semicolon:
    """The rules of `;/2`: disjunction (`A ; B`) and if-then-else (`(C -> T ; E)`).

    Attributes:
        FUNCTOR: The name, `;`.
        ARITY: The arity, 2.
        SIGNATURE: The signature, `;/2`.
        If: The rules of if-then-else: `If.Then` proves `T` if `C` holds (once), `If.Else`
            proves `E` otherwise.
        Or: The rules of disjunction: `Or.Left` proves `A`, `Or.Right` proves `B`.
    """

    FUNCTOR = _Semicolon.FUNCTOR

    ARITY = _Semicolon.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    class If:
        """The rules of if-then-else, `(C -> T ; E)`: `Then` and `Else`."""

        Then = _Semicolon.If.Then.INSTANCE

        Else = _Semicolon.If.Else.INSTANCE

    class Or:
        """The rules of disjunction, `A ; B`: `Left` and `Right`."""

        Left = _Semicolon.Or.Left.INSTANCE

        Right = _Semicolon.Or.Right.INSTANCE


SetPrologFlag: _rule.SetPrologFlag = _rule.SetPrologFlag.INSTANCE
"""The rule of `set_prolog_flag/2`: sets the value of a flag."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.rule.*")
