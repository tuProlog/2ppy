from collections.abc import Iterable, Mapping
from decimal import Decimal

from jpype import JArray, JString

from tuprolog.jvmutils import jiterable, jmap
from tuprolog.math import BigDecimal, BigInteger, big_decimal, big_integer
from tuprolog.pyutils import iterable_or_varargs

from ._definitions import (
    Atom,
    Block,
    Clause,
    Cons,
    Directive,
    EmptyBlock,
    EmptyList,
    Fact,
    Indicator,
    Integer,
    List,
    Numeric,
    Real,
    Rule,
    Scope,
    Struct,
    Substitution,
    Term,
    Truth,
    Tuple,
    Var,
)


def atom(string: str) -> Atom:
    return Atom.of(string)


def block(*terms: Term | Iterable[Term]) -> Block:
    return iterable_or_varargs(terms, lambda ts: Block.of(jiterable(ts)))


def clause(head: Term = None, *body: Term | Iterable[Term]):
    return iterable_or_varargs(body, lambda bs: Clause.of(head, jiterable(bs)))


def empty_logic_list() -> EmptyList:
    return EmptyList.getInstance()


def cons(head: Term, tail: Term = None) -> Cons:
    if tail is None:
        return Cons.singleton(head)
    else:
        return Cons.of(head, tail)


def directive(*goals: Term | Iterable[Term]) -> Directive:
    return iterable_or_varargs(goals, lambda gs: Directive.of(jiterable(gs)))


def empty_block() -> Block:
    return EmptyBlock.getInstance()


def fact(struct: Term | Iterable[Term]) -> Fact:
    return Fact.of(struct)


def indicator(name: str | Term, arity: int | Term) -> Indicator:
    return Indicator.of(name, arity)


def integer(value: int | BigInteger | str) -> Integer:
    return Integer.of(big_integer(value))


def real(value: float | BigDecimal | str | Decimal) -> Real:
    if isinstance(value, BigDecimal):
        return Real.of(value)
    return Real.of(big_decimal(value))


def numeric(value: BigInteger | BigDecimal | str | float | Decimal) -> Numeric:
    if isinstance(value, str):
        return Numeric.of(JString @ value)
    if isinstance(value, (int, BigInteger)):
        return integer(value)
    return real(value)


def rule(head: Struct, *body: Term | Iterable[Term]) -> Rule:
    return iterable_or_varargs(body, lambda bs: Rule.of(head, jiterable(bs)))


def struct(functor: str, *args: Term | Iterable[Term]) -> Struct:
    return iterable_or_varargs(args, lambda xs: Struct.of(functor, jiterable(xs)))


def truth(boolean: bool) -> Truth:
    return Truth.of(boolean)


def logic_list(*items: Term | Iterable[Term]) -> List:
    return iterable_or_varargs(items, lambda xs: List.of(jiterable(xs)))


def logic_list_from(items: Iterable[Term], last: Term = None) -> List:
    return List.from_(jiterable(items), last)


def logic_tuple(first: Term, second: Term, *others: Term | Iterable[Term]) -> Tuple:
    return iterable_or_varargs(others, lambda os: Tuple.of(jiterable([first, second] + list(os))))


def var(name: str) -> Var:
    return Var.of(name)


def unifier(assignments: Mapping[Var, Term] | None = None) -> Substitution.Unifier:
    return Substitution.unifier(jmap(assignments or {}))


def substitution(assignments: Mapping[Var, Term] | None = None) -> Substitution:
    return Substitution.of(jmap(assignments or {}))


def failed() -> Substitution.Fail:
    return Substitution.failed()


EMPTY_UNIFIER: Substitution.Unifier = substitution()


FAILED_SUBSTITUTION: Substitution.Fail = failed()


def scope(*variables: Var | str) -> Scope:
    if len(variables) == 0:
        return Scope.empty()
    vars = [var(v) if isinstance(v, str) else v for v in variables]
    return Scope.of(vars[0], JArray(Var) @ vars[1:])


def variables(*names: str) -> tuple[Var]:
    assert len(names) > 0
    return tuple(var(n) for n in names)
