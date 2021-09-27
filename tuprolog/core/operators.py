from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.core.operators as _operators
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.core import Atom, Integer, Struct, Term
from functools import singledispatch


Operator = _operators.Operator

OperatorSet = _operators.OperatorSet

Specifier = _operators.Specifier


@singledispatch
def operator(functor: str, specifier: Specifier, priority: int) -> Operator:
    return Operator(functor, specifier, priority)


@operator.register
def _(priority: Integer, specifier: Atom, functor: Atom) -> Operator:
    return Operator.fromTerms(priority, specifier, functor)


@operator.register
def _(term: Struct) -> Operator:
    return Operator.fromTerm(term)


def operator_set(*operators) -> OperatorSet:
    return iterable_or_varargs(operators, lambda os: OperatorSet(jiterable(os)))


@singledispatch
def specifier(name: str) -> Specifier:
    return Specifier.valueOf(name.upper())


@specifier.register
def _(term: Term) -> Specifier:
    return Specifier.fromTerm(term)


EMPTY_OPERATORS: OperatorSet = OperatorSet.EMPTY

DEFAULT_OPERATORS: OperatorSet = OperatorSet.DEFAULT

STANDARD_OPERATORS: OperatorSet = OperatorSet.STANDARD

XF: Specifier = Specifier.XF

YF: Specifier = Specifier.YF

FX: Specifier = Specifier.FX

FY: Specifier = Specifier.FY

XFX: Specifier = Specifier.XFX

XFY: Specifier = Specifier.XFY

YFX: Specifier = Specifier.YFX

OperatorSet.__add__ = lambda this, other: this.plus(other)
OperatorSet.__sub__ = lambda this, other: this.minus(other)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.operators.*")
