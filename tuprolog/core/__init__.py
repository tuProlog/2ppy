from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

from ._ktadapt import *

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Atom
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Block
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Clause
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Cons
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Constant
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Directive
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Empty
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import EmptyBlock
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import EmptyList
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Fact
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Formatter
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Indicator
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Integer
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import List
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Numeric
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Real
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Recursive
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Rule
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Scope
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Struct
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Substitution
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Term
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import TermComparator
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import TermConvertible
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import TermFormatter
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Terms
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import TermVisitor
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Truth
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Tuple
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.core import Var

from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap

from typing import Iterable, Union, Dict


@jpype.JImplements(TermConvertible)
class AbstractTermConvertible(object):
    @jpype.JOverride
    def toTerm(self):
        raise NotImplementedError()


def atom(string: str) -> Atom:
    return Atom.of(string)


def block(*terms: Union[Term, Iterable[Term]]) -> Block:
    return iterable_or_varargs(terms, lambda ts: Block.of(jiterable(ts)))


def clause(head: Term=None, *body: Union[Term, Iterable[Term]]):
    return iterable_or_varargs(body, lambda bs: Clause.of(head, jiterable(bs)))


def empty_logic_list() -> EmptyList:
    return EmptyList.getInstance()


def cons(head: Term, tail: Term=None) -> Cons:
    if tail is None:
        return Cons.singleton(head)
    else: 
        return Cons.of(head, tail)


def directive(*goals: Union[Term, Iterable[Term]]) -> Directive:
    return iterable_or_varargs(goals, lambda gs: Directive.of(jiterable(gs)))


def empty_block() -> Block:
    return EmptyBlock.getInstance()


def fact(struct: Union[Term, Iterable[Term]]) -> Fact:
    return Fact.of(struct)


def indicator(name: Union[str, Term], arity: Union[int, Term]) -> Indicator:
    return Indicator.of(name, arity)


def integer(value: Union[int, str]) -> Integer:
    if isinstance(value, str):
        return Integer.of(jpype.JString @ value)
    else:
        return Integer.of(jpype.JLong @ value)


def real(value: Union[float, str]) -> Real:
    if isinstance(value, str):
        return Real.of(jpype.JString @ value)
    else:
        return Real.of(jpype.JDouble @ value)


def rule(head: Struct, *body: Union[Term, Iterable[Term]]) -> Rule:
    return iterable_or_varargs(body, lambda bs: Rule.of(head, jiterable(bs)))


def struct(functor: str, *args: Union[Term, Iterable[Term]]) -> Struct:
    return iterable_or_varargs(args, lambda xs: Struct.of(functor, jiterable(xs)))


def truth(boolean: bool) -> Truth:
    return Truth.of(boolean)


TRUE = Truth.TRUE


FALSE = Truth.FALSE


FAIL = Truth.FAIL


def logic_list(*items: Union[Term, Iterable[Term]]) -> Tuple:
    return iterable_or_varargs(items, lambda xs: List.of(jiterable(xs)))


def logic_tuple(first: Term, second: Term, *others: Union[Term, Iterable[Term]]) -> Tuple:
    return iterable_or_varargs(others, lambda os: Tuple.of(jiterable([first, second] + list(os))))


def var(name: str) -> Var:
    return Var.of(name)


def unifier(assignments: Dict[Var, Term]={}) -> Substitution.Unifier:
    return Substitution.unifier(jmap(assignments))


def substitution(assignments: Dict[Var, Term]={}) -> Substitution:
    return Substitution.of(jmap(assignments))


def failed() -> Substitution.Fail:
    return Substitution.failed()


EMPTY_UNIFIER: Substitution.Unifier = substitution()

FAILED_SUBSTITUTION: Substitution.Fail = failed()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.*")
