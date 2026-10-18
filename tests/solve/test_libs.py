"""Tests for `tuprolog.solve.libs`, exposing 2P-Kt's IO library."""

import jpype

from tests.solve.primitive._support import bindings, solve_all
from tuprolog.solve.library import Library, libraries
from tuprolog.solve.libs import IOLib
from tuprolog.solve.prolog import prolog_solver


def test_definitions():
    assert IOLib == jpype.JClass("it.unibo.tuprolog.solve.libs.io.IOLib").INSTANCE
    assert isinstance(IOLib, Library)
    assert IOLib.alias == "prolog.io"


# file URIs: 2P-Kt 3.0.3 crashes on relative paths, and on absolute Windows ones (D:/...)


def test_io_lib_reads_files(tmp_path):
    path = tmp_path / "terms.pl"
    path.write_text("f(a). g(b).")
    solver = prolog_solver(libraries=libraries(IOLib))
    goal = f"open('{path.as_uri()}', read, S), read(S, X), read(S, Y), close(S)"
    solution = solve_all(solver, goal)[0]
    assert solution.is_yes
    assert (bindings([solution], "X"), bindings([solution], "Y")) == (["f(a)"], ["g(b)"])


def test_io_lib_writes_files(tmp_path):
    path = tmp_path / "out.txt"
    solver = prolog_solver(libraries=libraries(IOLib))
    goal = f"open('{path.as_uri()}', write, S), write(S, 'è'), close(S)"
    assert solve_all(solver, goal)[0].is_yes
    assert path.read_text(encoding="utf-8") == "è"
