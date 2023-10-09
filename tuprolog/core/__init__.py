from typing import Iterable, Dict, Tuple as PyTuple, Union
from decimal import Decimal
from jpype import JImplements, JOverride
from tuprolog import logger
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap
from ._ktadapt import *
from ._ktmath import *
import jpype.imports
import it.unibo.tuprolog.core as _core # type: ignore


Applicable = _core.Applicable

Atom = _core.Atom

Block = _core.Block

Clause = _core.Clause

Cons = _core.Cons

Constant = _core.Constant

Directive = _core.Directive

Empty = _core.Empty

EmptyBlock = _core.EmptyBlock

EmptyList = _core.EmptyList

Fact = _core.Fact

Formatter = _core.Formatter

Indicator = _core.Indicator

Integer = _core.Integer

List = _core.List

Numeric = _core.Numeric

Real = _core.Real

Recursive = _core.Recursive

Rule = _core.Rule

Scope = _core.Scope

Struct = _core.Struct

Substitution = _core.Substitution

Term = _core.Term

TermComparator = _core.TermComparator

TermConvertible = _core.TermConvertible

TermFormatter = _core.TermFormatter

Terms = _core.Terms

TermVisitor = _core.TermVisitor

Truth = _core.Truth

Tuple = _core.Tuple

Var = _core.Var

Variabled = _core.Variabled


@JImplements(TermConvertible)
class AbstractTermConvertible(object):
    @JOverride
    def toTerm(self):
        raise NotImplementedError()


def atom(string: str) -> Atom:
    return Atom.of(string)


def block(*terms: Union[Term, Iterable[Term]]) -> Block:
    return iterable_or_varargs(terms, lambda ts: Block.of(jiterable(ts)))


def clause(head: Term = None, *body: Union[Term, Iterable[Term]]):
    return iterable_or_varargs(body, lambda bs: Clause.of(head, jiterable(bs)))


def empty_logic_list() -> EmptyList:
    return EmptyList.getInstance()


def cons(head: Term, tail: Term = None) -> Cons:
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


def integer(value: Union[int, BigInteger, str]) -> Integer:
    return Integer.of(big_integer(value))


def real(value: Union[float, BigDecimal, str, Decimal]) -> Real:
    if isinstance(value, BigDecimal):
        return Real.of(value)
    return Real.of(big_decimal(value))


def numeric(value: Union[int, BigInteger, BigDecimal, str, float, Decimal]) -> Numeric:
    if isinstance(value, str):
        return Numeric.of(jpype.JString @ value)
    if isinstance(value, int) or isinstance(value, BigInteger):
        return integer(value)
    return real(value)


def rule(head: Struct, *body: Union[Term, Iterable[Term]]) -> Rule:
    return iterable_or_varargs(body, lambda bs: Rule.of(head, jiterable(bs)))


def struct(functor: str, *args: Union[Term, Iterable[Term]]) -> Struct:
    return iterable_or_varargs(args, lambda xs: Struct.of(functor, jiterable(xs)))


def truth(boolean: bool) -> Truth:
    return Truth.of(boolean)


TRUE = Truth.TRUE

FALSE = Truth.FALSE

FAIL = Truth.FAIL


def logic_list(*items: Union[Term, Iterable[Term]]) -> List:
    return iterable_or_varargs(items, lambda xs: List.of(jiterable(xs)))


def logic_list_from(items: Iterable[Term], last: Term = None) -> List:
    return List.from_(jiterable(items), last)


def logic_tuple(first: Term, second: Term, *others: Union[Term, Iterable[Term]]) -> Tuple:
    return iterable_or_varargs(others, lambda os: Tuple.of(jiterable([first, second] + list(os))))


def var(name: str) -> Var:
    return Var.of(name)


def unifier(assignments: Dict[Var, Term] = {}) -> Substitution.Unifier:
    return Substitution.unifier(jmap(assignments))


def substitution(assignments: Dict[Var, Term] = {}) -> Substitution:
    return Substitution.of(jmap(assignments))


def failed() -> Substitution.Fail:
    return Substitution.failed()


EMPTY_UNIFIER: Substitution.Unifier = substitution()

FAILED_SUBSTITUTION: Substitution.Fail = failed()


def scope(*variables: Union[Var, str]) -> Scope:
    if len(variables) == 0:
        return Scope.empty()
    vars = [var(v) if isinstance(v, str) else v for v in variables]
    return Scope.of(vars[0], jpype.JArray(Var) @ vars[1:])


def variables(*names: str) -> PyTuple[Var]:
    assert len(names) > 0
    return tuple((var(n) for n in names))


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.*")
