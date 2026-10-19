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

## Installation

```bash
pip install 2ppy        # or: uv add 2ppy
```

Python 3.10 or later. The package bundles 2P-Kt and a Java runtime: no Java installation is needed.

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

Interactive Prolog: `python -m tuprolog.repl.prolog`, or the terminal IDE: `2ppy-tui` (also as a
Docker image: `docker run -it --rm ghcr.io/tuprolog/2ppy`).

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
