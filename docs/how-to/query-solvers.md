# Query solvers

This guide shows how to create solvers, fill their knowledge bases, and control how queries are
solved. For the concepts (solutions, laziness, the two knowledge bases), see
[Solvers and solutions](../explanation/solvers-and-solutions.md).

## Create a solver

`tuprolog.solve.prolog.prolog_solver` creates a Prolog solver. All its arguments are optional:

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> from tuprolog.theory.parsing import parse_theory
>>> solver = prolog_solver(
...     static_kb=parse_theory("nat(0). nat(s(X)) :- nat(X). loop :- loop."),
...     dynamic_kb=parse_theory("counter(0)."),
... )

```

| Argument | Purpose |
|----------|---------|
| `static_kb` | clauses queries cannot change |
| `dynamic_kb` | clauses `assertz/1`, `retract/1` & co. change |
| `libraries` | extra predicates and functions (see [Define predicates in Python](define-predicates-in-python.md)) |
| `flags` | settings such as `unknown` (see [below](#set-flags)) |
| `std_in`, `std_out`, `std_err`, `warning` | input and output (see [Read and write streams](read-and-write-streams.md)) |
| `mutable` | whether the solver can be reconfigured after creation (the default) |

## Choose how to get solutions

| Method | Returns | On errors |
|--------|---------|-----------|
| `solver.query(goal)` | an iterator of dicts, variable names to Python values, one per *yes* | raises the error |
| `solver.solve_once(goal)` | the first `Solution` | returns a *halt* solution |
| `solver.solve(goal, options)` | an iterator (or a list, if eager) of `Solution`s | ends with a *halt* solution |

Goals are strings (parsed with the solver's current operators) or terms:

```pycon
>>> from tuprolog.core import struct, var
>>> list(solver.query("counter(N)"))
[{'N': 0}]
>>> solver.solve_once(struct("counter", var("N"))).to_dict()
{'N': 0}

```

## Limit the number of solutions

Queries may have infinitely many solutions: `nat(X)` enumerates all natural numbers. Solutions are
computed lazily, so take just the ones you need, or pass a `limit`:

```pycon
>>> list(solver.query("nat(X)", limit=3))
[{'X': 0}, {'X': s(0)}, {'X': s(s(0))}]
>>> from itertools import islice
>>> [answer["X"] for answer in islice(solver.query("nat(X)"), 2)]
[0, s(0)]

```

## Set a timeout

A `timeout` (in milliseconds) stops queries running too long: `query` raises a
`tuprolog.errors.TimeOutError`, while `solve` and `solve_once` return a *halt* solution.

```pycon
>>> from tuprolog.errors import TimeOutError
>>> try:
...     list(solver.query("loop", timeout=100))
... except TimeOutError:
...     print("timed out")
timed out

```

## Use solve options

`tuprolog.solve.solve_options` bundles the options of `solve` and `solve_once`: `lazy` (the
default) or eager (all solutions computed at once, returned as a list), `timeout`, and `limit`:

```pycon
>>> from tuprolog.solve import solve_options
>>> solutions = solver.solve("nat(X)", solve_options(lazy=False, limit=2))
>>> [s.to_dict() for s in solutions]
[{'X': 0}, {'X': s(0)}]
>>> solver.solve_once("loop", solve_options(timeout=100)).is_halt
True

```

## Change the knowledge bases

Prolog code changes the dynamic knowledge base with `assertz/1`, `asserta/1`, `retract/1` and
`retractall/1`:

```pycon
>>> list(solver.query("retract(counter(N)), M is N + 1, assertz(counter(M))"))
[{'N': 0, 'M': 1}]
>>> solver.solve_once("counter(N)")["N"]
1

```

Python code changes both knowledge bases of a (mutable) solver between queries: `append_static_kb`
and `append_dynamic_kb` add clauses, `load_static_kb` and `load_dynamic_kb` replace them all, and
`assert_z` (or `assert_a`) adds one clause to the dynamic knowledge base:

```pycon
>>> solver.append_static_kb(parse_theory("even(0). even(s(s(X))) :- even(X)."))
>>> solver.solve_once("even(s(s(0)))").is_yes
True
>>> from tuprolog.core.parsing import parse_struct
>>> solver.assert_z(parse_struct("counter(10)"))
>>> [answer["N"] for answer in solver.query("counter(N)")]
[1, 10]
>>> len(solver.static_kb), len(solver.dynamic_kb)
(5, 2)

```

## Set flags

*Flags* configure a solver, e.g. `unknown` says what calling an undefined predicate does
(`error`, `warning` or `fail`). Pass them to the factory with `tuprolog.solve.flags.flag_store`;
Prolog code reads and changes them with `current_prolog_flag/2` and `set_prolog_flag/2`:

```pycon
>>> from tuprolog.solve.flags import DEFAULT_FLAG_STORE, flag_store
>>> strict = prolog_solver(flags=flag_store(DEFAULT_FLAG_STORE, unknown="error"))
>>> strict.solve_once("undefined_predicate").exception.type
existence_error(procedure, undefined_predicate/0)
>>> lenient = prolog_solver(flags=flag_store(DEFAULT_FLAG_STORE, unknown="fail"))
>>> lenient.solve_once("undefined_predicate").is_no
True

```

## Define operators

Operators are declared by `op/3` directives or goals; the solver then parses goals and clauses with
them:

```pycon
>>> solver.solve_once("op(700, xfx, likes)").is_yes
True
>>> solver.solve_once("X = (bart likes skateboarding), X =.. L")["L"]
[likes, bart, skateboarding]

```

## Solve probabilistic queries

Probabilistic solvers (ProbLog) take the same options, plus `probabilistic=True`: see
[Run probabilistic programs](run-probabilistic-programs.md).

## See also

- Example notebook: [Knowledge bases and queries](../examples/02-knowledge-bases-and-queries.ipynb).
- API: `tuprolog.solve` ([reference](../api/tuprolog/solve.md)),
  `tuprolog.solve.prolog` ([reference](../api/tuprolog/solve/prolog.md)),
  `tuprolog.solve.flags` ([reference](../api/tuprolog/solve/flags.md)).
- [Standard predicates](../reference/standard-predicates.md).
- 2P-Kt's [solver API](https://tuprolog.github.io/2p-kt/reference/solver-api/).
