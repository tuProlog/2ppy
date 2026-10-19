# Relationship with 2P-Kt

[2P-Kt](https://github.com/tuProlog/2p-kt) is tuProlog's engine, written in Kotlin and split into
modules (see its [module map](https://tuprolog.github.io/2p-kt/reference/module-map/)). 2PPy
wraps a subset of them (see [Architecture](architecture.md)), mirroring their structure: each 2P-Kt
module becomes a `tuprolog` package, and each Kotlin package of it a Python sub-package.

## Module mapping

| 2P-Kt module | Kotlin package | 2PPy package |
|---|---|---|
| `core` | `it.unibo.tuprolog.core` | [`tuprolog.core`](../api/tuprolog/core.md), [`tuprolog.core.operators`](../api/tuprolog/core/operators.md), [`tuprolog.math`](../api/tuprolog/math.md) |
| `parser-core`, `parser-impl` | `it.unibo.tuprolog.core.parsing` | [`tuprolog.core.parsing`](../api/tuprolog/core/parsing.md) |
| `unify` | `it.unibo.tuprolog.unify` | [`tuprolog.unify`](../api/tuprolog/unify.md) |
| `theory` | `it.unibo.tuprolog.theory`, `it.unibo.tuprolog.collections` | [`tuprolog.theory`](../api/tuprolog/theory.md), [`tuprolog.collections`](../api/tuprolog/collections.md) |
| `parser-theory` | `it.unibo.tuprolog.theory.parsing` | [`tuprolog.theory.parsing`](../api/tuprolog/theory/parsing.md) |
| `solve` | `it.unibo.tuprolog.solve` (and sub-packages) | [`tuprolog.solve`](../api/tuprolog/solve.md) and its sub-packages (`channel`, `flags`, `library`, `primitive`, `function`, `exception`, `sideffects`, `data`, `stdlib`) |
| `solve-prolog` | `it.unibo.tuprolog.solve.prolog` | [`tuprolog.solve.prolog`](../api/tuprolog/solve/prolog.md) |
| `solve-plp` | `it.unibo.tuprolog.solve` (probabilistic extensions) | [`tuprolog.solve.plp`](../api/tuprolog/solve/plp.md) |
| `solve-problog` | `it.unibo.tuprolog.solve.problog` | [`tuprolog.solve.problog`](../api/tuprolog/solve/problog.md) |
| `io-lib` | `it.unibo.tuprolog.solve.libs.io` | `IOLib` in [`tuprolog.solve.libs`](../api/tuprolog/solve/libs.md) |
| `oop-lib` | `it.unibo.tuprolog.solve.libs.oop` | re-implemented for Python objects: `OOPLib` in [`tuprolog.solve.libs`](../api/tuprolog/solve/libs.md) |
| `repl` | `it.unibo.tuprolog.ui.repl` | re-implemented in Python: [`tuprolog.repl`](../api/tuprolog/repl.md) |
| `utils` | `it.unibo.tuprolog.utils` | [`tuprolog.utils`](../api/tuprolog/utils.md) (some interfaces) |

OOPLib and the REPL are the two exceptions to "wrap, don't re-implement": 2P-Kt's OOPLib drives
JVM objects, whereas Prolog code run from Python wants to drive Python objects, and a REPL is a
user interface, best written for its platform. Both keep 2P-Kt's Prolog API and behaviour.

## Not exposed

These 2P-Kt modules have no 2PPy counterpart: `solve-concurrent` (a parallel solver), `datalog`,
`serialize-core` and `serialize-theory` (term serialization), the Kotlin DSL (`dsl-*`, replaced
by Python factories and parsing), the GUIs and IDEs (`gui`, `ide-*`), and the test suites. Some of
their JARs ship as dependencies of the wrapped modules, and their classes are reachable through
JPype (`import it.unibo.tuprolog...` after importing `tuprolog`), but without a Pythonic API.

## Naming differences

| 2P-Kt (Kotlin) | 2PPy (Python) |
|---|---|
| companion factories: `Atom.of("a")`, `Struct.of("f", ...)`, `Var.of("X")` | functions: `atom("a")`, `struct("f", ...)`, `var("X")` (the JVM factories remain available) |
| solver factories: `Solver.prolog.solverWithDefaultBuiltins(...)` | `prolog_solver(...)`, with keyword arguments and defaults |
| methods in `camelCase`: `term.freshCopy()`, `solver.solveOnce(goal)` | also `snake_case`: `term.fresh_copy()`, `solver.solve_once(goal)` |
| properties: `term.arity`, `term.isGround` (Kotlin), `getArity()`, `isGround()` (JVM) | properties: `term.arity`, `term.is_ground` |
| `Solver.solve(goal)` returns a Kotlin `Sequence` | iterable from Python; goals may also be strings |
| `List.of(...)`, `Tuple.of(...)` | `logic_list(...)`, `logic_tuple(...)` (not to shadow Python's `list` and `tuple`) |
| `TypeError`, `SystemError`, ... in `solve.exception.error` | same names in `tuprolog.solve.exception.error.*`, classified by `PrologTypeError`, `PrologSystemError`, ... in `tuprolog.errors` (see [Exceptions](../reference/exceptions.md)) |
| `IOLib`, `OOPLib` objects | `IOLib`, `OOPLib` (and `oop_lib(...)`) in `tuprolog.solve.libs` |

Names that would shadow Python builtins (e.g. the JVM `TypeError`) remain importable by name, but
are left out of their packages' `__all__`, so that star imports do not shadow them.

## Versions

Each 2PPy release depends on one 2P-Kt version, declared in
[`jvm/gradle/libs.versions.toml`](https://github.com/tuProlog/2ppy/blob/master/jvm/gradle/libs.versions.toml):

```pycon
>>> import tuprolog
>>> str(tuprolog.Info.VERSION).startswith("3.")
True

```

## 2P-Kt documentation

2P-Kt's [documentation](https://tuprolog.github.io/2p-kt/) explains the engine's concepts in depth,
with Kotlin examples; its [API reference](https://tuprolog.github.io/2p-kt/api/) documents the JVM
types 2PPy exposes. Most relevant pages:

- [term hierarchy](https://tuprolog.github.io/2p-kt/reference/term-hierarchy/) and
  [term model](https://tuprolog.github.io/2p-kt/explanation/term-model/);
- [unification API](https://tuprolog.github.io/2p-kt/reference/unification-api/);
- [solver API](https://tuprolog.github.io/2p-kt/reference/solver-api/) and
  [solver design](https://tuprolog.github.io/2p-kt/explanation/solver-design/);
- [primitives and functions](https://tuprolog.github.io/2p-kt/reference/primitives-and-functions/),
  [libraries](https://tuprolog.github.io/2p-kt/reference/libraries/), and
  [default predicates](https://tuprolog.github.io/2p-kt/reference/default-predicates/);
- [I/O library](https://tuprolog.github.io/2p-kt/reference/io-lib/);
- [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
