from collections.abc import Iterable, Mapping
from decimal import Decimal

from jpype import JArray, JClass, JString

from tuprolog.jvmutils import jiterable, jmap
from tuprolog.math import BigDecimal, BigInteger, big_decimal, big_integer
from tuprolog.pyutils import iterable_or_varargs

from ._definitions import (
    DEFAULT_TAGS_FORMATTING_OPTIONS,
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
    TagsFormattingOptions,
    Term,
    TermFormatter,
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
    if isinstance(name, str) and isinstance(arity, int):
        return Indicator.of(name, arity)
    name = atom(name) if isinstance(name, str) else name
    arity = integer(arity) if isinstance(arity, int) else arity
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


def _operators_or_default(operators):
    # tuprolog.core.operators depends on tuprolog.core: the JVM class is looked up lazily
    if operators is None:
        return JClass("it.unibo.tuprolog.core.operators.OperatorSet").DEFAULT
    return operators


def canonical_formatter() -> TermFormatter:
    return TermFormatter.canonical()


def _showing_tags(tags: TagsFormattingOptions) -> TagsFormattingOptions:
    return tags.copy(
        True,
        tags.getDelimiters(),
        tags.getSeparator(),
        tags.getShowKeys(),
        tags.getShowDelimitersIfEmpty(),
        tags.getKeyFilter(),
        tags.getTagFormatter(),
    )


def default_formatter(operators=None, tags: TagsFormattingOptions | None = None) -> TermFormatter:
    # unlike the other factories, 2P-Kt's TermFormatter.default shows tags by default
    if tags is None:
        tags = _showing_tags(DEFAULT_TAGS_FORMATTING_OPTIONS)
    return TermFormatter.default(_operators_or_default(operators), tags)


def readable_formatter(
    operators=None, tags: TagsFormattingOptions = DEFAULT_TAGS_FORMATTING_OPTIONS
) -> TermFormatter:
    return TermFormatter.readable(_operators_or_default(operators), tags)


def pretty_variables_formatter(
    tags: TagsFormattingOptions = DEFAULT_TAGS_FORMATTING_OPTIONS,
) -> TermFormatter:
    return TermFormatter.prettyVariables(tags)


def pretty_expressions_formatter(
    pretty_variables: bool = True,
    operators=None,
    tags: TagsFormattingOptions = DEFAULT_TAGS_FORMATTING_OPTIONS,
) -> TermFormatter:
    return TermFormatter.prettyExpressions(pretty_variables, _operators_or_default(operators), tags)
