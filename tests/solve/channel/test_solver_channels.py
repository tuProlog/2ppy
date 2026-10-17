"""Channels backed by Python callables, plugged into solvers."""

import jpype.imports  # noqa: F401
import pytest
from it.unibo.tuprolog.solve.libs.io import IOLib  # type: ignore

from tests.solve.primitive._support import bindings, solve_all
from tuprolog.solve.channel import input_channel, output_channel
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, Unknown
from tuprolog.solve.library import libraries
from tuprolog.solve.prolog import prolog_solver

IO = IOLib.INSTANCE


def test_write_on_python_stdout():
    written: list[str] = []
    solver = prolog_solver(std_out=output_channel(written.append))
    assert solve_all(solver, "write(hello), write(' '), write(f(X, 1)), nl")[0].is_yes
    assert "".join(written).startswith("hello f(")
    assert written[-1] == "\n"


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 0.31.16: MutableSolver.setStandardOutput leaves write/1 on the old channel",
)
def test_stdout_can_be_replaced_on_mutable_solvers():
    first, second = [], []
    solver = prolog_solver(std_out=output_channel(first.append))
    solver.setStandardOutput(output_channel(second.append))
    solve_all(solver, "write(x)")
    assert (first, second) == ([], ["x"])


def test_write_on_python_stderr():
    written: list[str] = []
    solver = prolog_solver(libraries=IO, std_err=output_channel(written.append))
    assert solve_all(solver, "write(stderr, oops)")[0].is_yes
    assert "".join(written) == "oops"


def test_warnings_on_python_channel():
    warnings: list = []
    solver = prolog_solver(warning=output_channel(warnings.append))
    assert solve_all(solver, "undefined_predicate")[0].is_no
    assert len(warnings) == 1
    assert "undefined_predicate" in str(warnings[0])


def test_no_warnings_when_unknown_is_fail():
    warnings: list = []
    solver = prolog_solver(
        flags=DEFAULT_FLAG_STORE.set(Unknown, Unknown.FAIL),
        warning=output_channel(warnings.append),
    )
    assert solve_all(solver, "undefined_predicate")[0].is_no
    assert warnings == []


def test_read_term_from_string_channel():
    solver = prolog_solver(libraries=IO, std_in=input_channel("foo(bar, Y)."))
    assert bindings(solve_all(solver, "read(X)"), "X")[0].startswith("foo(bar, ")


def test_get_char_from_callable_channel():
    chars = iter("hi")
    solver = prolog_solver(libraries=IO, std_in=input_channel(lambda: next(chars, None)))
    solutions = solve_all(solver, "get_char(A), peek_char(B), get_char(C), get_char(D)")
    assert [bindings(solutions, v)[0] for v in "ABCD"] == ["h", "i", "i", "end_of_file"]


def test_echo_from_python_input_to_python_output():
    written: list[str] = []
    solver = prolog_solver(
        libraries=libraries(IO),
        std_in=input_channel("ab"),
        std_out=output_channel(written.append),
    )
    assert solve_all(solver, "get_char(X), put_char(X), get_char(Y), put_char(Y)")[0].is_yes
    assert "".join(written) == "ab"


@pytest.mark.xfail(
    strict=True, reason="2P-Kt 0.31.16 fails on a second read/1 from a string channel"
)
def test_read_many_terms_from_string_channel():
    solver = prolog_solver(libraries=IO, std_in=input_channel("a. b.\n"))
    solutions = solve_all(solver, "read(X), read(Y)")
    assert bindings(solutions, "X") == ["a"]
    assert bindings(solutions, "Y") == ["b"]


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 0.31.16 cannot read terms from InputChannelFromFunction (callable channels)",
)
def test_read_term_from_callable_channel():
    chars = iter("foo(bar).\n")
    solver = prolog_solver(libraries=IO, std_in=input_channel(lambda: next(chars, None)))
    assert bindings(solve_all(solver, "read(X)"), "X") == ["foo(bar)"]
