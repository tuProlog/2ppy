import logging
import jpype
import jpype.imports

from functools import singledispatch

from it.unibo.tuprolog.core.operators import Operator
from it.unibo.tuprolog.core.operators import OperatorSet
from it.unibo.tuprolog.core.operators import Specifier

from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap
from tuprolog.core import Atom
from tuprolog.core import Integer
from tuprolog.core import Struct

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

XF = Specifier.XF

YF = Specifier.YF

FX = Specifier.FX

FY = Specifier.FY

XFX = Specifier.XFX

XFY = Specifier.XFY

YFX = Specifier.YFX
