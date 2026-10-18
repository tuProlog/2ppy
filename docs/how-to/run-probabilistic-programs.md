# Run probabilistic programs

[ProbLog](https://dtai.cs.kuleuven.be/problog/) extends logic programming with probabilities:
clauses may be annotated as `P::Clause`, meaning that the clause holds with probability `P`,
independently of the others. A ProbLog solver computes, for each solution of a query, the
probability that it holds. This guide shows how to run ProbLog programs with 2PPy.

## Parse probabilistic clauses

The `::` operator is not part of standard Prolog: parse ProbLog programs with
`tuprolog.solve.problog.PROBLOG_OPERATORS`:

```pycon
>>> from tuprolog.solve.problog import PROBLOG_OPERATORS, problog_solver
>>> from tuprolog.theory.parsing import parse_theory
>>> graph = parse_theory(
...     """
...     0.6::edge(a, b).
...     0.7::edge(b, c).
...     0.4::edge(a, c).
...     path(X, Y) :- edge(X, Y).
...     path(X, Y) :- edge(X, Z), path(Z, Y).
... """,
...     PROBLOG_OPERATORS,
... )

```

Here each edge of a graph exists with some probability, while `path/2` is an ordinary rule.

## Compute probabilities

Create a solver with `problog_solver` (it takes the same arguments as `prolog_solver`), and solve
queries with the `probabilistic=True` option. `tuprolog.solve.plp.probability` reads the probability
of each solution:

```pycon
>>> from tuprolog.solve import solve_options
>>> from tuprolog.solve.plp import probability
>>> solver = problog_solver(static_kb=graph)
>>> for solution in solver.solve("path(a, X)", solve_options(probabilistic=True)):
...     print(solution.solved_query, round(probability(solution), 3))
path(a, b) 0.6
path(a, c) 0.652

```

`path(a, c)` holds if the direct edge exists, or if both `a-b` and `b-c` do: 0.4 + 0.6 × 0.7 −
0.4 × 0.6 × 0.7 = 0.652. ProbLog solutions are distinct: each answer appears once, with the
probability of all its proofs combined.

!!! note
    Use `solve`, not `solve_once`: the first solution of `solve_once` accounts only for the first
    proof (here, 0.4 for `path(a, c)`).

Without `probabilistic=True`, a ProbLog solver behaves as a Prolog one, enumerating proofs:

```pycon
>>> list(solver.query("path(a, X)"))
[{'X': 'b'}, {'X': 'c'}, {'X': 'c'}]

```

## Probabilistic facts with alternative explanations

A goal provable in several ways is more likely than each way alone:

```pycon
>>> weather = parse_theory(
...     """
...     0.3::rain.
...     0.4::sprinkler.
...     wet :- rain.
...     wet :- sprinkler.
... """,
...     PROBLOG_OPERATORS,
... )
>>> solver = problog_solver(static_kb=weather)
>>> [round(probability(s), 2) for s in solver.solve("wet", solve_options(probabilistic=True))]
[0.58]

```

## Inspect the decision diagrams

Probabilistic solutions carry the *binary decision diagram* (BDD) ProbLog built to compute their
probability, available via `tuprolog.solve.plp.binary_decision_diagram`.

## Use the ProbLog REPL

`python -m tuprolog.repl.problog` opens an interactive ProbLog shell, printing the probability of
each solution: see [Use the REPL](use-the-repl.md).

## See also

- API: `tuprolog.solve.problog` ([reference](../api/tuprolog/solve/problog.md)),
  `tuprolog.solve.plp` ([reference](../api/tuprolog/solve/plp.md)).
- The [ProbLog website](https://dtai.cs.kuleuven.be/problog/), for the language.
