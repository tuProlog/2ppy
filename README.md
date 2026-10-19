# 2PPy: tuProlog for Python

[![PyPI](https://img.shields.io/pypi/v/2ppy)](https://pypi.org/project/2ppy/)
[![Python](https://img.shields.io/pypi/pyversions/2ppy)](https://pypi.org/project/2ppy/)
[![CI/CD](https://github.com/tuProlog/2ppy/actions/workflows/check.yml/badge.svg)](https://github.com/tuProlog/2ppy/actions/workflows/check.yml)
[![Docs](https://img.shields.io/badge/docs-tuprolog.github.io%2F2ppy-blue)](https://tuprolog.github.io/2ppy/)
[![License](https://img.shields.io/github/license/tuProlog/2ppy)](https://github.com/tuProlog/2ppy/blob/master/LICENSE)

2PPy brings [tuProlog](https://github.com/tuProlog/2p-kt) (2P-Kt) to Python: logic terms,
unification, theories, Prolog and ProbLog solvers, predicates written in Python, and Prolog code
driving Python objects, through a Pythonic API over 2P-Kt (via [JPype](https://jpype.readthedocs.io)).

**Documentation: <https://tuprolog.github.io/2ppy/>**

## What to expect

- **It is a wrapper, not a re-implementation.** 2PPy wraps 2P-Kt's JVM implementation via JPype:
  importing `tuprolog` starts a Java Virtual Machine in the Python process. A Java runtime is
  installed automatically as a Python package ([jdk4py](https://pypi.org/project/jdk4py/)), so
  no Java installation is needed, but 2PPy fails at runtime if that JVM cannot start or work on
  your platform (e.g. unsupported architecture, restricted environments). The JVM can be started
  only once per Python process.
- **Bugs may be inherited from 2P-Kt.** Solving, parsing, and libraries are 2P-Kt's: if something
  behaves unexpectedly, the cause may lie upstream. Please report it
  [here](https://github.com/tuProlog/2ppy/issues) anyway; we will forward it to
  [2P-Kt](https://github.com/tuProlog/2p-kt/issues) when needed.
- **The API is meant to be Pythonic.** Snake-case names, keyword arguments with defaults, Python
  protocols (iteration, indexing, `len`, ...) on logic objects, automatic conversions between
  Python values and terms: the goal is to exploit logic programming *programmatically*, from Python
  code, not only to run Prolog programs.
- **It is not fast.** 2P-Kt favours flexibility and portability over speed (there are plans to
  address that), and 2PPy is most likely even slower, due to the overhead of every Python <-> JVM
  call. Use it for prototyping, teaching, research, and moderate workloads, not where performance
  is critical.
- **The documentation is mostly generated**, at the moment, but kept up to date with the codebase:
  every documented example is run by the tests.

## Installation

2PPy is published on [PyPI](https://pypi.org/project/2ppy/) as `2ppy` (the package to import is
`tuprolog`). It requires Python 3.10 or later, on Linux, macOS, or Windows.

With pip, preferably in a virtual environment:

```bash
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install 2ppy                                    # upgrade with: pip install -U 2ppy
```

With [uv](https://docs.astral.sh/uv/), in a project, or as a standalone tool for the terminal IDE:

```bash
uv add 2ppy
uv tool install 2ppy        # puts 2ppy-tui on the PATH
```

The package bundles 2P-Kt's JARs, and a Java runtime comes with its `jdk4py` dependency: no Java
installation is needed. To check that everything works (the first import starts the JVM):

```bash
python -c "import tuprolog; print(tuprolog.__version__, tuprolog.Info.VERSION, tuprolog.JVM_VERSION)"
```

This prints the versions of 2PPy, 2P-Kt, and the JVM.

## Quick start

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
>>> list(solver.query("ancestor(abe, D)"))
[{'D': 'homer'}, {'D': 'bart'}, {'D': 'lisa'}]

```

Predicates can be written in Python:

```pycon
>>> from tuprolog.solve.library import library
>>> from tuprolog.solve.primitive import predicate
>>> lib = library("my.lib", primitives={"upper/2": predicate(lambda s, _: [(s, s.upper())])})
>>> list(prolog_solver(libraries=lib).query("upper(hello, U)"))
[{'U': 'HELLO'}]

```

## Terminal IDE

2PPy comes with a terminal IDE (TUI), emulating 2P-Kt's graphical IDEs (`ide-swing` and `ide-web`)
in the terminal, on the same GUI core: edit theories, run queries, and browse their solutions.

```bash
2ppy-tui                                    # or: python -m tuprolog.tui
docker run -it --rm ghcr.io/tuprolog/2ppy   # the same, with Docker
```

See [Use the terminal IDE](https://tuprolog.github.io/2ppy/how-to/use-the-terminal-ide/).
A plain REPL is also available: `python -m tuprolog.repl.prolog` (or `...problog`).

## Learn more

See the [tutorials](https://tuprolog.github.io/2ppy/tutorials/) and the
[example notebooks](https://github.com/tuProlog/2ppy/tree/master/examples) to get started, and the
[API reference](https://tuprolog.github.io/2ppy/api/tuprolog/) for the details.

## Contributing

```bash
uv sync && uv run poe build-jars    # environment and JARs (requires a JDK 17+)
uv run poe static-checks            # what CI checks
uv run poe test                     # tests, including every documented example
uv run poe docs                     # the documentation site
```

See [Contribute](https://tuprolog.github.io/2ppy/how-to/contribute/) and
[`AGENTS.md`](https://github.com/tuProlog/2ppy/blob/master/AGENTS.md).
Releases are automated by semantic-release from [Conventional Commits](https://www.conventionalcommits.org/).
