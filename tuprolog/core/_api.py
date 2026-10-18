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

__all__ = [
    "EMPTY_UNIFIER",
    "FAILED_SUBSTITUTION",
    "atom",
    "block",
    "canonical_formatter",
    "clause",
    "cons",
    "default_formatter",
    "directive",
    "empty_block",
    "empty_logic_list",
    "fact",
    "failed",
    "indicator",
    "integer",
    "logic_list",
    "logic_list_from",
    "logic_tuple",
    "numeric",
    "pretty_expressions_formatter",
    "pretty_variables_formatter",
    "readable_formatter",
    "real",
    "rule",
    "scope",
    "struct",
    "substitution",
    "to_python",
    "to_term",
    "truth",
    "unifier",
    "var",
    "variables",
]


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


def to_term(value: Term | str | bool | float | Decimal | list | tuple) -> Term:
    """Converts a Python value into a term: strings become atoms, numbers numerics, booleans
    truths (true/false), lists logic lists, and tuples logic tuples (i.e. `(a, b)`, where a
    trailing nested tuple flattens, as `(a, (b, c))` is `(a, b, c)`); terms are returned as they
    are. `to_python` is its inverse."""
    if isinstance(value, Term):
        return value
    if isinstance(value, (str, JString)):
        return atom(value)
    if isinstance(value, bool):
        return truth(value)
    if isinstance(value, (int, float, Decimal, BigInteger, BigDecimal)):
        return numeric(value)
    if isinstance(value, list):
        return logic_list(value)
    if isinstance(value, tuple) and value:
        return to_term(value[0]) if len(value) == 1 else logic_tuple(*value)
    raise TypeError(f"Cannot convert {type(value).__name__} into a term: {value!r}")


def to_python(term: Term):
    """Converts a term into a Python value, as the inverse of `to_term`: truths become booleans,
    integers ints, reals floats, atoms strings, well-formed lists lists, and tuples tuples.
    Other terms (e.g. variables, compound terms, partial lists) are returned as they are."""
    if isinstance(term, Truth):
        return bool(term.isTrue())
    if isinstance(term, Integer):
        return term.to_int()
    if isinstance(term, Real):
        return term.to_float()
    if isinstance(term, List):
        return [to_python(item) for item in term] if term.isWellFormed() else term
    if isinstance(term, Tuple):
        return tuple(to_python(item) for item in term.unfolded)
    if isinstance(term, Atom):
        return str(term.getValue())
    return term


def _terms(values: Iterable) -> list[Term]:
    return [to_term(v) for v in values]


def rule(head: Struct, *body: Term | Iterable[Term]) -> Rule:
    return iterable_or_varargs(body, lambda bs: Rule.of(head, jiterable(bs)))


def struct(functor: str, *args: Term | Iterable[Term]) -> Struct:
    return iterable_or_varargs(args, lambda xs: Struct.of(functor, jiterable(_terms(xs))))


def truth(boolean: bool) -> Truth:
    return Truth.of(boolean)


def logic_list(*items: Term | Iterable[Term]) -> List:
    return iterable_or_varargs(items, lambda xs: List.of(jiterable(_terms(xs))))


def logic_list_from(items: Iterable[Term], last: Term = None) -> List:
    return List.from_(jiterable(_terms(items)), None if last is None else to_term(last))


def logic_tuple(first: Term, second: Term, *others: Term | Iterable[Term]) -> Tuple:
    return iterable_or_varargs(others, lambda os: Tuple.of(jiterable(_terms([first, second, *os]))))


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
