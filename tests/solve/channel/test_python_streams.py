"""Solver channels backed by Python streams, and Python's `sys` streams as default channels."""

import io
import sys

import pytest

from tests.solve.primitive._support import bindings, solve_all
from tuprolog.jvmioutils import ensure_input_stream
from tuprolog.solve.channel import (
    InputChannel,
    OutputChannel,
    ReaderChannel,
    ensure_input_channel,
    ensure_output_channel,
    input_channel,
    input_channel_from_stream,
    input_store,
    output_channel,
    output_store,
    std_err,
    std_in,
    std_out,
    warn,
)
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, Unknown
from tuprolog.solve.library import libraries
from tuprolog.solve.libs import IOLib
from tuprolog.solve.prolog import prolog_solver


def read_all(channel) -> list[str]:
    chars = []
    while (char := channel.read()) is not None:
        chars.append(str(char))
    return chars


@pytest.mark.parametrize("stream", [io.StringIO("aè😀"), io.BytesIO("aè😀".encode())])
def test_input_channel_from_python_streams(stream):
    assert read_all(input_channel(stream)) == ["a", "è", "😀"]


def test_input_channel_from_jvm_streams():
    channel = input_channel(ensure_input_stream(io.BytesIO(b"ab")))
    assert isinstance(channel, ReaderChannel)
    assert read_all(channel) == ["a", "b"]


def test_input_channel_from_stream_is_registered():
    assert "".join(read_all(input_channel_from_stream(io.StringIO("xy")))) == "xy"


@pytest.mark.parametrize("stream", [io.StringIO(), io.BytesIO()])
def test_output_channel_on_python_streams(stream):
    channel = output_channel(stream)
    channel.write("è")
    channel.write("x")
    value = stream.getvalue()
    assert (value if isinstance(value, str) else value.decode()) == "èx"


def test_solver_on_python_streams():
    out, err = io.StringIO(), io.BytesIO()
    solver = prolog_solver(
        libraries=libraries(IOLib),
        std_in=io.StringIO("hello('wòrld'). xy"),
        std_out=out,
        std_err=err,
    )
    solution = solve_all(solver, "read(X), write(X), nl, get_char(C), write(stderr, oops)")[0]
    assert solution.is_yes
    assert bindings([solution], "C") == ["x"]
    assert out.getvalue() == "hello(wòrld)\n"
    assert err.getvalue() == b"oops"


def test_solver_warnings_on_python_streams():
    warnings = io.StringIO()
    solver = prolog_solver(flags=DEFAULT_FLAG_STORE.set(Unknown, Unknown.WARNING), warning=warnings)
    assert solve_all(solver, "missing")[0].is_no
    assert warnings.getvalue() == "No such a predicate: missing/0\n"


def test_default_channels_follow_python_sys_streams(capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("ab"))
    solver = prolog_solver(
        libraries=libraries(IOLib), flags=DEFAULT_FLAG_STORE.set(Unknown, Unknown.WARNING)
    )
    solution = solve_all(solver, "get_char(X), write(X), write(stderr, err), missing")[0]
    assert solution.is_no
    captured = capsys.readouterr()
    assert captured.out == "a"
    assert captured.err == "errNo such a predicate: missing/0\n"


def test_default_channels_resolve_sys_streams_lazily(monkeypatch):
    solver = prolog_solver()
    replaced = io.StringIO()
    monkeypatch.setattr(sys, "stdout", replaced)
    solve_all(solver, "write(late)")
    assert replaced.getvalue() == "late"


def test_std_in_flushes_pending_prompts(monkeypatch):
    class Recorder(io.StringIO):
        flushes = 0

        def flush(self):
            self.flushes += 1
            super().flush()

    stdout = Recorder()
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stdin", io.StringIO("z"))
    assert read_all(std_in()) == ["z"]
    assert stdout.flushes > 0


def test_standard_channel_factories():
    assert isinstance(std_in(), InputChannel)
    for factory in (std_out, std_err, warn):
        assert isinstance(factory(), OutputChannel)


def test_ensure_input_channel():
    channel = input_channel("x")
    assert ensure_input_channel(channel) is channel
    assert isinstance(ensure_input_channel(None), InputChannel)
    assert ensure_input_channel(None, lambda: channel) is channel
    assert read_all(ensure_input_channel(io.StringIO("ab"))) == ["a", "b"]
    chars = iter("cd")
    assert read_all(ensure_input_channel(lambda: next(chars, None))) == ["c", "d"]
    with pytest.raises(TypeError, match="Invalid type"):
        ensure_input_channel(42)  # type: ignore[arg-type]


def test_ensure_output_channel():
    channel = output_channel(print)
    assert ensure_output_channel(channel) is channel
    assert isinstance(ensure_output_channel(None), OutputChannel)
    assert ensure_output_channel(None, lambda: channel) is channel
    written: list[str] = []
    ensure_output_channel(written.append).write("w")
    stream = io.StringIO()
    ensure_output_channel(stream).write("s")
    assert (written, stream.getvalue()) == (["w"], "s")
    with pytest.raises(TypeError, match="Invalid type"):
        ensure_output_channel(42)  # type: ignore[arg-type]


def test_stores_accept_python_streams():
    inputs = input_store(io.StringIO("i"), {"foo": io.StringIO("f")})
    assert read_all(inputs.std_in) == ["i"]
    assert read_all(inputs["foo"]) == ["f"]
    out, err, foo = io.StringIO(), io.StringIO(), io.StringIO()
    outputs = output_store(out, err, channels={"foo": foo})
    outputs.std_out.write("o")
    outputs.std_err.write("e")
    outputs["foo"].write("f")
    assert (out.getvalue(), err.getvalue(), foo.getvalue()) == ("o", "e", "f")


def test_mutable_solver_channel_setters_accept_python_streams():
    solver = prolog_solver()
    solver.standard_input = io.StringIO("x")
    solver.standard_output = io.StringIO()
    solver.standard_error = io.BytesIO()
    solver.warnings = io.StringIO()
    for channel in (solver.standard_input,):
        assert isinstance(channel, InputChannel)
    for channel in (solver.standard_output, solver.standard_error, solver.warnings):
        assert isinstance(channel, OutputChannel)
