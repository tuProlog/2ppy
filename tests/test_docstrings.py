"""The examples (`>>>`) in the docstrings of the tuprolog package, in the README, and in the pages
of the documentation site (docs/), run as documented.

Besides the docstrings `doctest` finds (modules, functions, classes, methods), this checks the
attribute docstrings, i.e. the string literals following module-level assignments, which document
the re-exported JVM types (e.g. `Term = _core.Term` followed by `\"\"\"...\"\"\"`).
"""

import ast
import doctest
import importlib
import inspect
import pkgutil
from itertools import pairwise
from pathlib import Path
from types import ModuleType

import pytest

import tuprolog

# modules whose import has side effects beyond defining names (they run interactive loops)
ENTRY_POINTS = {"tuprolog.__main__", "tuprolog.tui.__main__"}

MODULES = sorted(
    info.name
    for info in pkgutil.walk_packages(tuprolog.__path__, "tuprolog.")
    if info.name not in ENTRY_POINTS
)

OPTIONS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


def attribute_docstrings(module: ModuleType) -> list[tuple[str, str, int]]:
    """(name, docstring, line) of the attribute docstrings of a module."""
    try:
        source = inspect.getsource(module)
    except (OSError, TypeError):
        return []
    body = ast.parse(source).body
    found = []
    for statement, following in pairwise(body):
        if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
            continue
        if not (
            isinstance(following, ast.Expr)
            and isinstance(following.value, ast.Constant)
            and isinstance(following.value.value, str)
        ):
            continue
        targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
        names = [t.id for t in targets if isinstance(t, ast.Name)]
        if names:
            found.append((names[0], following.value.value, following.lineno))
    return found


def doctests(module: ModuleType) -> list[doctest.DocTest]:
    tests = doctest.DocTestFinder(exclude_empty=True).find(module, module.__name__)
    parser = doctest.DocTestParser()
    filename = getattr(module, "__file__", None)
    for name, docstring, line in attribute_docstrings(module):
        test = parser.get_doctest(
            docstring, dict(vars(module)), f"{module.__name__}.{name}", filename, line
        )
        if test.examples:
            tests.append(test)
    return [t for t in tests if t.examples]


@pytest.mark.parametrize("name", MODULES)
def test_docstring_examples(name):
    module = importlib.import_module(name)
    runner = doctest.DocTestRunner(optionflags=OPTIONS)
    for test in doctests(module):
        test.globs = {**vars(module), **test.globs}
        runner.run(test)
    results = runner.summarize(verbose=False)
    assert results.failed == 0, f"{results.failed} failing example(s) in {name}, see the output"


ROOT = Path(__file__).parent.parent

PAGES = [
    "README.md",
    *sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "docs").rglob("*.md")),
]


@pytest.mark.parametrize("page", PAGES)
def test_page_examples(page):
    results = doctest.testfile(str(ROOT / page), module_relative=False, optionflags=OPTIONS)
    assert results.failed == 0, f"{results.failed} failing example(s) in {page}, see the output"
