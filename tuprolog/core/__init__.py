"""Logic terms and clauses: the data model of logic programming.

Every piece of data a logic program manipulates is a **term** (`Term`). Terms are immutable trees,
whose kinds are:

- **variables** (`Var`), placeholders for terms yet to be determined, e.g. `X` or `_`;
- **constants** (`Constant`), carrying a value and no sub-terms:
    - **atoms** (`Atom`), symbolic names, e.g. `bart`, `'Hello World'`, `[]`;
      `true`, `false` and `fail` are atoms too (`Truth`);
    - **numbers** (`Numeric`): arbitrary-precision **integers** (`Integer`, e.g. `42`) and
      **reals** (`Real`, e.g. `3.14`);
- **structures** (`Struct`), a.k.a. compound terms: a *functor* (a name) applied to zero or more
  *arguments* (terms), e.g. `parent(homer, bart)`, whose functor is `parent` and *arity* is 2;
  their *indicator* is `parent/2`. Some structures have a dedicated syntax and type:
    - **lists** (`List`): `[a, b, c]`, i.e. chains of cells (`Cons`) ending in the empty list
      `[]` (`EmptyList`), or in another term for partial lists, e.g. `[H | T]`;
    - **tuples** (`Tuple`): `(a, b, c)`, i.e. conjunctions;
    - **blocks** (`Block`): `{a, b, c}`;
    - **clauses** (`Clause`), the statements of logic programs: **rules** (`Rule`,
      `Head :- Body`, i.e. "`Head` holds if `Body` does"), **facts** (`Fact`, rules whose body is
      `true`, written `Head.`), and **directives** (`Directive`, `:- Body`, commands run when a
      program is loaded);
    - **indicators** (`Indicator`): `name/arity`, denoting predicates or functors.

A term is *ground* when it contains no variables. Variables are identified by more than their
name: each `var("X")` call creates a new variable, printed as `X_<n>` (its complete name), so that
equally named variables of different clauses never clash. Use the same `Var` object (or a `Scope`)
wherever a variable must occur more than once.

A **substitution** (`Substitution`) maps variables to terms, e.g. `{X = bart}`: applying it to a
term replaces the variables with their values. Successful substitutions are **unifiers**
(`Substitution.Unifier`); the failed one (`Substitution.Fail`) means that no assignment exists,
e.g. when unification fails (see `tuprolog.unify`).

This package offers:

- the JVM types of terms and substitutions, whose methods are callable with Python names, e.g.
  `term.is_ground`, `struct.functor`, `struct.args`, `term.apply(substitution)`;
- Pythonic factories (`atom`, `var`, `struct`, `integer`, `real`, `logic_list`, `rule`,
  `substitution`, ...), converting Python values into terms where terms are expected;
- the conversions between Python values and terms (`to_term`, `to_python`);
- formatters, rendering terms as text (`default_formatter`, `pretty_expressions_formatter`, ...).

Sub-packages: `tuprolog.core.operators` (operators, e.g. `+` in `1 + 2`) and
`tuprolog.core.parsing` (terms from text).

Examples:
    >>> from tuprolog.core import atom, logic_list, struct, to_python, var
    >>> X = var("X")
    >>> term = struct("parent", X, "bart")
    >>> term
    parent(X_..., bart)
    >>> term.functor, term.arity, term.is_ground
    ('parent', 2, False)
    >>> term[1]
    bart
    >>> to_python(logic_list(1, 2.5, "a"))
    [1, 2.5, 'a']

See Also:
    2P-Kt's term hierarchy: <https://tuprolog.github.io/2p-kt/reference/term-hierarchy/>, and
    variables' scoping: <https://tuprolog.github.io/2p-kt/explanation/variables-and-scoping/>.
"""

import tuprolog.core._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "DEFAULT_TAGS_FORMATTING_OPTIONS",
    "EMPTY_UNIFIER",
    "FAIL",
    "FAILED_SUBSTITUTION",
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
