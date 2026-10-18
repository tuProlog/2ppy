# Getting started

In this tutorial you install 2PPy, load a few facts into a Prolog solver, and query it from Python
in the three ways the API offers.

## Install 2PPy

2PPy requires Python 3.10 or later. Install it from [PyPI](https://pypi.org/project/2ppy/):

```bash
pip install 2ppy        # or: uv add 2ppy
```

That is all: the package ships 2P-Kt's JARs, and depends on
[`jdk4py`](https://pypi.org/project/jdk4py/), which bundles a Java runtime. You need no Java
installation.

## Import it

```pycon
>>> import tuprolog
>>> tuprolog.__version__  # doctest: +SKIP
'1.5.0'

```

The first import of `tuprolog` starts a Java virtual machine (JVM) in the background, where 2P-Kt,
the logic engine 2PPy wraps, runs. It takes a second or two, and happens once per Python process:
later imports are instant. [Architecture](../explanation/architecture.md) explains how Python and
the JVM cooperate.

## Write a knowledge base

A Prolog program is a *knowledge base*: a collection of *clauses* stating what is true. The
simplest clauses are *facts*. Parse some from text:

```pycon
>>> from tuprolog.theory.parsing import parse_theory
>>> kb = parse_theory("""
...     parent(abe, homer).
...     parent(homer, bart).
...     parent(homer, lisa).
... """)
>>> len(kb)
3

```

`parent(abe, homer)` reads "Abe is a parent of Homer": `parent` is a *predicate* (a relation)
and `abe` and `homer` are *atoms* (symbolic constants). Each clause ends with a full stop.

## Create a solver

A *solver* answers questions (*queries*, or *goals*) about a knowledge base. Create a Prolog one,
giving it the facts as its *static* knowledge base:

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> solver = prolog_solver(static_kb=kb)

```

## Ask queries

A query is a term, possibly containing *variables*, i.e. names starting with an uppercase letter
(or `_`), which stand for unknown terms. The solver finds the values of the variables that make
the query true, one *solution* at a time.

### `query`: the Pythonic way

`solver.query(goal)` yields, for each solution, a dictionary from variable names to Python values:

```pycon
>>> for answer in solver.query("parent(homer, Child)"):
...     print(answer)
{'Child': 'bart'}
{'Child': 'lisa'}
>>> list(solver.query("parent(Parent, bart)"))
[{'Parent': 'homer'}]
>>> list(solver.query("parent(bart, Child)"))  # no solutions
[]

```

Queries with no variables are yes-or-no questions: they have one solution (an empty dictionary)
when true, none when false.

```pycon
>>> list(solver.query("parent(abe, homer)"))
[{}]

```

Queries can be conjunctions of goals, separated by commas, sharing variables: "who is a
grandparent of Bart?"

```pycon
>>> list(solver.query("parent(G, P), parent(P, bart)"))
[{'G': 'abe', 'P': 'homer'}]

```

### `solve_once`: the first solution

`solver.solve_once(goal)` returns the first `Solution`. It is truthy if the query succeeded, and
maps variable names to the *terms* bound to them (not to Python values):

```pycon
>>> solution = solver.solve_once("parent(abe, Who)")
>>> bool(solution), solution.is_yes
(True, True)
>>> solution["Who"]
homer
>>> solution.solved_query
parent(abe, homer)
>>> solution.to_dict()
{'Who': 'homer'}
>>> bool(solver.solve_once("parent(lisa, _)"))
False

```

### `solve`: every solution

`solver.solve(goal)` iterates over all the `Solution`s. Unlike `query`, it does not hide failures
and errors: each solution is a *yes*, a *no* (the query has no more solutions), or a *halt* (an
error stopped the resolution).

```pycon
>>> for solution in solver.solve("parent(homer, C)"):
...     print(solution.is_yes, solution.to_dict())
True {'C': 'bart'}
True {'C': 'lisa'}
>>> halted = solver.solve_once("X is foo + 1")  # foo is not a number
>>> halted.is_halt
True
>>> halted.exception.type
type_error(evaluable, foo/0)

```

`query`, instead, raises errors as Python exceptions (see
[Handle errors](../how-to/handle-errors.md)).

## What's next

- Continue with [Your first logic program](your-first-logic-program.md), which writes rules and
  changes the knowledge base while querying it.
- See [Query solvers](../how-to/query-solvers.md) for the options of a query (limits, timeouts).
- See [Solvers and solutions](../explanation/solvers-and-solutions.md) for what happens behind
  `query`, `solve_once` and `solve`.
