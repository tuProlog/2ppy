# 2PPy (tuProlog in Python)

Experimental porting of [2P-Kt](https://github.com/tuProlog/2p-kt) on Python, via [JPype](https://jpype.readthedocs.io).

> This is a __work in progress__.

## Introduction

Object-oriented and modular ecosystem for symbolic AI and logic programming, currently featuring:

* [a command-line interface, in the form of a REPL](#use-2ppy-as-an-interactive-repl)

* a module for logic terms and clauses representation, namely `tuprolog.core`

* a module for logic unification, namely `tuprolog.unify`

* a module for in-memory indexing and storing logic theories, namely `tuprolog.theory`

* a module for other indexed collections of logic clauses (multi-sets and queues), namely `tuprolog.collections`

* a module providing generic API for resolution of logic queries, namely `tuprolog.solve`
    * a module that implements deterministic logic programming and solving, namely `tuprolog.solve.prolog`
    * a module that implements probabilistic logic programming and solving, namely `tuprolog.solve.problog`
    * a module exposing 2P-Kt's IO and OOP libraries (e.g. `read/1`, `open/3`, `new_object/3`), namely `tuprolog.solve.libs`

* two parsing modules: one aimed at parsing terms, namely `tuprolog.core.parsing`, and the other aimed at parsing theories, namely `tuprolog.theory.parsing`

## How to use 2ppy

### Installing 2ppy

Install 2PPy from [PyPI](https://pypi.org/project/2ppy/) (Python 3.10 or later):

```bash
pip install 2ppy        # or: uv add 2ppy
```

The package ships 2P-Kt's JARs, and depends on [`jdk4py`](https://pypi.org/project/jdk4py/),
which bundles a Java runtime: no separate Java installation is required.
The JVM is started when `tuprolog` is first imported.

### Use 2ppy as a Python library

1. Import `tuprolog.*` modules in your Python scripts
1. Use the Pythonic API to write, parse or solve your logic programs. You can find some examples in the [tests folder](tests).
1. Python values are converted where terms are expected (e.g. `struct("f", "a", 1)` is `f(a, 1)`, see `tuprolog.core.to_term`).
    Methods without a Pythonic counterpart are forwarded to the underlying JVM objects, so they may return JVM types (e.g. `java.lang.String`).
1. Python streams (`io.IOBase`, e.g. files, `sys.stdin`, `io.StringIO`, `io.BytesIO`) are accepted wherever 2P-Kt reads or writes:
    parsers (`read_theory(open("kb.pl"))`), solvers' channels (`prolog_solver(std_in=io.StringIO("..."), std_out=buffer)`),
    and JVM methods expecting streams (binary), readers or writers (text). Binary streams are UTF-8 encoded.
    By default, solvers read from and write on Python's current `sys.stdin`, `sys.stdout` and `sys.stderr`.

### Use 2PPy as an interactive REPL

1. Python shell mode: run `python -m tuprolog`
1. Logic solver [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop): 
    1. run `python -m tuprolog.repl.prolog` for Prolog
    1. run `python -m tuprolog.repl.problog` for ProbLog

## How to contribute to 2PPy

The project follows [template-python-project-uv](https://github.com/gciatto/template-python-project-uv).
Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/) and
[Apache Maven](https://maven.apache.org/install.html) (`mvn` on the `PATH`), which downloads
2P-Kt's JARs from [Maven Central](https://mvnrepository.com/artifact/it.unibo.tuprolog), as declared in
[`pom.xml`](pom.xml).

```bash
uv sync                      # create the environment, with the development tools
uv run poe fetch-jars        # download the JARs into tuprolog/libs/ (needed before testing or building)
uv run poe test              # run the tests
uv run poe static-checks     # compileall, ruff format --check, ruff check, mypy (what CI runs)
uv run poe static-fixes      # ruff check --fix + ruff format
uv run poe coverage && uv run poe coverage-report
uv build                     # wheel and sdist in dist/ (JARs included)
```

Write the code inside `tuprolog/` and the tests inside `tests/`.
Contributor notes (layout, conventions) are in [`AGENTS.md`](AGENTS.md).
Optional local Git hooks: `uv run poe install-hooks [HOOK...]` (`pre-commit`, `conventional-commits`,
`no-ai-signature`, `pre-push`).

### Releases

Commits follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):
on every push to `master`, [semantic-release](https://semantic-release.gitbook.io/semantic-release/)
derives the next version from them, publishes it on [PyPI](https://pypi.org/project/2ppy/), and creates the
corresponding [GitHub Release](https://github.com/tuProlog/2ppy/releases).
`pyproject.toml` is the only version source: never bump it by hand.
The release workflow needs the `PYPI_TOKEN` and `RELEASE_TOKEN` repository secrets.

CI runs the static checks and the tests on Ubuntu, Windows and macOS, with Python 3.10 to 3.13.
Dependencies are kept up to date by [Renovate](https://docs.renovatebot.com/).
