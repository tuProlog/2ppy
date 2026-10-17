"""Aggregation of libraries into runtimes, via `libraries()`."""

import pytest

from tests.solve.primitive._support import bindings, solve_all
from tuprolog.core import atom, unifier
from tuprolog.solve import signature
from tuprolog.solve.library import Library, Runtime, aliased, libraries, library
from tuprolog.solve.library.exception import AlreadyLoadedLibraryException
from tuprolog.solve.primitive import primitive
from tuprolog.solve.prolog import prolog_solver


def answering(value: str, alias: str) -> Library:
    """A library whose `answer/1` primitive binds its argument to `value`."""

    def implementation(request):
        yield request.reply_success(unifier({request.arguments[0]: atom(value)}))

    return library(alias, primitives={signature("answer", 1): primitive(implementation)})


def aliases_of(runtime: Runtime) -> list[str]:
    return [str(lib.alias) for lib in runtime.libraries]


def test_libraries_preserves_order():
    assert aliases_of(libraries(library("a"), library("b"), library("c"))) == ["a", "b", "c"]
    assert aliases_of(libraries([library("a"), library("b")], library("c"))) == ["a", "b", "c"]


def test_libraries_same_precedence_as_runtime_of():
    first, second = answering("first", "lib.first"), answering("second", "lib.second")
    expected = bindings(
        solve_all(prolog_solver(libraries=Runtime.of(first, second)), "answer(X)"), "X"
    )
    actual = bindings(
        solve_all(prolog_solver(libraries=libraries(first, second)), "answer(X)"), "X"
    )
    assert actual == expected == ["second"]


def test_aliased_primitives_disambiguate_clashing_libraries():
    solver = prolog_solver(
        libraries=libraries(answering("first", "lib.first"), answering("second", "lib.second"))
    )
    assert bindings(solve_all(solver, "'lib.first.answer'(X)"), "X") == ["first"]
    assert bindings(solve_all(solver, "'lib.second.answer'(X)"), "X") == ["second"]


def test_libraries_empty():
    runtime = libraries()
    assert isinstance(runtime, Runtime)
    assert len(runtime) == 0


def test_libraries_rejects_duplicate_aliases():
    with pytest.raises(AlreadyLoadedLibraryException):
        libraries(library("a"), library("a"))


def test_libraries_keyword_arguments_alias_libraries():
    runtime = libraries(x=library("a"), y=library())
    assert sorted(aliases_of(runtime)) == ["x", "y"]


def test_aliased():
    original = answering("v", "original")
    renamed = aliased("renamed", original)
    assert renamed.alias == "renamed"
    assert renamed.primitives.keySet() == original.primitives.keySet()
    assert original.alias == "original"


@pytest.mark.parametrize("wrong", ["lib", 42, None, atom("a"), ["lib"], [library("a"), 1]])
def test_libraries_rejects_non_libraries(wrong):
    with pytest.raises(TypeError):
        libraries(wrong)


@pytest.mark.parametrize("wrong", ["lib", 42, None, [library("a")]])
def test_libraries_rejects_non_library_keyword_arguments(wrong):
    with pytest.raises(TypeError):
        libraries(x=wrong)


def test_libraries_accepts_runtimes():
    runtime = libraries(library("a"), library("b"))
    assert aliases_of(libraries(runtime)) == ["a", "b"]
    assert aliases_of(libraries(runtime, library("c"))) == ["a", "b", "c"]
    assert aliases_of(libraries([runtime], [library("c")])) == ["a", "b", "c"]


def test_libraries_accepts_nested_iterables_and_generators():
    nested = [[library("a"), (library("b"),)], (lib for lib in [library("c")])]
    assert aliases_of(libraries(nested)) == ["a", "b", "c"]
