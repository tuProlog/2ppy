import logging
import jpype
import jpype.imports

from it.unibo.tuprolog.core.operators import Operator
from it.unibo.tuprolog.core.operators import OperatorSet
from it.unibo.tuprolog.core.operators import Specifier

from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap
from tuprolog.core import Atom
from tuprolog.core import Integer
from tuprolog.core import Struct

from functools import singledispatch

logging.debug("Loaded JVM classes from it.unibo.tuprolog.core.operators.*")


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

def specifier(name: str) -> Specifier:
    return Specifier.valueOf(name)

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
