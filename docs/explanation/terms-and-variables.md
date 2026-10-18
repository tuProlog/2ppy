# Terms and variables

Terms ([`tuprolog.core`](../api/tuprolog/core.md)) are the data of logic programs: atoms,
numbers, variables, compound terms, and the special structures built from them (lists, tuples,
clauses). This page explains three properties that shape how you work with them in 2PPy:
terms are immutable, variables have an identity, and bindings live in substitutions rather than in
the variables.

## The term hierarchy

```text
Term
├── Var                       X, _Tail, _
├── Constant
│   ├── Atom                  abe, 'Hello World'
│   │   ├── Truth             true, false, fail
│   │   ├── EmptyList         []
│   │   └── EmptyBlock        {}
│   └── Numeric
│       ├── Integer           42
│       └── Real              3.14
└── Struct                    point(1, 2)
    ├── List (Cons)           [1, 2 | T]
    ├── Tuple                 (a, b, c)
    ├── Block                 {a, b}
    ├── Indicator             member/2
    └── Clause                Head :- Body
        ├── Rule              p(X) :- q(X)
        │   └── Fact          p(a)            (a rule whose body is true)
        └── Directive         :- initialization(main)
```

Atoms are also structures with no arguments: an `Atom` is both a `Constant` and a `Struct`, and
`[]` is both an `Atom` and a `List`. Every term answers questions about its kind (`is_atom`,
`is_var`, `is_struct`, `is_list`, `is_ground`, ...), and exposes its parts (`functor`, `arity`,
`args`, `term[i]` for the i-th argument).

```pycon
>>> from tuprolog.core import atom, struct, var
>>> from tuprolog.core.parsing import parse_term
>>> t = parse_term("point(1, Y)")
>>> t.functor, t.arity, t[0], t.is_ground
('point', 2, 1, False)
>>> atom("a").is_struct, atom("a").arity, parse_term("[]").is_list
(True, 0, True)

```

## Terms are immutable

No operation changes a term in place: methods that "modify" a term return a new one. Terms can
therefore be shared freely, between Python objects, theories and solvers, with no risk of aliasing.

```pycon
>>> f = struct("f", var("X"))
>>> g = f.set_args(atom("a"))
>>> f, g
(f(X_...), f(a))

```

This is also why variables are never assigned: binding `X` to `a` does not change `X`, it
produces a substitution (below), which can be *applied* to terms to get new terms.

## Variables have an identity

Each call to `var("X")` creates a **distinct** variable, even with the same name. Variables are
told apart by their *complete name*, the name plus a unique suffix, shown when printing them
(`X_0`, `X_1`, ...):

```pycon
>>> X1, X2 = var("X"), var("X")
>>> X1.name, X2.name, X1 == X2
('X', 'X', False)
>>> struct("f", X1) == struct("f", X1), struct("f", X1) == struct("f", X2)
(True, False)

```

So, to refer to the same variable twice, reuse the same object:

```pycon
>>> from tuprolog.core import rule
>>> X = var("X")
>>> rule(struct("mortal", X), struct("human", X))
mortal(X_...) :- human(X_...)
>>> rule(struct("mortal", var("X")), struct("human", var("X")))  # two unrelated variables!
mortal(X_...) :- human(X_...)

```

Parsing takes care of this: within one parsed term or clause, variables with the same name are the
same variable.

```pycon
>>> list(parse_term("f(X, g(X, Y))").variables)
[X_..., X_..., Y_...]

```

A **scope** ([`tuprolog.core.scope`](../api/tuprolog/core.md)) gives the same variable for the same
name, which is handy to build several terms sharing variables:

```pycon
>>> from tuprolog.core import scope
>>> s = scope()
>>> s.var("X") == s.var("X")
True

```

The anonymous variable `_` is special: every occurrence is a fresh variable. `fresh_copy()`
renames all the variables of a term with fresh ones, as solvers do with clauses before using them,
so that the variables of different uses never clash.

Terms also offer weaker notions of equality: `term.equals(other, False)` compares variables by
name only, and `structurally_equals` treats any two variables as equal.

## Substitutions

A **substitution** maps variables to terms, e.g. `{X = a, Y = 1}`. It is what unification
produces (a *unifier*), what solvers accumulate while solving, and what solutions carry. Applying
a substitution to a term replaces its variables with their values, returning a new term:

```pycon
>>> from tuprolog.core import integer, substitution
>>> X, Y = var("X"), var("Y")
>>> sigma = substitution({X: atom("a")})
>>> point = struct("point", X, Y)
>>> point.apply(sigma), point[sigma]
(point(a, Y_...), point(a, Y_...))
>>> point
point(X_..., Y_...)

```

Substitutions can be combined (`+`), and failed: a failed substitution (`is_failed`) represents
the absence of a unifier, e.g. the outcome of unifying `a` with `b`. See the
[unification API](../api/tuprolog/unify.md).

## Numbers

Integers have arbitrary precision (`tuprolog.math.BigInteger`), and reals are arbitrary-precision
decimals (`BigDecimal`), so `0.1` is exactly `0.1`, unlike a binary `float`. Converting a real to a
Python `float` (`to_float()`, `to_python`) may lose precision; `decimal_value` gives a
`decimal.Decimal`.

```pycon
>>> from tuprolog.core import real
>>> real("0.1").decimal_value, integer(2**100)
(Decimal('0.1'), 1267650600228229401496703205376)

```

## See also

- Example notebook: [Terms and unification](../examples/01-terms-and-unification.ipynb).
- [Build and parse terms](../how-to/build-and-parse-terms.md), a practical guide.
- [Python–term conversions](../reference/python-term-conversions.md).
- 2P-Kt's [term model](https://tuprolog.github.io/2p-kt/explanation/term-model/) and
  [variables and scoping](https://tuprolog.github.io/2p-kt/explanation/variables-and-scoping/).
