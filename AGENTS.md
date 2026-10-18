# AGENTS.md

Notes for coding agents and contributors. User-facing usage lives in `README.md`; do not duplicate
it here. The project follows
[template-python-project-uv](https://github.com/gciatto/template-python-project-uv); the roadmap
(status, design criteria, plan) is tracked in issue #47.

## What 2PPy is

A Python wrapper of [2P-Kt](https://github.com/tuProlog/2p-kt) via [JPype](https://jpype.readthedocs.io):
logic is written once in Kotlin and wrapped here ("write once, wrap elsewhere"), with an API as
Pythonic as possible. Never re-implement in Python what 2P-Kt already provides: wrap it, and
prefer fixing the Kotlin API (e.g. `@JvmStatic`, `@JvmOverloads`) over Python workarounds.

## Layout

```
tuprolog/           the package (flat layout); importing it starts the JVM
  __init__.py       starts the JVM on the JARs in libs/, exposes `Info`, `__version__`, `logger`
  libs/             2P-Kt's JARs (untracked, `poe fetch-jars`) + java.py (locates jdk4py's JVM)
  jvmutils.py       JVM <-> Python bridging: iterables, maps, automatic snake_case accessors
  pyutils.py        Python helpers (iterable-or-varargs forwarding, ...)
  <module>/         one sub-package per 2P-Kt module (core, unify, theory, solve, ...), each with
    _definitions.py   JVM types and constants re-exported under Pythonic names
    _api.py           Pythonic factory functions (snake_case, defaults, varargs)
    _adapters.py      @JImplementationFor customizers adding Python protocols to JVM types
  repl/             Cmd-based REPLs (`python -m tuprolog.repl.prolog`, `...problog`)
tests/              pytest tests (they need the JARs)
scripts/            fetch_jars.py (Maven), githooks.py (local Git hooks)
pom.xml             the 2P-Kt artifacts and version to fetch
.github/workflows/
  check.yml         static-checks + coverage, then tests on ubuntu/windows/macos x Python 3.10-3.13,
                    then deploy.yml
  deploy.yml        semantic-release (dry run off master and on the initial commit)
```

## Commands

```bash
uv sync                               # env + dev tools
uv run poe fetch-jars                 # JARs into tuprolog/libs/ (requires mvn)
uv run poe test                       # pytest
uv run poe static-checks              # compileall, ruff format --check, ruff check, mypy
uv run poe static-fixes               # ruff --fix + ruff format
uv run poe coverage && uv run poe coverage-report
uv run poe install-hooks [HOOK...]    # local hooks in .git/hooks (default: all)
```

## Conventions

- Commits follow Conventional Commits (`<type>[(scope)][!]: <description>`); semantic-release
  derives the next version from them (`feat` = minor, `fix` = patch, `!` = major;
  `chore`/`docs`/`style`/`test`/`ci` don't release).
- No AI-assistant signatures in commit messages or PR descriptions.
- `static-checks` and tests must pass before committing.
- Ruff: line length 100, target py310. Code must run on Python 3.10 (the lowest version in
  the CI matrix and `requires-python`; keep the three in sync).
- Manage dependencies with `uv add` / `uv add --dev`, never by hand-editing `uv.lock`.
  The 2P-Kt version lives in `pom.xml`.
- Tests must not hit the network (fetching the JARs is a setup step, not part of the tests).
- The JVM can be started only once per process: tests share it, and must not depend on
  JVM options.
- Every module declares a literal `__all__` (packages: the union of their `_definitions` and
  `_api`, checked by `tests/test_imports.py`). Names shadowing Python builtins (e.g. the JVM
  `TypeError`) or other tuprolog modules' names stay importable by name but out of `__all__`.
- Customizers (`@JImplementationFor`) of interfaces or base classes: add
  `@customize_derived(...)` (from `tuprolog.jvmutils`) for members overriding JVM methods,
  otherwise derived classes redeclaring those methods shadow them.

## Releases

Conventional Commits drive semantic-release (`release.config.mjs`), which runs
`uv version <next> && uv build && uv publish` in its prepare step, after `poe fetch-jars`
(the JARs ship in the wheel and the sdist). `pyproject.toml` is the only version source;
never bump it by hand. `CHANGELOG.md` is generated.
