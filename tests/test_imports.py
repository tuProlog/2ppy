"""Every tuprolog module imports cleanly, and star-imports do not shadow names unexpectedly."""

import importlib
import pkgutil
from collections import defaultdict
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

PUBLIC_MODULES = [m for m in MODULES if not any(p.startswith("_") for p in m.split("."))]


def star_names(module: ModuleType) -> list[str]:
    exported = getattr(module, "__all__", None)
    if exported is not None:
        return list(exported)
    return [n for n in vars(module) if not n.startswith("_")]


def test_walk_finds_all_subpackages():
    for expected in [
        "tuprolog.core",
        "tuprolog.repl",
        "tuprolog.repl.prolog",
        "tuprolog.repl.problog",
        "tuprolog.solve.exception.error.type",
        "tuprolog.solve.exception.warning",
        "tuprolog.solve.library.exception",
        "tuprolog.unify.exception",
    ]:
        assert expected in MODULES


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    module = importlib.import_module(name)
    assert module.__name__ == name


@pytest.mark.parametrize("name", PUBLIC_MODULES)
def test_star_import_names_exist(name):
    module = importlib.import_module(name)
    for exported in star_names(module):
        assert hasattr(module, exported), exported


def own_star_sources(package: ModuleType) -> list[ModuleType]:
    """The sibling modules a package re-exports via `from ._x import *`."""
    sources = []
    for part in ("_definitions", "_api"):
        try:
            sources.append(importlib.import_module(f"{package.__name__}.{part}"))
        except ModuleNotFoundError:
            pass
    return sources


@pytest.mark.parametrize(
    "name", [m for m in PUBLIC_MODULES if hasattr(importlib.import_module(m), "__path__")]
)
def test_package_star_sources_agree(name):
    """Names re-exported by both _definitions and _api of a package are the same object."""
    package = importlib.import_module(name)
    seen: dict[str, tuple[str, object]] = {}
    for source in own_star_sources(package):
        for exported in star_names(source):
            value = getattr(source, exported)
            if isinstance(value, ModuleType):
                continue
            if exported in seen:
                assert seen[exported][1] is value, (
                    f"{exported}: {seen[exported][0]} vs {source.__name__}"
                )
            seen[exported] = (source.__name__, value)


def collisions(modules: list[str]) -> dict[str, list[str]]:
    """Public names that different modules bind to different (non-module) objects."""
    owners: dict[str, list[tuple[str, object]]] = defaultdict(list)
    for name in modules:
        module = importlib.import_module(name)
        for exported in star_names(module):
            value = getattr(module, exported)
            if isinstance(value, ModuleType):
                continue
            if not any(value is other for _, other in owners[exported]):
                owners[exported].append((name, value))
    return {n: [m for m, _ in o] for n, o in owners.items() if len(o) > 1}


def test_exception_modules_do_not_collide():
    modules = [m for m in PUBLIC_MODULES if ".exception" in m]
    assert collisions(modules) == {}


def test_repl_modules_do_not_collide():
    modules = [m for m in PUBLIC_MODULES if m.startswith("tuprolog.repl")]
    assert collisions(modules) == {}


def test_public_modules_do_not_collide():
    assert collisions(PUBLIC_MODULES) == {}


@pytest.mark.parametrize(
    "name", PUBLIC_MODULES + [m for m in MODULES if m.endswith(("._api", "._definitions"))]
)
def test_modules_declare_all(name):
    module = importlib.import_module(name)
    assert isinstance(getattr(module, "__all__", None), list), f"{name} has no __all__"


@pytest.mark.parametrize(
    "name", [m for m in PUBLIC_MODULES if hasattr(importlib.import_module(m), "__path__")]
)
def test_package_all_is_the_union_of_its_sources(name):
    package = importlib.import_module(name)
    sources = own_star_sources(package)
    if not sources:
        return
    expected = {n for source in sources for n in star_names(source)}
    assert set(package.__all__) == expected
