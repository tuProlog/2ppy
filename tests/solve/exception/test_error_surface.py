"""The names that `from tuprolog.solve.exception.error import *` (and friends) expose."""

import builtins
import importlib
import inspect
from types import ModuleType

import pytest
from jpype import JClass, JObject

SUBMODULES = [
    "domain",
    "evaluation",
    "existence",
    "instantiation",
    "message",
    "permission",
    "representation",
    "syntax",
    "system",
    "type",
]

ERROR = "tuprolog.solve.exception.error"


def submodule(name: str, part: str = "") -> ModuleType:
    return importlib.import_module(f"{ERROR}.{name}{part}")


def factories(name: str) -> dict[str, object]:
    api = submodule(name, "._api")
    return {
        n: f
        for n, f in vars(api).items()
        if inspect.isfunction(f) and f.__module__ == api.__name__ and not n.startswith("_")
    }


def star_names(module: ModuleType) -> set[str]:
    exported = getattr(module, "__all__", None)
    if exported is not None:
        return set(exported)
    return {n for n in vars(module) if not n.startswith("_")}


def star_import(module_name: str) -> dict[str, object]:
    """The namespace `from module_name import *` would bind (no exec needed)."""
    module = importlib.import_module(module_name)
    return {n: getattr(module, n) for n in star_names(module)}


@pytest.mark.parametrize("name", SUBMODULES)
def test_every_submodule_has_factories_or_definitions(name):
    assert factories(name) or star_names(submodule(name, "._definitions"))


def test_factory_names_are_unique_across_submodules():
    seen: dict[str, str] = {}
    for name in SUBMODULES:
        for factory in factories(name):
            assert factory not in seen, f"{factory} defined in both {seen[factory]} and {name}"
            seen[factory] = name


@pytest.mark.parametrize("name", SUBMODULES)
def test_factories_resolve_to_their_module(name):
    error = importlib.import_module(ERROR)
    package = submodule(name)
    for factory_name, factory in factories(name).items():
        assert getattr(package, factory_name) is factory
        assert getattr(error, factory_name) is factory, factory_name


@pytest.mark.parametrize("name", SUBMODULES)
def test_definitions_resolve_to_their_module(name):
    error = importlib.import_module(ERROR)
    definitions = submodule(name, "._definitions")
    for definition in star_names(definitions):
        value = getattr(definitions, definition)
        if isinstance(value, ModuleType) or definition == "logger":
            continue
        assert getattr(error, definition) is value, definition


@pytest.mark.parametrize("name", SUBMODULES)
def test_star_import_of_submodule(name):
    namespace = star_import(f"{ERROR}.{name}")
    for factory_name, factory in factories(name).items():
        assert namespace[factory_name] is factory


SHADOWED = pytest.mark.xfail(
    strict=True,
    reason="the domain(), permission() and type() factories shadow the sub-packages of the same "
    "name in tuprolog.solve.exception.error: `import ...error.type as m` yields the function",
)


@pytest.mark.parametrize(
    "name",
    [
        pytest.param(n, marks=SHADOWED) if n in {"domain", "permission", "type"} else n
        for n in SUBMODULES
    ],
)
def test_submodules_are_not_shadowed(name):
    error = importlib.import_module(ERROR)
    assert getattr(error, name) is submodule(name)


@pytest.mark.xfail(
    strict=True,
    reason="star-imports of tuprolog.solve.exception(.error) shadow Python builtins: Warning, "
    "TypeError, SyntaxError, SystemError, PermissionError (JVM classes) and type (a factory)",
)
@pytest.mark.parametrize("module", ["tuprolog.solve.exception", ERROR])
def test_star_imports_do_not_shadow_builtins(module):
    namespace = star_import(f"{module}")
    shadowed = {n for n in namespace if n != "__builtins__" and hasattr(builtins, n)}
    assert shadowed == set()


@pytest.mark.xfail(
    strict=True,
    reason="no __all__ in tuprolog.solve.exception.error.*: star-imports leak helper imports "
    "(jpype, logger, errors, Term, ExecutionContext, Iterable, atom, ...)",
)
def test_star_import_exposes_only_error_names():
    namespace = star_import(f"{ERROR}")
    leaked = set()
    for name, value in namespace.items():
        defined_here = getattr(value, "__module__", "") or ""
        if name == "__builtins__" or defined_here.startswith(ERROR):
            continue
        if isinstance(value, ModuleType) and value.__name__.startswith(ERROR):
            continue
        if isinstance(value, JClass):
            java_name = str(value.class_.getName())
        elif isinstance(value, JObject):
            java_name = str(value.getClass().getName())
        else:
            java_name = ""
        if java_name.startswith("it.unibo.tuprolog.solve.exception.error."):
            continue
        leaked.add(name)
    assert leaked == set()
