from collections.abc import Iterable
from functools import singledispatch

from tuprolog.core import Atom, Integer, Struct, Term
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs

from ._definitions import Operator, OperatorSet, Specifier

__all__ = ["operator", "operator_set", "specifier"]


@singledispatch
def operator(functor: str, specifier: Specifier, priority: int) -> Operator:
    """Creates an operator, from its parts or from an `op/3` term.

    It takes either `(functor, specifier, priority)`, as Python values, or `(priority, specifier,
    functor)`, as terms (as in `op(Priority, Specifier, Functor)`), or a single `op/3` structure.

    Args:
        functor: the functor of the operator, e.g. `"+"`.
        specifier: its position and associativity (a `Specifier`, see `specifier`).
        priority: its priority, from 1 (binding tightest) to 1200.

    Returns:
        The operator.

    Examples:
        >>> from tuprolog.core.operators import *
        >>> operator("++", XFX, 700)
        Operator(700, XFX, '++')
        >>> from tuprolog.core import atom, integer, struct
        >>> operator(integer(700), atom("xfx"), atom("++"))
        Operator(700, XFX, '++')
        >>> operator(struct("op", integer(700), atom("xfx"), atom("++")))
        Operator(700, XFX, '++')

    Note:
        Wraps 2P-Kt's `Operator` constructor, `Operator.fromTerms` and `Operator.fromTerm`.
    """
    return Operator(functor, specifier, priority)


@operator.register
def _(priority: Integer, specifier: Atom, functor: Atom) -> Operator:
    return Operator.fromTerms(priority, specifier, functor)


@operator.register
def _(term: Struct) -> Operator:
    return Operator.fromTerm(term)


def operator_set(*operators: Operator | Iterable[Operator]) -> OperatorSet:
    """Creates an operator set.

    Args:
        *operators: the operators, either as many arguments or as a single iterable. No operators
            give an empty set.

    Returns:
        The operator set.

    Examples:
        >>> from tuprolog.core.operators import *
        >>> operator_set(operator("++", XFX, 700), operator("--", FY, 200))
        OperatorSet([...])
        >>> len(operator_set())
        0

    Note:
        Wraps 2P-Kt's `OperatorSet` constructor.
    """
    return iterable_or_varargs(operators, lambda os: OperatorSet(jiterable(os)))


@singledispatch
def specifier(name: str) -> Specifier:
    """Returns the specifier with a given name, as a string or a term.

    Args:
        name: the name of the specifier, as a string in any case (e.g. `"xfx"`), or as a term (an
            atom, e.g. `xfx`).

    Returns:
        The specifier.

    Raises:
        TypeError: if `name` is neither a string nor a term.
        java.lang.IllegalArgumentException: if there is no specifier with that name.

    Examples:
        >>> from tuprolog.core import atom
        >>> specifier("xfx"), specifier("YFX"), specifier(atom("fy"))
        (XFX, YFX, FY)

    Note:
        Wraps 2P-Kt's `Specifier.valueOf` and `Specifier.fromTerm`.
    """
    if not isinstance(name, str):
        raise TypeError(f"Cannot convert {type(name)} into Specifier")
    return Specifier.valueOf(name.upper())


@specifier.register
def _(term: Term) -> Specifier:
    return Specifier.fromTerm(term)
