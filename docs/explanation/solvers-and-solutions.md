# Solvers and solutions

A **solver** answers queries against a logic program. This page explains what a solver is made
of, how it produces solutions, and the kinds of solutions it produces. The API lives in
[`tuprolog.solve`](../api/tuprolog/solve.md); Prolog solvers are made by
[`tuprolog.solve.prolog.prolog_solver`](../api/tuprolog/solve/prolog.md), ProbLog ones by
[`tuprolog.solve.problog.problog_solver`](../api/tuprolog/solve/problog.md).

## Anatomy of a solver

| Part | What it is | Factory argument | Read it with |
|---|---|---|---|
| static knowledge base | a theory of clauses that programs cannot change | `static_kb` | `solver.static_kb` |
| dynamic knowledge base | a theory of clauses that `assertz/1`, `retract/1`, ... change while solving | `dynamic_kb` | `solver.dynamic_kb` |
| libraries | the predicates, functions, clauses and operators available besides the knowledge bases: by default, the standard library | `libraries` | `solver.libraries` |
| flags | named settings, e.g. what calling an unknown predicate does | `flags` | `solver.flags` |
| operators | the operators used to parse goals and clauses, from libraries and `op/3` directives | | `solver.operators` |
| channels | standard input, output, error, and warnings | `std_in`, `std_out`, `std_err`, `warning` | `solver.standard_output`, ... |
| unificator | the unification algorithm | `unificator` | `solver.unificator` |

Goals are solved against the libraries' clauses and primitives, then the static and the dynamic
knowledge bases. The two knowledge bases differ in who can change them: a static predicate (one
with clauses in `static_kb`) cannot be modified by Prolog code, which gets a
`permission_error` trying; the dynamic one is what `assertz/1` and `retract/1` operate on.

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> from tuprolog.theory.parsing import parse_theory
>>> solver = prolog_solver(
...     static_kb=parse_theory("parent(abe, homer)."), dynamic_kb=parse_theory("counter(0).")
... )
>>> solver.solve_once("assertz(parent(homer, bart))").exception.type
permission_error(modify, static_procedure, parent/2)
>>> list(solver.query("retract(counter(N)), M is N + 1, assertz(counter(M))"))
[{'N': 0, 'M': 1}]
>>> solver.dynamic_kb
MutableIndexedTheory{ counter(1) :- true }

```

Solvers are **mutable** by default (`MutableSolver`): Python code can also load clauses
(`load_static_clauses`, `load_dynamic_clauses`, `load_static_kb`, ...), libraries
(`load_library`), and change flags (`set_flag`) between queries. `prolog_solver(mutable=False)`
makes an immutable `Solver`, whose configuration is fixed at creation.

!!! note
    Assigning the standard channels of an existing solver (e.g. `solver.standard_output = ...`)
    currently has no effect on what Prolog code writes (a 2P-Kt issue): pass channels to the
    factory instead.

## Solutions are produced lazily

Solving a goal is a search (see [Logic programming in a nutshell](logic-programming.md)): there
can be zero, one, many, or infinitely many solutions. `solver.solve(goal)` returns an iterator
which runs the search only as far as needed to produce the next solution, so goals with infinitely
many solutions are fine as long as you stop asking:

```pycon
>>> from itertools import islice
>>> solver = prolog_solver(static_kb=parse_theory("nat(0). nat(N) :- nat(M), N is M + 1."))
>>> [s["N"] for s in islice(solver.solve("nat(N)"), 4)]
[0, 1, 2, 3]

```

**Solve options** ([`solve_options`](../api/tuprolog/solve.md)) tune a resolution:

| Option | Meaning |
|---|---|
| `lazy=True` | iterate lazily; with `lazy=False`, `solve` computes all solutions and returns a list |
| `limit` | at most this many solutions |
| `timeout` | at most this many milliseconds; a resolution running out of time ends with a halt solution (`TimeOutException`) |

```pycon
>>> from tuprolog.solve import solve_options
>>> solver.solve("nat(N)", solve_options(lazy=False, limit=3))
[Yes(query=nat(N_...), substitution={N_...=0}), Yes(...), Yes(...)]

```

Shortcuts: `solver.solve_once(goal)` gives the first solution only, and `solver.query(goal,
limit=..., timeout=...)` yields the bindings of each successful solution as dictionaries of
Python values (see [Query solvers](../how-to/query-solvers.md)).

## Kinds of solutions

Each `Solution` is one of three kinds:

| Kind | Meaning | `bool(solution)` | Carries |
|---|---|---|---|
| **yes** (`is_yes`) | the goal succeeded | `True` | `substitution`: the bindings of the query's variables; `solved_query`: the query with them applied |
| **no** (`is_no`) | the goal failed (no more solutions) | `False` | |
| **halt** (`is_halt`) | the resolution stopped: an uncaught error, `halt/0,1`, or a timeout | `False` | `exception`: the reason |

A sequence of solutions ends with either the last *yes* (when the solver knows there are no more
alternatives), a *no* (after the last *yes*, when the solver finds out only by searching), or a
*halt*. `solve` and `solve_once` never raise for errors in the goal:
they return halt solutions, and `solution.raise_error()` raises their exception. `query` raises
it instead.

```pycon
>>> list(solver.solve("member(X, [a, b])"))
[Yes(query=member(X_..., [a, b]), substitution={X_...=a}),
 Yes(query=member(X_..., [a, b]), substitution={X_...=b}),
 No(query=member(X_..., [a, b]))]
>>> list(solver.solve("member(c, [a, b])"))
[No(query=member(c, [a, b]))]
>>> solution = solver.solve_once("atom_length(X, 3)")
>>> solution.is_halt, solution.exception.type
(True, instantiation_error)

```

## ProbLog solvers

`problog_solver()` makes solvers for ProbLog, a probabilistic extension of Prolog: clauses may be
annotated with probabilities (`0.6::heads(coin).`), and, with the `probabilistic` solve option, each
solution carries the probability that the query is true in a random world drawn from the annotated
clauses (see [`tuprolog.solve.plp.probability`](../api/tuprolog/solve/plp.md)). Parse ProbLog
programs with its operators (`PROBLOG_OPERATORS`), which add `::`:

```pycon
>>> from tuprolog.solve.plp import probability
>>> from tuprolog.solve.problog import PROBLOG_OPERATORS, problog_solver
>>> coins = parse_theory(
...     "0.6::heads(c1). 0.5::heads(c2). two :- heads(c1), heads(c2).", PROBLOG_OPERATORS
... )
>>> [
...     probability(s)
...     for s in problog_solver(static_kb=coins).solve("two", solve_options(probabilistic=True))
... ]
[0.3]

```

Probabilities combine all the proofs of a query, so use `solve`: `solve_once` stops at the first
proof. See [Run probabilistic programs](../how-to/run-probabilistic-programs.md).

## See also

- [Standard predicates](../reference/standard-predicates.md), what default solvers can do.
- 2P-Kt's [solver API](https://tuprolog.github.io/2p-kt/reference/solver-api/),
  [solver design](https://tuprolog.github.io/2p-kt/explanation/solver-design/) and
  [state machine](https://tuprolog.github.io/2p-kt/explanation/state-machine/).
