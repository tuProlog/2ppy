# Your first logic program

In this tutorial you write a small Prolog program about a family, step by step: facts, rules,
recursive rules, and a knowledge base that changes while you query it. At the end, you add a
predicate written in Python. It assumes you have read [Getting started](getting-started.md).

## Facts

Start with the facts: who is whose parent, and who is male or female.

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> from tuprolog.theory.parsing import parse_theory
>>> facts = parse_theory("""
...     parent(abe, homer).    parent(mona, homer).
...     parent(homer, bart).   parent(marge, bart).
...     parent(homer, lisa).   parent(marge, lisa).
...     parent(homer, maggie). parent(marge, maggie).
...     male(abe). male(homer). male(bart).
...     female(mona). female(marge). female(lisa). female(maggie).
... """)
>>> solver = prolog_solver(static_kb=facts)
>>> [answer["X"] for answer in solver.query("female(X)")]
['mona', 'marge', 'lisa', 'maggie']

```

## Rules

A *rule* `Head :- Body` states that `Head` is true whenever `Body` is. Variables in a rule are
universally quantified: `father(X, Y) :- parent(X, Y), male(X).` reads "for all `X` and `Y`, `X` is
the father of `Y` if `X` is a parent of `Y` and `X` is male".

```pycon
>>> rules = parse_theory("""
...     father(X, Y) :- parent(X, Y), male(X).
...     mother(X, Y) :- parent(X, Y), female(X).
...     sibling(X, Y) :- parent(P, X), parent(P, Y), X \\== Y.
... """)
>>> solver = prolog_solver(static_kb=facts + rules)
>>> list(solver.query("father(F, lisa)"))
[{'F': 'homer'}]
>>> list(solver.query("mother(marge, C)"))
[{'C': 'bart'}, {'C': 'lisa'}, {'C': 'maggie'}]

```

(`\\==` is Prolog's `\==`, "not identical", doubled because it sits in a Python string.)

## Backtracking

To answer `sibling(bart, S)`, the solver tries the clauses and the facts in order, and *backtracks*
to the last choice whenever a goal fails, or whenever you ask for the next solution. As Bart has two
parents, each sibling is found twice, once through each parent:

```pycon
>>> [answer["S"] for answer in solver.query("sibling(bart, S)")]
['lisa', 'maggie', 'lisa', 'maggie']

```

Collect the distinct answers into a list with Prolog's `setof/3` (`S` is only a placeholder there,
so it is not part of the solution):

```pycon
>>> list(solver.query("setof(S, sibling(bart, S), Siblings)"))
[{'Siblings': ['lisa', 'maggie']}]

```

## Recursion

Rules may refer to themselves. An ancestor is a parent, or a parent of an ancestor:

```pycon
>>> ancestors = parse_theory("""
...     ancestor(X, Y) :- parent(X, Y).
...     ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
... """)
>>> solver = prolog_solver(static_kb=facts + rules + ancestors)
>>> list(solver.query("setof(A, ancestor(A, maggie), As)"))
[{'As': ['homer', 'marge', 'abe', 'mona']}]
>>> list(solver.query("ancestor(abe, D)", limit=2))  # just the first two descendants
[{'D': 'homer'}, {'D': 'bart'}]

```

## A knowledge base that changes

Clauses in the *static* knowledge base cannot change while the solver runs. Clauses in the
*dynamic* one can: `assertz/1` adds a clause at the end, `asserta/1` at the beginning, and
`retract/1` removes the first clause matching its argument. Keep the facts about birth years in the
dynamic knowledge base:

```pycon
>>> years = parse_theory("born(bart, 1980). born(lisa, 1982).")
>>> solver = prolog_solver(static_kb=facts + rules, dynamic_kb=years)
>>> solver.solve_once("assertz(born(maggie, 1988))").is_yes
True
>>> list(solver.query("born(Who, Year), Year > 1981"))
[{'Who': 'lisa', 'Year': 1982}, {'Who': 'maggie', 'Year': 1988}]
>>> solver.solve_once("retract(born(bart, _))").is_yes
True
>>> [answer["Who"] for answer in solver.query("born(Who, _)")]
['lisa', 'maggie']

```

Changing a static predicate is an error, which halts the query:

```pycon
>>> solver.solve_once("assertz(male(clancy))").exception.type
permission_error(modify, static_procedure, male/1)

```

## Arithmetic

`is/2` evaluates arithmetic expressions; comparisons such as `>/2` and `=</2` compare numbers:

```pycon
>>> list(solver.query("born(lisa, Y), Age is 2026 - Y"))
[{'Y': 1982, 'Age': 44}]

```

## A predicate written in Python

Some predicates are easier to write in Python. `tuprolog.solve.primitive.predicate` turns a Python
function into a predicate: its arguments are converted into Python values, and it returns `True` or
`False`, or the tuples of argument values making the goal true. Put it in a *library*, and give the
library to the solver:

```pycon
>>> from tuprolog.solve.library import library
>>> from tuprolog.solve.primitive import predicate
>>> def initial(name, _):
...     return [(name, name[0].upper())]
>>> names = library("names", primitives={"initial/2": predicate(initial)})
>>> solver = prolog_solver(static_kb=facts + rules, libraries=names)
>>> list(solver.query("mother(M, lisa), initial(M, I)"))
[{'M': 'marge', 'I': 'M'}]

```

## What you learned

- facts and rules make a knowledge base, which solvers query;
- solvers find solutions by trying clauses in order and backtracking;
- the dynamic knowledge base changes during resolution, the static one does not;
- Python functions can be predicates.

Read on:

- [Logic programming in a nutshell](../explanation/logic-programming.md), for the theory behind
  this tutorial;
- [Define predicates in Python](../how-to/define-predicates-in-python.md), for more on predicates,
  functions and libraries;
- [Standard predicates](../reference/standard-predicates.md), for the built-in predicates such as
  `setof/3` and `assertz/1`.
