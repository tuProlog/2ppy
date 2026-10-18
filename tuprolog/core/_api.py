from collections.abc import Iterable, Mapping
from decimal import Decimal
from typing import Any

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
    """Creates an atom, i.e. a constant symbolic name.

    Args:
        string: the name of the atom, e.g. `"bart"`. The names `"[]"`, `"{}"`, `"true"`, `"false"`
            and `"fail"` give the corresponding special atoms (`tuprolog.core.EmptyList`,
            `tuprolog.core.EmptyBlock`, `tuprolog.core.Truth`).

    Returns:
        The atom.

    Examples:
        >>> atom("bart"), atom("Hello World"), atom("[]").is_empty_list
        (bart, 'Hello World', True)

    Note:
        Wraps 2P-Kt's `Atom.of`.
    """
    return Atom.of(string)


def block(*terms: Term | Iterable[Term]) -> Block:
    """Creates a block, i.e. a curly-braced term such as `{a, b}`.

    Args:
        *terms: the terms in the block (terms, not Python values), either as many arguments or as a
            single iterable. No terms give the empty block `{}`.

    Returns:
        The block.

    Examples:
        >>> block(atom("a"), atom("b")), block([atom("a")]), block()
        ({a, b}, {a}, {})

    Note:
        Wraps 2P-Kt's `Block.of`.
    """
    return iterable_or_varargs(terms, lambda ts: Block.of(jiterable(ts)))


def clause(head: Term | None = None, *body: Term | Iterable[Term]) -> Clause:
    """Creates a clause: a rule (`head :- body`), a fact, or a directive (`:- body`).

    Args:
        head: the head of the clause (a structure or an atom), or `None` for a directive.
        *body: the goals of the body (terms), either as many arguments or as a single iterable; many
            goals are joined in a conjunction. No goals give a fact (with a head) or an error
            (without a head).

    Returns:
        The clause: a `tuprolog.core.Rule` (a `tuprolog.core.Fact` when the body is empty or
        `true`), or a `tuprolog.core.Directive` when `head` is `None`.

    Raises:
        java.lang.IllegalArgumentException: if both the head and the body are missing.

    Examples:
        >>> clause(struct("p"), atom("q"), atom("r"))
        p :- (q, r)
        >>> clause(struct("p")), clause(None, atom("q"))
        (p :- true, :- q)

    Note:
        Wraps 2P-Kt's `Clause.of`.
    """
    return iterable_or_varargs(body, lambda bs: Clause.of(head, jiterable(bs)))


def empty_logic_list() -> EmptyList:
    """Returns the empty list `[]`.

    Returns:
        The empty list, a singleton.

    Examples:
        >>> empty_logic_list(), empty_logic_list().is_empty_list
        ([], True)
    """
    return EmptyList.getInstance()


def cons(head: Term, tail: Term | None = None) -> Cons:
    """Creates a list cell, i.e. the list `[head | tail]`.

    Args:
        head: the first item (a term).
        tail: the rest of the list (a term, usually a list or a variable). If `None`, the list
            `[head]`.

    Returns:
        The list cell.

    Examples:
        >>> cons(atom("a")), cons(atom("a"), logic_list("b")), cons(atom("a"), var("T"))
        ([a], [a, b], [a | T_...])

    Note:
        Wraps 2P-Kt's `Cons.of` and `Cons.singleton`.
    """
    if tail is None:
        return Cons.singleton(head)
    else:
        return Cons.of(head, tail)


def directive(*goals: Term | Iterable[Term]) -> Directive:
    """Creates a directive, i.e. a clause without head, `:- goal1, ..., goalN`.

    Args:
        *goals: the goals (terms), either as many arguments or as a single iterable: at least one.

    Returns:
        The directive.

    Examples:
        >>> directive(struct("dynamic", indicator("counter", 1)))
        :- dynamic(counter/1)

    Note:
        Wraps 2P-Kt's `Directive.of`.
    """
    return iterable_or_varargs(goals, lambda gs: Directive.of(jiterable(gs)))


def empty_block() -> Block:
    """Returns the empty block `{}`.

    Returns:
        The empty block, a singleton.

    Examples:
        >>> empty_block(), empty_block().is_empty_block
        ({}, True)
    """
    return EmptyBlock.getInstance()


def fact(struct: Term) -> Fact:
    """Creates a fact, i.e. a clause `head :- true`, stating that `head` holds unconditionally.

    Args:
        struct: the head of the fact (a structure or an atom).

    Returns:
        The fact.

    Examples:
        >>> fact(struct("parent", "homer", "bart"))
        parent(homer, bart) :- true

    Note:
        Wraps 2P-Kt's `Fact.of`.
    """
    return Fact.of(struct)


def indicator(name: str | Term, arity: int | Term) -> Indicator:
    """Creates an indicator, `name/arity`, identifying a predicate or a functor.

    Args:
        name: the name, as a string or a term (usually an atom; a variable for patterns).
        arity: the number of arguments, as an int or a term (usually an integer; a variable for
            patterns).

    Returns:
        The indicator.

    Examples:
        >>> indicator("parent", 2), indicator(atom("parent"), integer(2))
        (parent/2, parent/2)

    Note:
        Wraps 2P-Kt's `Indicator.of`.
    """
    if isinstance(name, str) and isinstance(arity, int):
        return Indicator.of(name, arity)
    name = atom(name) if isinstance(name, str) else name
    arity = integer(arity) if isinstance(arity, int) else arity
    return Indicator.of(name, arity)


def integer(value: int | BigInteger | str) -> Integer:
    """Creates an integer number, of arbitrary precision.

    Args:
        value: the value, as a Python `int` (booleans count as 0 and 1), a
            `tuprolog.math.BigInteger`, or a string of digits (e.g. `"42"`, or `"0x1F"` in
            hexadecimal).

    Returns:
        The integer.

    Raises:
        TypeError: if `value` has another type (e.g. a `float`).

    Examples:
        >>> integer(42), integer("123456789012345678901234567890"), integer("0x1F")
        (42, 123456789012345678901234567890, 31)

    Note:
        Wraps 2P-Kt's `Integer.of`.
    """
    return Integer.of(big_integer(value))


def real(value: float | BigDecimal | str | Decimal) -> Real:
    """Creates a real number, of arbitrary precision.

    Args:
        value: the value, as a Python `float` (its shortest representation is kept, e.g. `0.1` stays
            `0.1`), a `decimal.Decimal`, a string (e.g. `"3.14"`, `"1e3"`), a Python `int`, or a
            `tuprolog.math.BigDecimal`.

    Returns:
        The real.

    Examples:
        >>> real(0.1), real("3.14"), real(1), real(Decimal("2.50"))
        (0.1, 3.14, 1.0, 2.5)

    Note:
        Wraps 2P-Kt's `Real.of`; see `tuprolog.math.big_decimal` for the conversion.
    """
    if isinstance(value, BigDecimal):
        return Real.of(value)
    if isinstance(value, float):  # its shortest repr, e.g. 0.1, which converts back to it exactly
        value = repr(value)
    return Real.of(big_decimal(value))


def numeric(value: BigInteger | BigDecimal | str | float | Decimal) -> Numeric:
    """Creates a number, integer or real depending on `value`.

    Args:
        value: the value. Python `int`s (and `tuprolog.math.BigInteger`s) give integers; `float`s,
            `decimal.Decimal`s (and `tuprolog.math.BigDecimal`s) give reals; strings are parsed,
            giving an integer or a real by their syntax.

    Returns:
        The number, a `tuprolog.core.Integer` or a `tuprolog.core.Real`.

    Raises:
        java.lang.NumberFormatException: if `value` is a string not representing a number.

    Examples:
        >>> numeric(3), numeric(1.5), numeric("2"), numeric("2.5")
        (3, 1.5, 2, 2.5)
        >>> numeric("2").is_integer, numeric("2.5").is_real
        (True, True)
        >>> numeric("1e3")  # reals are normalized as by `real`
        1000.0

    Note:
        Wraps 2P-Kt's `Numeric.of`.
    """
    if isinstance(value, str):
        number = Numeric.of(JString @ value)
        # a real from a string skips big_decimal's normalization: e.g. 1e3 would format as 1E+3.0
        return real(value) if isinstance(number, Real) else number
    if isinstance(value, (int, BigInteger)):
        return integer(value)
    return real(value)


def to_term(value: Term | str | bool | float | Decimal | list | tuple) -> Term:
    """Converts a Python value into a term.

    Strings become atoms, booleans truths (`true`/`false`), `int`s integers, `float`s and
    `decimal.Decimal`s reals, lists logic lists, and tuples logic tuples (i.e. conjunctions
    `(a, b)`, where a trailing nested tuple flattens, as `(a, (b, c))` is `(a, b, c)`; a 1-tuple
    gives its item). The items of lists and tuples are converted as well; terms are returned as
    they are. `to_python` is its inverse.

    Args:
        value: the value to convert.

    Returns:
        The term.

    Raises:
        TypeError: if `value` cannot be converted (e.g. `None`, a dict, or the empty tuple).

    Examples:
        >>> to_term("bart"), to_term(True), to_term(42), to_term(2.5)
        (bart, true, 42, 2.5)
        >>> to_term([1, "a", (2, 3)])
        [1, a, (2, 3)]
    """
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


def to_python(term: Term) -> Any:
    """Converts a term into a Python value, as the inverse of `to_term`.

    Truths become booleans (`fail` too becomes `False`), integers `int`s, reals `float`s (possibly
    losing precision), atoms strings (`[]` gives the empty list, being a list), well-formed lists
    lists, and tuples tuples, converting their items as well. Other terms (e.g. variables, compound
    terms, partial lists) are returned as they are.

    Args:
        term: the term to convert.

    Returns:
        The Python value, or `term` itself when it has no Python counterpart.

    Examples:
        >>> to_python(logic_list(1, 2.5, "a", truth(True)))
        [1, 2.5, 'a', True]
        >>> to_python(logic_tuple(1, 2)), to_python(struct("f", "a"))
        ((1, 2), f(a))
    """
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
    """Creates a rule, `head :- body`, i.e. "`head` holds if `body` does".

    Args:
        head: the head (a structure or an atom).
        *body: the goals of the body (terms), either as many arguments or as a single iterable; many
            goals are joined in a conjunction. No goals, or just `true`, give a fact.

    Returns:
        The rule (a `tuprolog.core.Fact` when the body is empty or `true`).

    Examples:
        >>> X, Y, Z = variables("X", "Y", "Z")
        >>> rule(struct("grandparent", X, Z), struct("parent", X, Y), struct("parent", Y, Z))
        grandparent(X_..., Z_...) :- (parent(X_..., Y_...), parent(Y_..., Z_...))
        >>> rule(struct("p")).is_fact
        True

    Note:
        Wraps 2P-Kt's `Rule.of`.
    """
    return iterable_or_varargs(body, lambda bs: Rule.of(head, jiterable(bs)))


def struct(functor: str, *args: Term | Iterable[Term]) -> Struct:
    """Creates a structure, i.e. a compound term `functor(arg1, ..., argN)`.

    The arguments are converted with `to_term`, so Python values are accepted. Structures with a
    dedicated type come out with that type, e.g. `struct(",", "a", "b")` is a `tuprolog.core.Tuple`
    and `struct("f")` is the atom `f`.

    Args:
        functor: the name of the structure.
        *args: the arguments, either as many arguments or as a single iterable (a list is unpacked:
            wrap it, as in `struct("f", [[1, 2]])`, to pass a logic list as the only argument).

    Returns:
        The structure.

    Examples:
        >>> struct("parent", "homer", "bart"), struct("f", 1, 2.5, var("X"))
        (parent(homer, bart), f(1, 2.5, X_...))
        >>> struct("f", ["a", "b"]), struct("f", [["a", "b"]])
        (f(a, b), f([a, b]))

    Note:
        Wraps 2P-Kt's `Struct.of`.
    """
    return iterable_or_varargs(args, lambda xs: Struct.of(functor, jiterable(_terms(xs))))


def truth(boolean: bool) -> Truth:
    """Creates a truth value, i.e. the atom `true` or `false`.

    Args:
        boolean: the truth value (any truthy or falsy value).

    Returns:
        `tuprolog.core.TRUE` or `tuprolog.core.FALSE`.

    Examples:
        >>> truth(True), truth(False)
        (true, false)

    Note:
        Wraps 2P-Kt's `Truth.of`.
    """
    return Truth.of(boolean)


def logic_list(*items: Term | Iterable[Term]) -> List:
    """Creates a well-formed logic list, e.g. `[1, 2, 3]`.

    The items are converted with `to_term`, so Python values are accepted.

    Args:
        *items: the items, either as many arguments or as a single iterable. No items give `[]`.

    Returns:
        The list.

    Examples:
        >>> logic_list(1, 2, 3), logic_list(["a", "b"]), logic_list()
        ([1, 2, 3], [a, b], [])

    Note:
        Wraps 2P-Kt's `List.of`.
    """
    return iterable_or_varargs(items, lambda xs: List.of(jiterable(_terms(xs))))


def logic_list_from(items: Iterable[Term], last: Term | None = None) -> List:
    """Creates a logic list from an iterable, ending with a given tail rather than `[]`.

    The items (and `last`) are converted with `to_term`, so Python values are accepted. Use
    `logic_list` for well-formed lists.

    Args:
        items: the items.
        last: the final tail, giving the list `[item1, ..., itemN | last]` (e.g. a partial list,
            when `last` is a variable, or a well-formed list, when `last` is `[]`). If `None`, the
            last item is the final tail, i.e. the list is `[item1, ..., itemN-1 | itemN]`.

    Returns:
        The list.

    Examples:
        >>> logic_list_from([1, 2], last=var("T")), logic_list_from([1, 2], last=empty_logic_list())
        ([1, 2 | T_...], [1, 2])
        >>> logic_list_from([1, logic_list(2, 3)])
        [1, 2, 3]

    Note:
        Wraps 2P-Kt's `List.from`.
    """
    return List.from_(jiterable(_terms(items)), None if last is None else to_term(last))


def logic_tuple(first: Term, second: Term, *others: Term | Iterable[Term]) -> Tuple:
    """Creates a logic tuple, i.e. a conjunction `(first, second, ...)`.

    The items are converted with `to_term`, so Python values are accepted. A last item that is a
    tuple flattens, as `(a, (b, c))` is `(a, b, c)`.

    Args:
        first: the first item.
        second: the second item.
        *others: the other items, either as many arguments or as a single iterable.

    Returns:
        The tuple.

    Examples:
        >>> logic_tuple(1, 2, 3), logic_tuple("a", "b", ["c", "d"])
        ((1, 2, 3), (a, b, c, d))

    Note:
        Wraps 2P-Kt's `Tuple.of`.
    """
    return iterable_or_varargs(others, lambda os: Tuple.of(jiterable(_terms([first, second, *os]))))


def var(name: str) -> Var:
    """Creates a new logic variable.

    Each call creates a different variable, even with the same name: its complete name (e.g. `X_0`)
    adds a unique number to `name`. Reuse the returned object (or a `scope`) wherever the variable
    must occur more than once.

    Args:
        name: the name of the variable, e.g. `"X"`; `"_"` gives an anonymous variable. Names that
            are not valid Prolog variable names (e.g. lowercase) are printed between backticks.

    Returns:
        The variable.

    Examples:
        >>> X = var("X")
        >>> X.name, X == X, X == var("X")
        ('X', True, False)

    Note:
        Wraps 2P-Kt's `Var.of`.
    """
    return Var.of(name)


def unifier(assignments: Mapping[Var, Term] | None = None) -> Substitution.Unifier:
    """Creates a unifier, i.e. a successful substitution, from variable-term assignments.

    Args:
        assignments: a mapping from variables to terms (terms, not Python values). If `None`, the
            empty unifier.

    Returns:
        The unifier.

    Examples:
        >>> X = var("X")
        >>> unifier({X: atom("a")})[X], unifier()
        (a, {})

    Note:
        Wraps 2P-Kt's `Substitution.unifier`.
    """
    return Substitution.unifier(jmap(assignments or {}))


def substitution(assignments: Mapping[Var, Term] | None = None) -> Substitution:
    """Creates a substitution from variable-term assignments.

    Unlike `unifier`, the assignments are checked: variables assigned to other assigned variables
    are resolved, and contradicting assignments give the failed substitution.

    Args:
        assignments: a mapping from variables to terms (terms, not Python values). If `None`, the
            empty substitution.

    Returns:
        The substitution: a `tuprolog.core.Substitution.Unifier`, or a
        `tuprolog.core.Substitution.Fail`.

    Examples:
        >>> X, Y = var("X"), var("Y")
        >>> s = substitution({X: atom("a"), Y: X})
        >>> s[Y], s.is_success
        (a, True)

    Note:
        Wraps 2P-Kt's `Substitution.of`.
    """
    return Substitution.of(jmap(assignments or {}))


def failed() -> Substitution.Fail:
    """Returns the failed substitution, meaning that no assignment of variables exists.

    Returns:
        The failed substitution, a singleton (also `tuprolog.core.FAILED_SUBSTITUTION`).

    Examples:
        >>> failed(), failed().is_failed
        ({Failed Substitution}, True)

    Note:
        Wraps 2P-Kt's `Substitution.failed`.
    """
    return Substitution.failed()


EMPTY_UNIFIER: Substitution.Unifier = substitution()
"""The empty unifier `{}`, assigning no variables: applying it leaves terms unchanged."""


FAILED_SUBSTITUTION: Substitution.Fail = failed()
"""The failed substitution, meaning that no assignment of variables exists (see `failed`)."""


def scope(*variables: Var | str) -> Scope:
    """Creates a scope, i.e. a factory of terms remembering the variables it creates by name.

    See `tuprolog.core.Scope`.

    Args:
        *variables: the variables the scope starts with, as `Var`s or names (creating new
            variables).

    Returns:
        The scope.

    Examples:
        >>> s = scope("X")
        >>> s.struct("f", s.var("X"), s.var("X"))
        f(X_..., X_...)

    Note:
        Wraps 2P-Kt's `Scope.of` and `Scope.empty`.
    """
    if len(variables) == 0:
        return Scope.empty()
    vars = [var(v) if isinstance(v, str) else v for v in variables]
    return Scope.of(vars[0], JArray(Var) @ vars[1:])


def variables(*names: str) -> tuple[Var]:
    """Creates many new logic variables at once (see `var`).

    Args:
        *names: the names of the variables: at least one.

    Returns:
        A tuple of the variables, in the order of `names`.

    Raises:
        AssertionError: if no names are given.

    Examples:
        >>> X, Y = variables("X", "Y")
        >>> X.name, Y.name
        ('X', 'Y')
    """
    assert len(names) > 0
    return tuple(var(n) for n in names)


def _operators_or_default(operators: Any) -> Any:
    # tuprolog.core.operators depends on tuprolog.core: the JVM class is looked up lazily
    if operators is None:
        return JClass("it.unibo.tuprolog.core.operators.OperatorSet").DEFAULT
    return operators


def canonical_formatter() -> TermFormatter:
    """Creates a formatter rendering terms in canonical form, ignoring operators.

    Structures are rendered as `functor(arg1, ..., argN)` (lists too, as `'.'(head, tail)`), atoms
    are quoted when needed, and variables are rendered as `_<n>`.

    Returns:
        The formatter.

    Examples:
        >>> str(canonical_formatter().format(struct("+", "a", logic_list(1))))
        "'+'(a, '.'(1, []))"

    Note:
        Wraps 2P-Kt's `TermFormatter.canonical`.
    """
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


def default_formatter(
    operators: Any = None, tags: TagsFormattingOptions | None = None
) -> TermFormatter:
    """Creates the default formatter: operators as expressions, variables as `_<n>`, atoms never
    quoted, and tags shown.

    Args:
        operators: the operators to render as expressions (a `tuprolog.core.operators.OperatorSet`).
            If `None`, `tuprolog.core.operators.DEFAULT_OPERATORS`.
        tags: how to render the tags of terms. If `None`, the default options, but showing the tags.

    Returns:
        The formatter.

    Examples:
        >>> default_formatter().format(struct("+", var("X"), 1))
        '_... + 1'

    Note:
        Wraps 2P-Kt's `TermFormatter.default`.
    """
    # unlike the other factories, 2P-Kt's TermFormatter.default shows tags by default
    if tags is None:
        tags = _showing_tags(DEFAULT_TAGS_FORMATTING_OPTIONS)
    return TermFormatter.default(_operators_or_default(operators), tags)


def readable_formatter(
    operators: Any = None, tags: TagsFormattingOptions = DEFAULT_TAGS_FORMATTING_OPTIONS
) -> TermFormatter:
    """Creates a formatter for humans: operators as expressions, variables by their name (numbered
    when names clash, `_` for anonymous ones), atoms quoted when needed.

    Args:
        operators: the operators to render as expressions (a `tuprolog.core.operators.OperatorSet`).
            If `None`, `tuprolog.core.operators.DEFAULT_OPERATORS`.
        tags: how to render the tags of terms (by default, not rendering them).

    Returns:
        The formatter.

    Examples:
        >>> readable_formatter().format(struct("is", var("X"), struct("+", 1, 2)))
        'X is 1 + 2'

    Note:
        Wraps 2P-Kt's `TermFormatter.readable`.
    """
    return TermFormatter.readable(_operators_or_default(operators), tags)


def pretty_variables_formatter(
    tags: TagsFormattingOptions = DEFAULT_TAGS_FORMATTING_OPTIONS,
) -> TermFormatter:
    """Creates a formatter rendering variables by their name (numbered when names clash), operators
    canonically, and lists, tuples and blocks with their syntax.

    Args:
        tags: how to render the tags of terms (by default, not rendering them).

    Returns:
        The formatter.

    Examples:
        >>> str(pretty_variables_formatter().format(struct("+", var("X"), logic_list(1))))
        "'+'(X, [1])"

    Note:
        Wraps 2P-Kt's `TermFormatter.prettyVariables`.
    """
    return TermFormatter.prettyVariables(tags)


def pretty_expressions_formatter(
    pretty_variables: bool = True,
    operators: Any = None,
    tags: TagsFormattingOptions = DEFAULT_TAGS_FORMATTING_OPTIONS,
) -> TermFormatter:
    """Creates a formatter rendering operators as expressions, e.g. `1 + 2` rather than `'+'(1, 2)`.

    Args:
        pretty_variables: whether to render variables by their name (e.g. `X`), rather than by their
            complete name (e.g. `X_0`).
        operators: the operators to render as expressions (a `tuprolog.core.operators.OperatorSet`).
            If `None`, `tuprolog.core.operators.DEFAULT_OPERATORS`.
        tags: how to render the tags of terms (by default, not rendering them).

    Returns:
        The formatter.

    Examples:
        >>> term = struct("+", var("X"), struct("*", 2, 3))
        >>> pretty_expressions_formatter().format(term)
        'X + 2 * 3'
        >>> pretty_expressions_formatter(pretty_variables=False).format(term)
        'X_... + 2 * 3'

    Note:
        Wraps 2P-Kt's `TermFormatter.prettyExpressions`.
    """
    return TermFormatter.prettyExpressions(pretty_variables, _operators_or_default(operators), tags)
