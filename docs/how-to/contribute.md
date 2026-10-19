# Contribute

This guide sets up a development environment for 2PPy, and walks through the checks, the
conventions, the documentation, and the release process. The sources are on
[GitHub](https://github.com/tuProlog/2ppy); the project follows the
[template-python-project-uv](https://github.com/gciatto/template-python-project-uv) layout.

## Set up the environment

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and a JDK 17 or newer
(`java` on the `PATH`, or `JAVA_HOME` set). The JVM side of 2PPy is a
[Gradle](https://gradle.org/) project in
[`jvm/`](https://github.com/tuProlog/2ppy/tree/master/jvm), run through its wrapper (no Gradle
installation needed): it downloads 2P-Kt's JARs from
[Maven Central](https://mvnrepository.com/artifact/it.unibo.tuprolog), at the version declared in
[`jvm/gradle/libs.versions.toml`](https://github.com/tuProlog/2ppy/blob/master/jvm/gradle/libs.versions.toml),
and compiles the Kotlin adapters making 2P-Kt usable from Python (`jvm/src/main/kotlin`, e.g. the
facade of `tuprolog.gui`), without changing 2P-Kt itself.

```bash
git clone https://github.com/tuProlog/2ppy.git && cd 2ppy
uv sync                      # create the environment, with the development and documentation tools
uv run poe build-jars        # build the JVM side, and copy the JARs into tuprolog/libs/ (needed
                             # before testing or building)
```

## Run the checks

```bash
uv run poe test              # the tests, including the examples in docstrings, README and docs pages
uv run poe test-jvm          # the tests of the JVM side (jvm/src/test)
uv run poe static-checks     # compileall, ruff format --check, ruff check, mypy (what CI runs)
uv run poe static-fixes      # ruff check --fix + ruff format
uv run poe coverage && uv run poe coverage-report
uv build                     # wheel and sdist in dist/ (JARs included)
```

Optional local Git hooks run some of these automatically:
`uv run poe install-hooks [HOOK...]` (`pre-commit`, `conventional-commits`, `no-ai-signature`,
`pre-push`).

## Know the layout

- `tuprolog/` is the package: one sub-package per 2P-Kt module (`core`, `unify`, `theory`,
  `solve`, ...), each split into `_definitions.py` (the JVM types, re-exported under Pythonic
  names), `_api.py` (Pythonic factory functions) and `_adapters.py` (Python protocols added to JVM
  types); see [Architecture](../explanation/architecture.md).
- `jvm/` is the JVM side: a Gradle project declaring 2P-Kt's artifacts, with the Kotlin adapters
  2PPy needs on top of them; `poe build-jars` copies its JAR and runtime classpath into
  `tuprolog/libs/`.
- `tests/` holds the pytest tests; `docs/` the documentation site; `scripts/` the Git hooks.
- Contributor notes, with the full list of conventions, are in
  [`AGENTS.md`](https://github.com/tuProlog/2ppy/blob/master/AGENTS.md).

## Follow the conventions

- Wrap 2P-Kt, never re-implement it in Python: when 2P-Kt's API is in the way, adapt it in
  Kotlin, in `jvm/src/main/kotlin` (or fix it upstream, when the fix belongs there).
- Code must run on Python 3.10 (Ruff: line length 100, target py310).
- Every module declares a literal `__all__`.
- Manage dependencies with `uv add` (or `uv add --dev`), never by editing `uv.lock`; the 2P-Kt
  version lives in `jvm/gradle/libs.versions.toml`.
- Tests must not use the network, and must not depend on JVM options (the JVM starts once per
  process, shared by all tests).
- `static-checks` and the tests must pass before committing.

## Write documentation

- Document every public module, function, class and re-exported JVM type with Google-style
  docstrings (`Args:`, `Returns:`, `Raises:`, `Examples:`, ...); JVM types get an *attribute
  docstring*, a string literal right after their assignment in `_definitions.py`.
- Write examples as doctests (`>>>`): `tests/test_docstrings.py` runs those in docstrings, in the
  README and in the pages under `docs/`. Keep them deterministic (use `...` for unstable output,
  such as fresh variable names) and free of network access.
- Pages under `docs/` follow 2P-Kt's documentation: tutorials, how-to guides, reference,
  explanation. The API reference is generated from the docstrings.

Build the site, in strict mode, or serve it with live reload:

```bash
uv run poe docs              # the site in site/
uv run poe docs-serve        # http://127.0.0.1:8000, rebuilt on changes
```

## Commit and release

Commits follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
(`<type>[(scope)][!]: <description>`; `feat` releases a minor version, `fix` a patch, `!` a major
one; `docs`, `test`, `chore`, `ci`, `style` release nothing). On every push to `master`,
[semantic-release](https://semantic-release.gitbook.io/semantic-release/) derives the next version
from them, publishes it on [PyPI](https://pypi.org/project/2ppy/), and creates the corresponding
[GitHub Release](https://github.com/tuProlog/2ppy/releases). `pyproject.toml` is the only version
source: never bump it by hand. The release workflow needs the `PYPI_TOKEN` and `RELEASE_TOKEN`
repository secrets.

CI runs the static checks and the tests on Ubuntu, Windows and macOS, with Python 3.10 to 3.13,
and builds the documentation site, which every push to `master` deploys on
[GitHub Pages](https://tuprolog.github.io/2ppy/). Dependencies are kept up to date by
[Renovate](https://docs.renovatebot.com/).
