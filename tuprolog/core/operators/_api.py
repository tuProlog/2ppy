from functools import singledispatch
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.core import Atom, Integer, Struct, Term
from ._definitions import Operator, OperatorSet, Specifier


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
