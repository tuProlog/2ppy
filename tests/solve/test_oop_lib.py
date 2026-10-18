"""Tests for the Python OOP library: 2P-Kt's OOPLib Prolog API over Python objects."""

import io
import sys
import types

import pytest

from tuprolog.errors import (
    PrologExistenceError,
    PrologInstantiationError,
    PrologPermissionError,
    PrologSystemError,
    PrologTypeError,
)
from tuprolog.solve.library import libraries
from tuprolog.solve.libs import NULL_REF, SAFE_MODULES, OOPLib, oop_lib
from tuprolog.solve.prolog import prolog_solver


class Point:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def moved(self, dx=0, dy=0):
        return Point(self.x + dx, self.y + dy)

    def _secret(self):
        return 42


@pytest.fixture
def solver():
    return prolog_solver(libraries=libraries(oop_lib(aliases={"point": Point})))


def first(solver, goal):
    results = list(solver.query(goal, limit=1))
    assert results, f"{goal} failed"
    return results[0]


# --- the library ---------------------------------------------------------------------------------


def test_default_instance():
    assert OOPLib.alias == "prolog.oop.python"
    assert {str(op.functor) for op in OOPLib.operators} >= {".", ":=", "as", "$"}


PRIMITIVES = [
    "type/2",
    "new_object/3",
    "invoke_method/3",
    "assign/3",
    "cast/3",
    "register/2",
    "unregister/1",
    "alias/2",
    "ref/1",
    "object_ref/1",
    "type_ref/1",
    "null_ref/1",
    "list_items/2",
    "set_items/2",
    "array_items/2",
]


def test_oop_lib_primitives_and_rules():
    assert {str(s.name) + "/" + str(s.arity) for s in OOPLib.primitives.keySet()} == set(PRIMITIVES)
    heads = {f"{c.head.functor}/{c.head.arity}" for c in OOPLib.clauses}
    assert heads >= {":=/2", "new_object/2", "fluent_reduce/2", "property_reduce/3", "./2"}


# --- types, objects and calls -------------------------------------------------------------------


def test_type(solver):
    assert first(solver, "type('collections.Counter', T)")["T"] == "<type:collections.Counter>"
    assert first(solver, "type(int, T), type_ref(T), ref(T)")["T"] == "<type:builtins.int>"
    assert first(solver, "type(math, T)")["T"] == "<module:math>"


def test_new_object_and_method_calls(solver):
    result = first(solver, "new_object($list, [], L), L.append(1), L.append(a), list_items(L, I)")
    assert result["I"] == [1, "a"]
    assert result["L"].startswith("<object:list#")


def test_new_object_with_keyword_arguments(solver):
    result = first(solver, "new_object($point, [y = 2], P), X := P.x, Y := P.y")
    assert (result["X"], result["Y"]) == (0, 2)


def test_fluent_calls_and_chains(solver):
    assert first(solver, "X := $math.sqrt(16)")["X"] == 4.0
    assert first(solver, "X := $math.pi")["X"] == 3.141592653589793
    assert first(solver, "X := hello.upper")["X"] == "HELLO"
    assert first(solver, "X := $math.sqrt(2).hex")["X"] == (2**0.5).hex()
    assert first(solver, "X := [1, 2, 1].count(1)")["X"] == 2


def test_methods_and_attributes(solver):
    result = first(
        solver, "new_object($point, [1, 2], P), Q := P.moved(dy = 3), X := Q.x, Y := Q.y"
    )
    assert (result["X"], result["Y"]) == (1, 5)


def test_keyword_arguments(solver):
    assert first(solver, "X := $json.dumps([1, 2], indent = 2)")["X"] == "[\n  1,\n  2\n]"


def test_assignment(solver):
    result = first(solver, "new_object($point, [], P), P.x := 5, X := P.x")
    assert result["X"] == 5


def test_cast(solver):
    assert first(solver, "X := '42' as $int")["X"] == 42
    assert first(solver, "X := 3 as $float")["X"] == 3.0
    assert first(solver, "X := 3 as 'fractions.Fraction'")["X"].startswith("<object:Fraction#")


def test_results_are_terms_or_references(solver):
    result = first(solver, "X := 'a,b'.split(','), list_items(X, L)")
    assert result["X"].startswith("<object:list#")
    assert result["L"] == ["a", "b"]
    assert first(solver, "new_object($dict, [], D), X := D.get(a)")["X"] == "<null>"


def test_items(solver):
    assert first(solver, "X := 'ab'.partition(b), array_items(X, I)")["I"] == ["a", "b", ""]
    assert sorted(first(solver, "new_object($set, [[a, b, a]], S), set_items(S, I)")["I"]) == [
        "a",
        "b",
    ]


def test_references_inside_collections_are_dereferenced(solver):
    result = first(solver, "new_object($point, [1], P), new_object($list, [[P]], L), X := L.pop.x")
    assert result["X"] == 1


def test_same_object_same_reference(solver):
    result = first(solver, "new_object($list, [], L), register(L, l), alias(l, R)")
    assert result["L"] == result["R"]


# --- aliases -------------------------------------------------------------------------------------


def test_aliases_of_oop_lib_and_python(solver):
    for alias, expected in [("arraylist", "list"), ("hashmap", "dict"), ("string", "str")]:
        assert first(solver, f"alias({alias}, R)")["R"] == f"<type:builtins.{expected}>"
    assert first(solver, "alias(math, R)")["R"] == "<module:math>"
    assert first(solver, "X := $builtins.len([1, 2, 3])")["X"] == 3


def test_safe_modules_are_aliased(solver):
    for module in sorted(SAFE_MODULES - {"string"}):  # $string is str, as in OOPLib
        assert first(solver, f"alias({module}, R)")["R"] == f"<module:{module}>"
    assert first(solver, "type('string.Template', T)")["T"] == "<type:string.Template>"


def test_standard_streams_are_python_current_ones(solver, monkeypatch):
    buffer = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buffer)
    first(solver, "$stdout.write(hello)")
    assert buffer.getvalue() == "hello"


def test_register_and_unregister(solver):
    result = first(
        solver, "new_object($list, [], L), register(L, l), $l.append(1), list_items($l, I)"
    )
    assert result["I"] == [1]
    assert first(solver, "unregister(l)") == {}
    assert list(solver.query("unregister(l)")) == []
    with pytest.raises(PrologExistenceError, match="no alias `l`"):
        first(solver, "X := $l.copy")


def test_aliases_cannot_be_registered_twice(solver):
    with pytest.raises(PrologPermissionError):
        first(solver, "register(1, a), register(2, a)")


def test_user_aliases():
    solver = prolog_solver(libraries=oop_lib(aliases={"ns": types.SimpleNamespace(answer=42)}))
    assert first(solver, "X := $ns.answer")["X"] == 42


# --- references ----------------------------------------------------------------------------------


def test_reference_checks(solver):
    assert first(solver, "new_object($list, [], L), ref(L), object_ref(L)")
    assert first(solver, "type(int, T), \\+ object_ref(T), type_ref(T)")
    assert first(solver, "null_ref(N), ref(N), \\+ object_ref(N)")["N"] == str(NULL_REF.value)
    assert list(solver.query("ref(abc)")) == []
    assert list(solver.query("type_ref(1)")) == []


# --- restrictions and errors ---------------------------------------------------------------------


def test_only_safe_modules_are_importable(solver):
    with pytest.raises(PrologExistenceError):
        first(solver, "type(os, T)")
    with pytest.raises(PrologExistenceError):
        first(solver, "type('subprocess.run', T)")
    with pytest.raises(PrologExistenceError):
        first(solver, "type(eval, T)")


def test_all_imports_can_be_allowed():
    solver = prolog_solver(libraries=oop_lib(allow_all_imports=True))
    assert first(solver, "type('os.path', T)")["T"].startswith("<module:")
    assert first(solver, "X := $sys.maxsize")["X"] == sys.maxsize


def test_private_attributes_are_not_accessible(solver):
    with pytest.raises(PrologPermissionError):
        first(solver, "new_object($point, [], P), X := P.'_secret'")
    with pytest.raises(PrologPermissionError):
        first(solver, "X := hello.'__class__'")


def test_private_attributes_can_be_allowed():
    solver = prolog_solver(libraries=oop_lib(allow_private=True, aliases={"point": Point}))
    assert first(solver, "new_object($point, [], P), X := P.'_secret'")["X"] == 42


def test_missing_attributes(solver):
    with pytest.raises(PrologExistenceError, match="no attribute `nope` on str"):
        first(solver, "X := hello.nope")


def test_unbound_receivers(solver):
    with pytest.raises(PrologInstantiationError):
        first(solver, "invoke_method(_, upper, _)")


def test_wrong_arguments(solver):
    with pytest.raises(PrologTypeError):
        first(solver, "type(1, _)")
    with pytest.raises(PrologTypeError):
        first(solver, "invoke_method(a, 1, _)")
    with pytest.raises(PrologTypeError):
        first(solver, "X := 1 as $math")


def test_python_exceptions_are_system_errors(solver):
    with pytest.raises(PrologSystemError, match="ValueError"):
        first(solver, "X := $math.log(0)")
    assert first(solver, "catch(X := $math.sqrt(-1), error(system_error, _), true)") == {}
