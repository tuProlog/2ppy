from typing import Iterable, Dict, Tuple as PyTuple, Union
from decimal import Decimal
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap
from tuprolog.math import big_integer, big_decimal, BigInteger, BigDecimal
from ._definitions import *


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
