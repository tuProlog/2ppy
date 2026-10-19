# 2PPy: tuProlog for Python

2PPy brings [tuProlog](https://github.com/tuProlog/2p-kt) (2P-Kt) to Python: an object-oriented,
modular ecosystem for **symbolic AI** and **logic programming**. It lets Python programs represent
knowledge as logic terms and clauses, reason over it with Prolog (or ProbLog) solvers, and mix
logic and Python code freely in both directions.

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> from tuprolog.theory.parsing import parse_theory
>>> solver = prolog_solver(
...     static_kb=parse_theory("""
...     parent(abe, homer). parent(homer, bart). parent(homer, lisa).
...     ancestor(X, Y) :- parent(X, Y).
...     ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
... """)
... )
>>> [answer["D"] for answer in solver.query("ancestor(abe, D)")]
['homer', 'bart', 'lisa']

```

No knowledge of 2P-Kt, Kotlin or Java is needed, and no Java installation either:
`pip install 2ppy` (Python 3.10 or later) ships everything, Java runtime included.

## What 2PPy offers

| Capability | What it means | Where to start |
|------------|---------------|----------------|
| **Logic terms** | Build, parse, inspect and format atoms, numbers, variables, compound terms, lists, clauses; convert them from and to Python values | [Build and parse terms](how-to/build-and-parse-terms.md) |
| **Unification** | Compute the substitutions making two terms equal, the core operation of logic programming | [Terms and variables](explanation/terms-and-variables.md) |
| **Theories** | Store clauses in indexed, immutable or mutable knowledge bases | [Your first logic program](tutorials/your-first-logic-program.md) |
| **Prolog solving** | Answer queries with an ISO-compliant Prolog engine, getting answers as Python dicts and errors as Python exceptions | [Query solvers](how-to/query-solvers.md) |
| **Probabilistic solving** | Compute the probability of queries over ProbLog programs | [Run probabilistic programs](how-to/run-probabilistic-programs.md) |
| **Python extensions** | Define predicates and arithmetic functions as plain Python functions | [Define predicates in Python](how-to/define-predicates-in-python.md) |
| **Python objects from Prolog** | Let Prolog code create Python objects and call their methods (OOPLib) | [Use Python objects from Prolog](how-to/use-python-objects-from-prolog.md) |
| **Input/output** | Use Python streams (files, `io.StringIO`, `sys.stdout`) wherever logic code reads or writes | [Read and write streams](how-to/read-and-write-streams.md) |
| **Interactive use** | Prolog and ProbLog REPLs, and a Python shell with the whole API loaded | [Use the REPL](how-to/use-the-repl.md) |
| **Terminal IDE** | Edit theories and solve queries in a terminal user interface, page by page; installed with 2PPy, or run with Docker | [Use the terminal IDE](how-to/use-the-terminal-ide.md), [How it works](explanation/terminal-ide.md) |

## How it works

2PPy is a thin, Pythonic layer over 2P-Kt, the Kotlin implementation of tuProlog, which runs on a
Java virtual machine (JVM) started, once per process, when `tuprolog` is first imported:

```text
 your Python code
       │  Pythonic API: snake_case factories, Python protocols, value conversions
       ▼
 tuprolog (2PPy) ── JPype bridge ──▶ 2P-Kt on the JVM (terms, unification, solvers, libraries)
```

Logic is implemented once, in 2P-Kt, and wrapped: 2PPy adds factories with Python defaults,
conversions between Python values and terms, Python protocols on JVM objects (iteration, indexing,
`len`, `in`, operators), Python exception classes for 2P-Kt's errors, and Python-friendly ways to
extend solvers. See [Architecture](explanation/architecture.md) for details.

The package mirrors 2P-Kt's modules:

| Package | Content |
|---------|---------|
| [`tuprolog.core`](api/tuprolog/core.md) | terms and clauses; [parsing](api/tuprolog/core/parsing.md) and [operators](api/tuprolog/core/operators.md) |
| [`tuprolog.unify`](api/tuprolog/unify.md) | unification and substitutions |
| [`tuprolog.theory`](api/tuprolog/theory.md) | theories (knowledge bases) and their [parsing](api/tuprolog/theory/parsing.md) |
| [`tuprolog.solve`](api/tuprolog/solve.md) | the solver API, the [Prolog](api/tuprolog/solve/prolog.md) and [ProbLog](api/tuprolog/solve/problog.md) solvers, primitives, libraries, flags, channels |
| [`tuprolog.errors`](api/tuprolog/errors.md) | Python exception classes for 2P-Kt's errors |
| [`tuprolog.repl`](api/tuprolog/repl.md) | the REPLs |
| [`tuprolog.gui`](api/tuprolog/gui.md) and [`tuprolog.tui`](api/tuprolog/tui.md) | the core of tuProlog's IDEs, and the terminal IDE |

The [package map](reference/package-map.md) lists every module.

## How this documentation is organized

Following the [Divio documentation system](https://docs.divio.com/documentation-system/), as
2P-Kt's documentation does:

- **[Tutorials](tutorials/index.md)**: learning by doing, from installation to a first logic
  program;
- **[How-to guides](how-to/index.md)**: recipes for specific tasks;
- **[Examples](examples/index.md)**: Jupyter notebooks showing 2PPy at work;
- **[Reference](reference/index.md)**: precise descriptions, including the
  [API reference](api/tuprolog.md) generated from the docstrings;
- **[Explanation](explanation/index.md)**: background and design, from logic programming basics to
  how 2PPy wraps 2P-Kt.

Every example in this documentation, notebooks included, is run by the test suite.

## Project

2PPy is developed by the [tuProlog](https://github.com/tuProlog) team, under the
[Apache License 2.0](https://github.com/tuProlog/2ppy/blob/master/LICENSE), on
[GitHub](https://github.com/tuProlog/2ppy), and released on [PyPI](https://pypi.org/project/2ppy/).
It is in **alpha**: its API may still change between minor versions. Contributions are welcome: see
[Contribute](how-to/contribute.md).
