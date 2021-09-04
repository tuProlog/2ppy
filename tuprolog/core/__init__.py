import logging
import jpype
import jpype.imports

from it.unibo.tuprolog.core import Atom
from it.unibo.tuprolog.core import Block
from it.unibo.tuprolog.core import Clause
from it.unibo.tuprolog.core import Cons
from it.unibo.tuprolog.core import Constant
from it.unibo.tuprolog.core import Directive
from it.unibo.tuprolog.core import Empty
from it.unibo.tuprolog.core import EmptyBlock
from it.unibo.tuprolog.core import EmptyList
from it.unibo.tuprolog.core import Fact
from it.unibo.tuprolog.core import Formatter
from it.unibo.tuprolog.core import Indicator
from it.unibo.tuprolog.core import Integer
from it.unibo.tuprolog.core import List
from it.unibo.tuprolog.core import Numeric
from it.unibo.tuprolog.core import Real
from it.unibo.tuprolog.core import Recursive
from it.unibo.tuprolog.core import Rule
from it.unibo.tuprolog.core import Scope
from it.unibo.tuprolog.core import Struct
from it.unibo.tuprolog.core import Substitution
from it.unibo.tuprolog.core import Term
from it.unibo.tuprolog.core import TermComparator
from it.unibo.tuprolog.core import TermConvertible
from it.unibo.tuprolog.core import TermFormatter
from it.unibo.tuprolog.core import Terms
from it.unibo.tuprolog.core import TermVisitor
from it.unibo.tuprolog.core import Truth
from it.unibo.tuprolog.core import Tuple
from it.unibo.tuprolog.core import Var

from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap

from typing import Iterable, Union, Dict


logging.debug("Loaded JVM classes from it.unibo.tuprolog.core.*")


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
    return Integer.of(value)


def real(value: Union[float, str]) -> Real:
    return Real.of(value)


def rule(head: Struct, *body: Union[Term, Iterable[Term]]) -> Rule:
    return iterable_or_varargs(body, lambda bs: Rule.of(head, jiterable(bs)))


def struct(functor: str, *args: Union[Term, Iterable[Term]]) -> Struct:
    return iterable_or_varargs(args, lambda xs: Struct.of(functor, jiterable(xs)))


def truth(boolean: bool) -> Truth:
    return Truth.of(boolean)


TRUE = Truth.TRUE


FALSE = Truth.FALSE


FAIL = Truth.FAIL


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


Term.__lt__ = lambda this, other: this.compareTo(other) < 0
Term.__gt__ = lambda this, other: this.compareTo(other) > 0
Term.__le__ = lambda this, other: this.compareTo(other) <= 0
Term.__ge__ = lambda this, other: this.compareTo(other) >= 0
Term.__getitem__ = lambda this, item, *items: this.get(item, *items)
