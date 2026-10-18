import it.unibo.tuprolog.core as _core  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JImplements, JOverride

from tuprolog import logger

__all__ = [
    "DEFAULT_TAGS_FORMATTING_OPTIONS",
    "FAIL",
    "FALSE",
    "TRUE",
    "AbstractTermComparator",
    "AbstractTermConvertible",
    "AbstractTermVisitor",
    "Applicable",
    "Atom",
    "Block",
    "Clause",
    "Cons",
    "Constant",
    "Directive",
    "Empty",
    "EmptyBlock",
    "EmptyList",
    "Fact",
    "Formatter",
    "Indicator",
    "Integer",
    "List",
    "Numeric",
    "Real",
    "Recursive",
    "Rule",
    "Scope",
    "Struct",
    "Substitution",
    "TagsFormattingOptions",
    "Term",
    "TermComparator",
    "TermConvertible",
    "TermFormatter",
    "TermVisitor",
    "Terms",
    "Truth",
    "Tuple",
    "Var",
    "Variabled",
]


Applicable = _core.Applicable
"""Terms (and other objects) to which a substitution can be applied, i.e. `Term` and its sub-types.

`apply(substitution)` returns a copy of the object where the variables bound by the substitution are
replaced by their values (in Python, also `term[substitution]`); `fresh_copy()` returns a copy
where every variable is replaced by a brand-new one.

Note:
    2P-Kt's `it.unibo.tuprolog.core.Applicable`.
"""


Atom = _core.Atom
"""A constant symbolic name, e.g. `bart`, `'Hello World'`, `[]`, `+`.

An atom is both a `Constant`, whose `value` is its name, and a structure with no arguments, whose
`functor` is its name (and whose `arity` is 0). Atoms needing quotes in Prolog syntax (e.g. those
starting with an uppercase letter or containing spaces) are printed quoted.

Some atoms have a dedicated type: `[]` is the `EmptyList`, `{}` the `EmptyBlock`, and `true`,
`false` and `fail` are `Truth`s.

Build atoms with `tuprolog.core.atom` (or `Atom.of`). Members: `value` (the name, a string).

Examples:
    >>> from tuprolog.core import atom
    >>> atom("bart"), atom("Hello World")
    (bart, 'Hello World')
    >>> atom("bart").value
    'bart'
    >>> atom("bart").is_atom, atom("bart").arity
    (True, 0)
"""


Block = _core.Block
"""A block, i.e. a curly-braced term: `{a, b, c}`, commonly used in grammar rules.

A block wrapping two or more terms folds them into a tuple, i.e. `{a, b, c}` is the structure
`{}((a, b, c))`; the block wrapping no terms is the `EmptyBlock` `{}`. As other `Recursive` terms,
blocks are iterable (and sized) over the terms they wrap.

Build blocks with `tuprolog.core.block` (or `tuprolog.core.empty_block`).

Examples:
    >>> from tuprolog.core import atom, block
    >>> b = block(atom("a"), atom("b"))
    >>> b, len(b), list(b)
    ({a, b}, 2, [a, b])
"""


Clause = _core.Clause
"""A clause, i.e. a statement of a logic program: a structure with functor `:-`.

A clause is either a **rule** (`Rule`), `Head :- Body`, meaning that `Head` holds if `Body` does,
or a **directive** (`Directive`), `:- Body`, a goal run when the program is loaded. Facts (`Fact`)
are rules whose body is `true`, written `Head.`. A theory (see `tuprolog.theory`) is a sequence of
clauses.

The body is a goal, i.e. a callable term, possibly a conjunction (a `Tuple`) of goals, as in
`grandparent(X, Z) :- parent(X, Y), parent(Y, Z)`.

Build clauses with `tuprolog.core.clause` (or the more specific `rule`, `fact`, `directive`).
Members: `head` (a `Struct`, or `None` for directives), `body` (a `Term`), `body_items` (the goals
of the body), `body_size`, `is_rule`, `is_fact`, `is_directive`, `is_well_formed`, and methods
returning modified copies, e.g. `set_head(head)`, `set_body(body)`, `set_head_args(*args)`,
`insert_head_arg(index, arg)`, `set_body_items(*goals)`.

Examples:
    >>> from tuprolog.core import rule, struct, variables
    >>> X, Y, Z = variables("X", "Y", "Z")
    >>> r = rule(
    ...     struct("grandparent", X, Z), struct("parent", X, Y), struct("parent", Y, Z)
    ... )
    >>> r.head, r.body_size
    (grandparent(X_..., Z_...), 2)
    >>> r.is_rule, r.is_fact, r.is_directive
    (True, False, False)
"""


Cons = _core.Cons
"""A non-empty list cell: a structure with functor `.` and two arguments, its `head` (the first
item) and its `tail` (the rest of the list).

`[a, b]` is `'.'(a, '.'(b, []))`, i.e. a chain of cells ending in the `EmptyList`. When a chain
ends in another term (e.g. a variable), the list is *partial*, e.g. `[a | T]`.

Build cells with `tuprolog.core.cons` (or `logic_list`, `logic_list_from`).

Examples:
    >>> from tuprolog.core import atom, cons, logic_list
    >>> cell = cons(atom("a"), logic_list("b", "c"))
    >>> cell, cell.head, cell.tail
    ([a, b, c], a, [b, c])
"""


Constant = _core.Constant
"""A term carrying a single value and no sub-terms: an `Atom` (whose value is a string) or a
`Numeric` (whose value is a number). Constants are always ground.

Members: `value`, `is_constant`.
"""


Directive = _core.Directive
"""A clause without head, `:- Body`, e.g. `:- dynamic(counter/1).`: a goal to run when the program
including it is loaded, rather than knowledge to query.

Build directives with `tuprolog.core.directive` (or `clause(None, ...)`).

Examples:
    >>> from tuprolog.core import directive, struct
    >>> d = directive(struct("initialization", "main"))
    >>> d, d.head, d.body
    (:- initialization(main), None, initialization(main))
"""


Empty = _core.Empty
"""The type of the two "empty" atoms: the `EmptyList` `[]` and the `EmptyBlock` `{}`."""


EmptyBlock = _core.EmptyBlock
"""The empty block, i.e. the atom `{}`, a singleton (see `tuprolog.core.empty_block`)."""


EmptyList = _core.EmptyList
"""The empty list, i.e. the atom `[]`, a singleton (see `tuprolog.core.empty_logic_list`).

Every well-formed list ends with it.
"""


Fact = _core.Fact
"""A rule whose body is `true`, written `Head.`, e.g. `parent(homer, bart).`: an unconditional
truth.

Rule factories return a fact whenever the body is `true`. Build facts with `tuprolog.core.fact`.

Examples:
    >>> from tuprolog.core import fact, struct
    >>> f = fact(struct("parent", "homer", "bart"))
    >>> f, f.head, f.body, f.is_fact
    (parent(homer, bart) :- true, parent(homer, bart), true, True)
"""


Formatter = _core.Formatter
"""An object turning other objects into strings, by its `format(obj)` method.

`TermFormatter` is the formatter of terms.
"""


Indicator = _core.Indicator
"""A predicate (or functor) indicator, `Name/Arity`, e.g. `parent/2`: the term identifying a
predicate (or a functor) by its name and its number of arguments.

Build indicators with `tuprolog.core.indicator`. Members: `indicated_name` (a string),
`indicated_arity` (an int), `name_term`, `arity_term`, `is_well_formed` (whether the name is an atom
and the arity a non-negative integer).

Examples:
    >>> from tuprolog.core import indicator
    >>> i = indicator("parent", 2)
    >>> i, i.indicated_name, i.indicated_arity
    (parent/2, 'parent', 2)
"""


Integer = _core.Integer
"""An integer number, e.g. `42`, of arbitrary precision (never overflowing).

Build integers with `tuprolog.core.integer` (or `numeric`). Members: `value` and `int_value` (the
value, a Python `int`), `decimal_value` (a `decimal.Decimal`), `to_int()`, `to_float()`.

Examples:
    >>> from tuprolog.core import integer
    >>> n = integer("123456789012345678901234567890")
    >>> n, n.value + 1
    (123456789012345678901234567890, 123456789012345678901234567891)
"""


List = _core.List
"""A logic list: either the `EmptyList` `[]`, or a `Cons` cell `[Head | Tail]`.

`[a, b, c]` is a chain of cells ending in `[]`: it is *well-formed*. A chain ending in another term,
as `[a, b | T]`, is a *partial* list. Lists are iterable (and sized) over their items, the last
item of a partial list being its final tail.

Build lists with `tuprolog.core.logic_list`, `logic_list_from`, `cons`, or `empty_logic_list`.
Members: `is_well_formed`, `unfolded` (all items, including the final `[]` of well-formed lists),
`to_iterable()`, and those of `Recursive` terms.

Examples:
    >>> from tuprolog.core import logic_list, logic_list_from, var
    >>> logic_list(1, 2, 3), len(logic_list(1, 2, 3)), list(logic_list(1, 2, 3))
    ([1, 2, 3], 3, [1, 2, 3])
    >>> partial = logic_list_from([1, 2], last=var("T"))
    >>> partial, partial.is_well_formed
    ([1, 2 | T_...], False)
"""


Numeric = _core.Numeric
"""A number: an `Integer` or a `Real`, both of arbitrary precision.

Integers and reals are distinct terms, even when their values are equal (`1` and `1.0`), as in
Prolog. Build numbers with `tuprolog.core.numeric` (or `integer`, `real`). Members: `int_value` (a
Python `int`), `decimal_value` (a `decimal.Decimal`), `to_int()`, `to_float()`,
`compare_value_to(other)` (comparing values, regardless of the kind of number).

Examples:
    >>> from tuprolog.core import integer, real
    >>> integer(1) == real(1.0), integer(1).compare_value_to(real(1.0))
    (False, 0)
    >>> real(2.5).to_int(), integer(3).to_float()
    (2, 3.0)
"""


Real = _core.Real
"""A real number, e.g. `3.14`, of arbitrary precision (a decimal, not a binary floating-point
number).

Build reals with `tuprolog.core.real` (or `numeric`). Members: `value` and `decimal_value` (the
value, a `decimal.Decimal`), `int_value`, `to_int()`, `to_float()`.

Examples:
    >>> from tuprolog.core import real
    >>> real(0.1), real(0.1).value, real("3.14").to_float()
    (0.1, Decimal('0.1'), 3.14)
"""


Recursive = _core.Recursive
"""A structure representing a sequence of terms folded into nested binary structures: a `List`
(functor `.`), a `Tuple` (functor `,`) or a `Block` (functor `{}`).

Python protocols: `len(term)` is the number of items, and `iter(term)` iterates over them.
Members: `size`, `unfolded` (the items, as a list), `lazily_unfolded` (the items, lazily),
`to_iterable()`.
"""


Rule = _core.Rule
"""A clause with a head, `Head :- Body`: "`Head` holds if `Body` does", e.g.
`grandparent(X, Z) :- parent(X, Y), parent(Y, Z)`.

When the body is `true` the rule is a `Fact`. Build rules with `tuprolog.core.rule`. See `Clause`
for the members.

Examples:
    >>> from tuprolog.core import rule, struct, var
    >>> X = var("X")
    >>> r = rule(struct("mortal", X), struct("human", X))
    >>> r, r.head, r.body
    (mortal(X_...) :- human(X_...), mortal(X_...), human(X_...))
"""


Scope = _core.Scope
"""A factory of terms remembering the variables it creates, by name.

As `var("X")` creates a new variable at each call, building a term where a variable occurs more
than once requires reusing the same `Var` object: a scope does it automatically, as asking it for
a variable it already created returns that variable. Its factories mirror those of
`tuprolog.core` (`var`, `atom`, `struct`, `integer`, `real`, `numeric`, `truth`, `list`,
`list_from`, `tuple`, `cons`, `block`, `clause`, `rule`, `fact`, `directive`, `indicator`),
without converting Python values: pass them terms.

Python protocols: `name in scope` tells whether the scope created a variable named `name`, and
`scope[name]` returns it (or `None`). Members: `variables` (a map from names to variables),
`anonymous()` (a new anonymous variable: `var("_")` returns the same variable at each call).

Build scopes with `tuprolog.core.scope`.

Examples:
    >>> from tuprolog.core import scope
    >>> s = scope()
    >>> s.struct("member", s.var("H"), s.list_from([s.var("_")], s.var("T")))
    member(H_..., [__... | T_...])
    >>> s.var("H") == s["H"], "H" in s, "X" in s
    (True, True, False)
"""


Struct = _core.Struct
"""A structure, a.k.a. compound term: a *functor* (a name) applied to zero or more *arguments*
(terms), e.g. `parent(homer, bart)`, whose functor is `parent` and *arity* is 2.

Most terms are structures under the hood: atoms (no arguments), lists, tuples, blocks, clauses and
indicators, which have dedicated types. Structures are immutable: "modifying" methods return new
structures.

Build structures with `tuprolog.core.struct`. Members: `functor`, `arity`, `args` (the arguments),
`indicator` (`functor/arity`), `get_arg_at(i)`, and methods returning modified copies, e.g.
`set_functor(name)`, `set_args(*args)`, `add_first(arg)`, `add_last(arg)`, `insert_at(i, arg)`.

Python protocols: `struct[i]` is the `i`-th argument, and `struct[i, j, ...]` is
`struct[i][j]...`.

Examples:
    >>> from tuprolog.core import atom, struct
    >>> s = struct("f", "a", struct("g", "b"))
    >>> s.functor, s.arity, s.indicator
    ('f', 2, f/2)
    >>> s[0], s[1, 0]
    (a, b)
    >>> s.set_functor("h"), s.add_last(atom("c"))
    (h(a, g(b)), f(a, g(b), c))
"""


Substitution = _core.Substitution
"""A substitution, i.e. an assignment of terms to variables, e.g. `{X = bart, Y = 1}`.

A substitution is either a **unifier** (`Substitution.Unifier`), a successful (possibly empty)
assignment, or the **failed** substitution (`Substitution.Fail`), meaning that no assignment
exists, e.g. because two terms do not unify (see `tuprolog.unify`). Applying a unifier to a term
replaces the assigned variables with their values (`term.apply(substitution)`, or
`term[substitution]`).

Substitutions are immutable mappings from `Var`s to `Term`s: `substitution[var]`, `var in
substitution`, `len(substitution)` and iteration work as for dictionaries. Combining two
substitutions with `+` merges them, failing when they assign different values to a variable; `-`
removes variables. Members: `is_success`, `is_failed`, `get_by_name(name)`, `apply_to(term)`,
`filter(...)`.

Build substitutions with `tuprolog.core.substitution`, `unifier`, `failed`, or use the constants
`EMPTY_UNIFIER` and `FAILED_SUBSTITUTION`.

Examples:
    >>> from tuprolog.core import atom, struct, substitution, var
    >>> X, Y = var("X"), var("Y")
    >>> s = substitution({X: atom("a")})
    >>> s[X], X in s, len(s), s.is_success
    (a, True, 1, True)
    >>> struct("f", X, Y)[s]
    f(a, Y_...)
    >>> (s + substitution({X: atom("b")})).is_failed
    True
"""


Term = _core.Term
"""The base type of all logic terms: variables (`Var`), constants (`Atom`s and `Numeric`s), and
structures (`Struct`, including lists, tuples, blocks and clauses).

Terms are immutable trees: methods "changing" a term return a new one. Terms are compared by
`==` (variables being equal only to themselves) and ordered by the standard order of terms
(variables, then numbers, then atoms, then structures), so `<` and `sorted` work.

Members, callable on any term:

- type checks (properties): `is_var`, `is_constant`, `is_atom`, `is_number`, `is_integer`,
  `is_real`, `is_struct`, `is_list`, `is_cons`, `is_empty_list`, `is_tuple`, `is_block`,
  `is_clause`, `is_rule`, `is_fact`, `is_directive`, `is_truth`, `is_true`, `is_ground`, ...;
- casts: `cast_to_<type>()` (e.g. `cast_to_struct()`, raising a Java `ClassCastException` on
  mismatch) and `as_<type>()` (e.g. `as_var()`, returning `None` on mismatch);
- `variables` (the variables occurring in the term, lazily, repetitions included);
- `apply(substitution)` (in Python, also `term[substitution]`), `fresh_copy()` (a copy with new
  variables);
- `structurally_equals(other)` (equality up to variables' renaming), `accept(visitor)` (see
  `TermVisitor`);
- `tags` (metadata attached to the term, see `tuprolog.utils.Taggable`).

`str(term)` and `repr(term)` render the term in Prolog syntax; see `TermFormatter` for other
renderings.

Examples:
    >>> from tuprolog.core import atom, integer, struct, var
    >>> X = var("X")
    >>> t = struct("f", X, "a")
    >>> t.is_struct, t.is_ground, t.as_var()
    (True, False, None)
    >>> list(t.variables)
    [X_...]
    >>> sorted([atom("b"), integer(1), struct("f", "a"), atom("a")])
    [1, a, b, f(a)]
    >>> t.structurally_equals(struct("f", var("Y"), "a"))
    True

See Also:
    2P-Kt's term hierarchy: <https://tuprolog.github.io/2p-kt/reference/term-hierarchy/>.
"""


TermComparator = _core.TermComparator
"""A comparator of terms (a JVM `java.util.Comparator`), following the standard order of terms:
variables, then numbers, then atoms, then structures (by arity, then functor, then arguments).

Implement custom comparators in Python by subclassing `AbstractTermComparator`.
"""


TermConvertible = _core.TermConvertible
"""Objects convertible into terms, by their `to_term()` method (e.g. operators, see
`tuprolog.core.operators.Operator`).

Implement it in Python by subclassing `AbstractTermConvertible`.
"""


TermFormatter = _core.TermFormatter
"""A formatter rendering terms as text, by its `format(term)` method.

Formatters differ in how they render variables (by complete name, e.g. `X_0`, by name, e.g. `X`, or
as `_<n>`), operators (canonically, e.g. `'+'(1, 2)`, or as expressions, e.g. `1 + 2`), and
whether they quote atoms when needed. Build formatters with `tuprolog.core.default_formatter`,
`canonical_formatter`, `readable_formatter`, `pretty_variables_formatter`, or
`pretty_expressions_formatter`.

Examples:
    >>> from tuprolog.core import pretty_expressions_formatter, struct, var
    >>> pretty_expressions_formatter().format(struct("+", var("X"), 1))
    'X + 1'
"""


TagsFormattingOptions = TermFormatter.TagsFormattingOptions
"""Options for rendering the tags of terms (see `Term.tags`), used by formatters.

Its constructor takes (all optional): `showTags` (whether to render tags, default false),
`delimiters` (a Kotlin pair of strings, default `<` and `>`), `separator` (default `", "`),
`showKeys` (default true), `showDelimitersIfEmpty` (default false), `keyFilter` (a predicate over
tag names), `tagFormatter` (a `Formatter` of tag values). Its `copy(...)` method takes them all,
positionally.
"""


DEFAULT_TAGS_FORMATTING_OPTIONS: TagsFormattingOptions = TagsFormattingOptions()
"""The default `TagsFormattingOptions`, not rendering tags."""


Terms = _core.Terms
"""Constants shared by the term types, e.g. reserved functors and the patterns of well-formed
names."""


TermVisitor = _core.TermVisitor
"""A visitor of terms (the Visitor pattern): `term.accept(visitor)` calls the `visitX` method
matching the term's type (`visitVar`, `visitAtom`, `visitStruct`, `visitList`, ...).

Each `visitX` method defaults to the method of the parent type (e.g. `visitAtom` to `visitStruct`,
and finally `visitTerm` to `defaultValue`), so implementations override just the methods they need,
plus `defaultValue`. Implement visitors in Python by subclassing `AbstractTermVisitor`.
"""


Truth = _core.Truth
"""A truth value: one of the atoms `true`, `false` and `fail` (the constants `TRUE`, `FALSE`,
`FAIL`).

Build them with `tuprolog.core.truth`, or `atom("true")` etc. Members: `is_true`, `is_fail`.
"""


Tuple = _core.Tuple
"""A tuple, i.e. a conjunction: `(a, b, c)`, a structure with functor `,` and two arguments, `left`
and `right`, where tuples of more items nest on the right (`(a, (b, c))` is `(a, b, c)`).

The bodies of clauses with many goals are tuples. As other `Recursive` terms, tuples are iterable
(and sized) over their items.

Build tuples with `tuprolog.core.logic_tuple`.

Examples:
    >>> from tuprolog.core import logic_tuple
    >>> t = logic_tuple(1, 2, 3)
    >>> t, t.left, t.right, list(t)
    ((1, 2, 3), 1, (2, 3), [1, 2, 3])
"""


Var = _core.Var
"""A logic variable: a placeholder for a term yet to be determined, e.g. `X`.

A variable has a `name` (e.g. `X`), but its identity is its `complete_name` (e.g. `X_0`), pairing
the name with a unique number: each `var("X")` call creates a new variable, different from other
variables named `X`, so that variables of different clauses never clash. Reuse the same `Var`
object (or a `Scope`) wherever a variable must occur more than once. Variables named `_` are
*anonymous*: each occurrence is a different variable.

Build variables with `tuprolog.core.var` or `variables`. Members: `name`, `complete_name`,
`is_anonymous`.

Examples:
    >>> from tuprolog.core import var
    >>> X = var("X")
    >>> X.name, X == X, X == var("X")
    ('X', True, False)
    >>> var("_").is_anonymous
    True
"""


Variabled = _core.Variabled
"""Objects containing variables, i.e. terms: their `variables` member lists the variables occurring
in them.
"""


TRUE = Truth.TRUE
"""The atom `true`, i.e. the goal that always succeeds."""


FALSE = Truth.FALSE
"""The atom `false`, i.e. a goal that always fails."""


FAIL = Truth.FAIL
"""The atom `fail`, i.e. a goal that always fails."""


@JImplements(TermComparator)
class AbstractTermComparator:
    """A base class for term comparators implemented in Python.

    Override `compare(first, second)`, returning a negative int, zero, or a positive int when
    `first` precedes, equals, or follows `second`. Instances are `TermComparator`s, usable wherever
    2P-Kt expects one.

    Examples:
        >>> from tuprolog.core import AbstractTermComparator, atom
        >>> class ByLength(AbstractTermComparator):
        ...     def compare(self, first, second):
        ...         return len(str(first)) - len(str(second))
        >>> ByLength().compare(atom("abc"), atom("z")) > 0
        True
    """

    @JOverride
    def equals(self, other):
        return self is other

    @JOverride
    def compare(self, first, second):
        raise NotImplementedError()


@JImplements(TermConvertible)
class AbstractTermConvertible:
    """A base class for Python objects convertible into terms: override `toTerm()`.

    Instances are `TermConvertible`s, usable wherever 2P-Kt expects one.
    """

    @JOverride
    def toTerm(self):
        raise NotImplementedError()


@JImplements(TermVisitor)
class AbstractTermVisitor:
    """A base class for term visitors implemented in Python (see `TermVisitor`).

    Override `defaultValue(term)`, the result for the terms whose `visitX` method is not overridden,
    and any `visitX(term)` method (`visitVar`, `visitAtom`, `visitStruct`, `visitList`, ...): the
    ones not overridden delegate to the method of the parent type, as in 2P-Kt. Then call
    `term.accept(visitor)`.

    Examples:
        >>> from tuprolog.core import AbstractTermVisitor, atom, integer, var
        >>> class Kind(AbstractTermVisitor):
        ...     def defaultValue(self, term):
        ...         return "other"
        ...     def visitAtom(self, term):
        ...         return "atom"
        ...     def visitVar(self, term):
        ...         return "variable"
        >>> [t.accept(Kind()) for t in (atom("a"), var("X"), integer(1))]
        ['atom', 'variable', 'other']
    """

    @JOverride
    def defaultValue(self, term):
        raise NotImplementedError()

    @JOverride
    def visitTerm(self, term):
        return TermVisitor.visitTerm(self, term)

    @JOverride
    def visitVar(self, term):
        return TermVisitor.visitVar(self, term)

    @JOverride
    def visitConstant(self, term):
        return TermVisitor.visitConstant(self, term)

    @JOverride
    def visitStruct(self, term):
        return TermVisitor.visitStruct(self, term)

    @JOverride
    def visitCollection(self, term):
        return TermVisitor.visitCollection(self, term)

    @JOverride
    def visitAtom(self, term):
        return TermVisitor.visitAtom(self, term)

    @JOverride
    def visitTruth(self, term):
        return TermVisitor.visitTruth(self, term)

    @JOverride
    def visitNumeric(self, term):
        return TermVisitor.visitNumeric(self, term)

    @JOverride
    def visitInteger(self, term):
        return TermVisitor.visitInteger(self, term)

    @JOverride
    def visitReal(self, term):
        return TermVisitor.visitReal(self, term)

    @JOverride
    def visitBlock(self, term):
        return TermVisitor.visitBlock(self, term)

    @JOverride
    def visitEmpty(self, term):
        return TermVisitor.visitEmpty(self, term)

    @JOverride
    def visitEmptyBlock(self, term):
        return TermVisitor.visitEmptyBlock(self, term)

    @JOverride
    def visitList(self, term):
        return TermVisitor.visitList(self, term)

    @JOverride
    def visitCons(self, term):
        return TermVisitor.visitCons(self, term)

    @JOverride
    def visitEmptyList(self, term):
        return TermVisitor.visitEmptyList(self, term)

    @JOverride
    def visitTuple(self, term):
        return TermVisitor.visitTuple(self, term)

    @JOverride
    def visitIndicator(self, term):
        return TermVisitor.visitIndicator(self, term)

    @JOverride
    def visitClause(self, term):
        return TermVisitor.visitClause(self, term)

    @JOverride
    def visitRule(self, term):
        return TermVisitor.visitRule(self, term)

    @JOverride
    def visitFact(self, term):
        return TermVisitor.visitFact(self, term)

    @JOverride
    def visitDirective(self, term):
        return TermVisitor.visitDirective(self, term)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.*")
