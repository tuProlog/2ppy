# Logic programming in a nutshell

Logic programming is *declarative*: rather than writing the steps of a computation, you state
**facts** and **rules** about a problem, and ask **queries**; a **solver** searches for the
answers. Prolog, the best-known logic programming language, is what 2PPy's solvers run. This page
introduces the notions the rest of the documentation relies on, assuming you know Python but not
Prolog.

## Terms: the data

Everything is a **term**:

- **atoms** are symbolic constants: `abe`, `red`, `'Hello World'` (quoted when they start with an
  uppercase letter or contain spaces), `[]`;
- **numbers**: integers (`42`, of any size) and reals (`3.14`);
- **variables** are placeholders for terms, written with an uppercase initial or `_`: `X`,
  `Person`, `_Tail`; the bare `_` is *anonymous*, i.e. a fresh variable each time it occurs;
- **compound terms** (or structures) apply a **functor** to arguments: `point(1, 2)`,
  `parent(abe, homer)`. The number of arguments is the **arity**: `point/2` names a functor
  `point` of arity 2;
- **lists** are written `[1, 2, 3]`, or `[Head | Tail]` to split off their first item(s).

Some functors are **operators**, written in infix, prefix or postfix notation: `1 + 2` is the
compound term `+(1, 2)`, and `X = Y` is `=(X, Y)`. Terms are *not* evaluated: `1 + 2` is a
structure, not `3`, unless arithmetic is explicitly asked for (`X is 1 + 2`).

## Clauses: the program

A program is a **theory** (or knowledge base): a sequence of **clauses**, each ending with a
full stop.

```prolog
% facts: what holds unconditionally
parent(abe, homer).
parent(homer, bart).
parent(homer, lisa).

% rules: Head holds if Body does (`:-` reads "if", `,` reads "and")
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
```

Variables are universally quantified within their clause: the rule reads "for all `X`, `Y`, `Z`,
`X` is a grandparent of `Z` if `X` is a parent of `Y` and `Y` is a parent of `Z`". The clauses
whose heads share a functor and arity form a **predicate**, e.g. `parent/2`.

A **query** (or goal) asks whether something follows from the program, and for which values of
its variables:

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> from tuprolog.theory.parsing import parse_theory
>>> kb = parse_theory("""
...     parent(abe, homer). parent(homer, bart). parent(homer, lisa).
...     grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
... """)
>>> solver = prolog_solver(static_kb=kb)
>>> list(solver.query("grandparent(abe, G)"))
[{'G': 'bart'}, {'G': 'lisa'}]

```

## Unification: matching terms

The solver matches goals against clause heads by **unification**: two terms unify if some
assignment of their variables makes them identical. The most general such assignment is their
**most general unifier** (mgu), a **substitution** like `{X = homer, Y = abe}`.

| Terms | Unify? | Substitution |
|---|---|---|
| `parent(abe, X)` and `parent(Y, homer)` | yes | `{Y = abe, X = homer}` |
| `point(X, 2)` and `point(1, Y)` | yes | `{X = 1, Y = 2}` |
| `f(X, X)` and `f(a, b)` | no | `X` cannot be both `a` and `b` |
| `X` and `f(X)` | no, with the occurs check | `X = f(f(f(...)))` would be infinite |

```pycon
>>> from tuprolog.core.parsing import parse_term
>>> from tuprolog.unify import mgu
>>> mgu(parse_term("parent(abe, X)"), parse_term("parent(Y, homer)"))
{Y_...=abe, X_...=homer}
>>> mgu(parse_term("f(X, X)"), parse_term("f(a, b)")).is_failed
True

```

Unification works both ways: there are no input and output arguments. `parent(homer, C)` asks
for homer's children, `parent(P, bart)` for bart's parents, with the same clauses.

## Resolution: how queries are solved

Prolog solvers use **SLD resolution**. To solve a goal, the solver:

1. picks the first clause (in program order) whose head unifies with the goal;
2. applies the unifier, and replaces the goal with the clause's body (nothing, for a fact);
3. solves the body's goals, left to right, the same way;
4. when no goals are left, it has found a **solution**: the bindings of the query's variables.

When a goal matches no (further) clause, the solver **backtracks**: it goes back to the most
recent choice that has alternatives, undoes the bindings made since, and tries the next clause.
Asking for more solutions backtracks as well. The search is therefore depth-first, in program
order, which makes clause and goal order matter: a left-recursive rule such as
`ancestor(X, Y) :- ancestor(X, Z), parent(Z, Y).` loops forever.

In 2PPy, solutions are produced lazily: `solver.solve(goal)` and `solver.query(goal)` return
iterators that search for the next solution only when asked (see
[Solvers and solutions](solvers-and-solutions.md)).

## Cut and negation

The **cut**, `!`, prunes the search: once reached, it commits to the clause it is in and to the
choices made in its body so far, discarding their alternatives.

```prolog
max(X, Y, X) :- X >= Y, !.   % if X >= Y, do not try the next clause
max(_, Y, Y).
```

**Negation as failure**, `\+ Goal` (or `not(Goal)`), succeeds if `Goal` has no solution. It is not
logical negation: it means "cannot be proved from the program" (the *closed-world assumption*),
and it binds no variables.

```pycon
>>> kb = parse_theory("""
...     parent(homer, bart).
...     childless(P) :- \\+ parent(P, _).
...     max(X, Y, X) :- X >= Y, !.
...     max(_, Y, Y).
... """)
>>> solver = prolog_solver(static_kb=kb)
>>> list(solver.query("childless(bart)")), list(solver.query("childless(homer)"))
([{}], [])
>>> list(solver.query("max(3, 5, M)"))
[{'M': 5}]

```

(`\\+` is `\+` escaped in a Python string.) A query with no variables gives one empty dictionary
per solution, or none.

## Beyond pure logic

Prolog also offers **built-in predicates** for arithmetic (`is/2`), term inspection, collecting
solutions (`findall/3`), changing the knowledge base while solving (`assertz/1`, `retract/1`),
input and output, and exceptions (`catch/3`, `throw/1`): see
[Standard predicates](../reference/standard-predicates.md). Errors are thrown as terms, e.g.
`error(type_error(atom, 1), _)`, and become Python exceptions at the boundary (see
[Exceptions](../reference/exceptions.md)).

**Probabilistic** logic programming extends clauses with probabilities (`0.6::heads(coin).`), so
that queries yield the probability of being true: see
[Run probabilistic programs](../how-to/run-probabilistic-programs.md).

## Further reading

- [Your first logic program](../tutorials/your-first-logic-program.md), a hands-on tutorial.
- [Learn Prolog Now!](https://lpn.swi-prolog.org/), a free introductory book on Prolog.
- 2P-Kt's [term model](https://tuprolog.github.io/2p-kt/explanation/term-model/) and
  [solver design](https://tuprolog.github.io/2p-kt/explanation/solver-design/).
