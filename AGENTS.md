# AGENTS.md

Notes for coding agents and contributors. User-facing usage lives in the documentation site
(`docs/`; `README.md` stays a concise summary pointing to it): do not duplicate it here. The
project follows [template-python-project-uv](https://github.com/gciatto/template-python-project-uv); the roadmap
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
tests/              pytest tests (they need the JARs), including the examples of docstrings, README
                    and docs pages
examples/           Jupyter notebooks (with their outputs), run by tests/test_examples.py and
                    rendered in the site's Examples section (copied there by docs/gen_ref_pages.py)
docs/               the documentation site (mkdocs.yml): index.md (the full picture), tutorials/,
                    how-to/, reference/, explanation/ (as 2P-Kt's documentation), and
                    gen_ref_pages.py (generates api/, one API-reference page per public module)
scripts/            fetch_jars.py (Maven), githooks.py (local Git hooks)
pom.xml             the 2P-Kt artifacts and version to fetch
.github/workflows/
  check.yml         static-checks + coverage, then tests on ubuntu/windows/macos x Python 3.10-3.13,
                    then deploy.yml
  deploy.yml        semantic-release (dry run off master and on the initial commit)
  docs.yml          builds the documentation site, deploys it on GitHub Pages from master
```

## Commands

```bash
uv sync                               # env + dev tools
uv run poe fetch-jars                 # JARs into tuprolog/libs/ (requires mvn)
uv run poe test                       # pytest
uv run poe static-checks              # compileall, ruff format --check, ruff check, mypy
uv run poe static-fixes               # ruff --fix + ruff format
uv run poe coverage && uv run poe coverage-report
uv run jupyter lab examples/          # edit the example notebooks (Jupyter is a dev dependency)
uv run poe docs                       # documentation site in site/ (mkdocs build --strict)
uv run poe docs-serve                 # the same, with live reload
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

## Documentation

The site's pages (`docs/`) give the full picture, organized as 2P-Kt's documentation (tutorials,
how-to guides, reference, explanation; see `mkdocs.yml`'s `nav`), and link the API reference for
details. The Python API is documented in docstrings, for `help()` and for an API reference generated from
them (mkdocstrings/griffe-like tools). Readers are not assumed to know 2P-Kt (nor Kotlin): explain
the logic-programming notions a page relies on, and link 2P-Kt's documentation
(<https://tuprolog.github.io/2p-kt/>, API at <https://tuprolog.github.io/2p-kt/api/>) only as
further reading. The organization follows 2P-Kt's KDoc:

- **Packages** (`__init__.py` docstring, before the imports): what the package is for, its key
  notions, its main types and factories, a short example, and related packages.
- **JVM types** re-exported by `_definitions.py`: an attribute docstring (a string literal right
  after the assignment, e.g. `Term = _core.Term` then `"""..."""`) saying what the type models,
  its main members as callable from Python (JVM methods also get snake_case aliases, `getX()` the
  property `x`, `isX()` the property `is_x`, see `tuprolog.jvmutils`), and the Python protocols its
  `_adapters.py` customizer adds (e.g. iteration, indexing, `len`).
- **Functions, classes, methods, properties** (`_api.py`, `_adapters.py`, plain modules): a
  one-line summary, then details, then the sections that apply.

Style: Google-style docstrings (`Args:`, `Returns:`, `Yields:`, `Raises:`, `Examples:`, `Note:`,
`See Also:`) with Markdown text; names in backticks, fully qualified when in another package
(`tuprolog.core.Term`); describe the 2P-Kt counterpart in a `Note:` when useful (e.g. "Wraps
2P-Kt's `Struct.of`"). Examples are doctests (`>>>`), run by `tests/test_docstrings.py` (with
`ELLIPSIS` and `NORMALIZE_WHITESPACE`; use `...` for unstable output, e.g. fresh variable names):
keep them short, deterministic, and free of I/O on real files or the network. Example notebooks
are committed with their outputs: after editing one, re-run it (e.g. `uv run jupyter nbconvert
--to notebook --execute --inplace examples/<name>.ipynb`), and list new ones in `examples/README.md`,
`docs/examples/index.md` and `mkdocs.yml`'s `nav`. The site
(`uv run poe docs`, MkDocs Material + mkdocstrings) renders the docstrings statically, with griffe:
it builds in strict mode, so fix the warnings it reports (e.g. a `Returns:` section of an
unannotated function).

## Releases

Conventional Commits drive semantic-release (`release.config.mjs`), which runs
`uv version <next> && uv build && uv publish` in its prepare step, after `poe fetch-jars`
(the JARs ship in the wheel and the sdist). `pyproject.toml` is the only version source;
never bump it by hand. `CHANGELOG.md` is generated.
