# Explanation

Understanding-oriented discussions: the ideas behind logic programming, and why 2PPy works the
way it does. Read them to build a mental model; for step-by-step instructions, see the
[how-to guides](../how-to/index.md), and for exact behaviour, the [reference](../reference/index.md).

- [Logic programming in a nutshell](logic-programming.md): terms, clauses, unification,
  resolution, backtracking, cut and negation, for Python developers.
- [Terms and variables](terms-and-variables.md): immutability, the identity of variables,
  scopes, substitutions.
- [Solvers and solutions](solvers-and-solutions.md): what a solver is made of, and how it
  produces solutions.
- [Architecture](architecture.md): how 2PPy wraps 2P-Kt, running on the JVM, behind a Pythonic
  API.
- [Relationship with 2P-Kt](relationship-with-2p-kt.md): how 2PPy's packages map onto 2P-Kt's
  modules, and what is (not) exposed.

2P-Kt's own [explanation pages](https://tuprolog.github.io/2p-kt/explanation/) go deeper into the
engine's internals, e.g. its [solver design](https://tuprolog.github.io/2p-kt/explanation/solver-design/)
and [clause database](https://tuprolog.github.io/2p-kt/explanation/clause-db-and-rete/).
