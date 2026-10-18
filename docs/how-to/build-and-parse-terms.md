# Build and parse terms

Every piece of data a logic program handles is a *term*: an atom (`bart`), a number (`42`, `3.14`),
a variable (`X`), or a compound term, i.e. a *functor* applied to arguments (`parent(homer, bart)`).
Lists, tuples and clauses are compound terms too. This guide shows how to make terms in Python and
how to take them apart. For what terms are, see
[Terms and variables](../explanation/terms-and-variables.md).

## From Python values

The factories of `tuprolog.core` create each kind of term; those expecting terms convert Python
values with `to_term` (strings become atoms, numbers numbers, lists logic lists, tuples logic
tuples, booleans `true`/`false`):

```pycon
>>> from tuprolog.core import atom, integer, logic_list, real, struct, to_term, var
>>> struct("parent", "homer", "bart")
parent(homer, bart)
>>> struct("point", 1, 2.5), integer(10**30), real("0.1")
(point(1, 2.5), 1000000000000000000000000000000, 0.1)
>>> logic_list(1, "a", [2, 3])
[1, a, [2, 3]]
>>> to_term(("a", "b", "c"))
(a, b, c)
>>> atom("Hello World")  # printed quoted, as Prolog syntax requires
'Hello World'

```

The [conversion table](../reference/python-term-conversions.md) lists every conversion.

## From Prolog text

`tuprolog.core.parsing` parses Prolog syntax, with the standard operators. Printing a term (`str`, `repr`) writes most operators in canonical form
(`'+'(1, 2)`); see [Print terms](#print-terms) for other styles:

```pycon
>>> from tuprolog.core.parsing import parse_clause, parse_struct, parse_term
>>> term = parse_term("f(X, [1, 2 | T], 'hello world', 1 + 2 * 3)")
>>> term
f(X_..., [1, 2 | T_...], 'hello world', '+'(1, '*'(2, 3)))
>>> term[3].functor, term[3].args
('+', [1, '*'(2, 3)])
>>> parse_clause("grandparent(X, Z) :- parent(X, Y), parent(Y, Z)")
grandparent(X_..., Z_...) :- (parent(X_..., Y_...), parent(Y_..., Z_...))

```

Parsing an invalid text raises a `tuprolog.errors.ParsingError`, which is also a `ValueError`:

```pycon
>>> from tuprolog.errors import ParsingError
>>> try:
...     parse_term("f(a")
... except ValueError as error:
...     print(isinstance(error, ParsingError), error.line, error.column)
True 1 4

```

## Variables

Each `var("X")` call creates a *distinct* variable: printed names get a numeric suffix (`X_0`,
`X_1`, ...) telling variables with the same name apart. Reuse the same `Var` object to refer to
the same variable, e.g. in a rule's head and body:

```pycon
>>> from tuprolog.core import rule, variables
>>> X = var("X")
>>> rule(struct("mortal", X), struct("human", X))
mortal(X_...) :- human(X_...)
>>> var("X") == var("X")
False
>>> A, B = variables("A", "B")

```

Within a parsed text, instead, equal names denote the same variable:

```pycon
>>> t = parse_term("f(X, Y, X)")
>>> t[0] == t[2], t[0] == t[1]
(True, False)

```

## Take terms apart

Terms are immutable trees. Inspect them with properties (`functor`, `arity`, `args`, `is_atom`,
`is_var`, `is_ground`, ...) and indexing:

```pycon
>>> t = parse_term("point(1, Y)")
>>> t.functor, t.arity, t.is_ground
('point', 2, False)
>>> t[0], t[1].is_var, t[1].name
(1, True, 'Y')
>>> [str(item) for item in parse_term("[a, b, c]")]
['a', 'b', 'c']

```

Convert terms back into Python values with `to_python` (terms without a Python counterpart, such
as variables and compound terms, stay as they are):

```pycon
>>> from tuprolog.core import to_python
>>> to_python(parse_term("[1, 2.5, abc, (x, y)]"))
[1, 2.5, 'abc', ('x', 'y')]

```

## Apply substitutions

A *substitution* maps variables to terms. Build one by unifying two terms (see `tuprolog.unify`),
then apply it:

```pycon
>>> from tuprolog.unify import mgu
>>> pattern = parse_term("point(X, Y)")
>>> substitution = mgu(pattern, parse_term("point(1, 2)"))
>>> pattern.apply(substitution)
point(1, 2)
>>> mgu(parse_term("f(a)"), parse_term("f(b)")).is_failed  # no substitution makes them equal
True

```

## Print terms

`str(term)` writes Prolog syntax, with most operators in canonical form and variables with their
numeric suffixes. Formatters (`tuprolog.core.TermFormatter`) offer other styles, e.g. with
operators in infix notation and readable variable names:

```pycon
>>> from tuprolog.core import pretty_expressions_formatter
>>> t = parse_term("X + 2 * Y")
>>> print(t)
'+'(X_..., '*'(2, Y_...))
>>> print(pretty_expressions_formatter().format(t))
X + 2 * Y

```

## Custom operators

Operators let Prolog text use infix, prefix or postfix notation (`1 + 2`, `- X`, `a :- b`). Parse
text with operators of your own by passing them, together with the default ones:

```pycon
>>> from tuprolog.core.operators import DEFAULT_OPERATORS, XFX, operator, operator_set
>>> likes = operator_set(operator("likes", XFX, 700))
>>> parse_term("bart likes skateboarding", DEFAULT_OPERATORS + likes)
likes(bart, skateboarding)

```

## See also

- API: `tuprolog.core` ([reference](../api/tuprolog/core.md)),
  `tuprolog.core.parsing` ([reference](../api/tuprolog/core/parsing.md)),
  `tuprolog.core.operators` ([reference](../api/tuprolog/core/operators.md)),
  `tuprolog.unify` ([reference](../api/tuprolog/unify.md)).
- 2P-Kt's [term hierarchy](https://tuprolog.github.io/2p-kt/reference/term-hierarchy/).
