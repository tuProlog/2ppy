"""Side effects altering libraries, operators and channels."""

import jpype.imports  # noqa: F401
import pytest
from it.unibo.tuprolog.solve.libs.io import IOLib  # type: ignore

from tests.solve.primitive._support import bindings, solve_all
from tuprolog.core.operators import XFX, operator, operator_set
from tuprolog.solve import signature
from tuprolog.solve.channel import input_channel, output_channel
from tuprolog.solve.library import Library, libraries, library
from tuprolog.solve.primitive import primitive
from tuprolog.solve.sideffects import (
    AddLibraries,
    CloseInputChannels,
    CloseOutputChannels,
    LoadLibrary,
    OpenInputChannels,
    OpenOutputChannels,
    RemoveOperators,
    ResetInputChannels,
    ResetOperators,
    ResetOutputChannels,
    ResetRuntime,
    SetOperators,
    UnloadLibraries,
    UpdateLibrary,
    add_libraries,
    close_input_channels,
    close_output_channels,
    load_library,
    open_input_channels,
    open_output_channels,
    remove_operators,
    reset_input_channels,
    reset_libraries,
    reset_operators,
    reset_output_channels,
    set_operators,
    unload_libraries,
    update_library,
)

ARROW = operator("===>", XFX, 700)
TILDE = operator("~~>", XFX, 650)


def greeting(alias: str, name: str = "hello") -> Library:
    return library(alias, primitives={signature(name, 0): primitive(lambda r: [r.reply_success()])})


def aliases(runtime) -> set[str]:
    return {str(a) for a in runtime.keySet()}


# --- libraries ---


def test_load_library_factory():
    effect = load_library("x", greeting("a"))
    assert isinstance(effect, LoadLibrary)
    assert effect.library.alias == "x"


def test_update_library_factory():
    effect = update_library("x", greeting("a"))
    assert isinstance(effect, UpdateLibrary)
    assert effect.library.alias == "x"


@pytest.mark.parametrize(
    "factory, kind", [(add_libraries, AddLibraries), (reset_libraries, ResetRuntime)]
)
def test_runtime_factories(factory, kind):
    assert isinstance(factory(), kind)
    assert aliases(factory().libraries) == set()
    assert aliases(factory(greeting("a"), greeting("b")).libraries) == {"a", "b"}
    assert aliases(factory([greeting("a"), greeting("b")]).libraries) == {"a", "b"}
    assert aliases(factory(libraries(greeting("a"))).libraries) == {"a"}


@pytest.mark.parametrize(
    "arguments, expected",
    [(lambda: ("a", "b"), ["a", "b"]), (lambda: (["a", "b"],), ["a", "b"]), (lambda: (), [])],
    ids=["many", "list", "none"],
)
def test_unload_libraries_factory(arguments, expected):
    effect = unload_libraries(*arguments())
    assert isinstance(effect, UnloadLibraries)
    assert [str(a) for a in effect.aliases] == expected


def test_unload_libraries_with_single_alias():
    assert [str(a) for a in unload_libraries("abc").aliases] == ["abc"]


def test_load_library_end_to_end(emitting):
    solver = emitting(load_library("lib.greeting", greeting("ignored")))
    assert solve_all(solver, "hello")[0].is_no
    assert solve_all(solver, "emit, hello")[0].is_yes
    assert "lib.greeting" in aliases(solver.libraries)
    assert solve_all(solver, "'lib.greeting.hello'")[0].is_yes


def test_add_libraries_end_to_end(emitting):
    solver = emitting(add_libraries(greeting("a", "ciao"), greeting("b", "hola")))
    assert solve_all(solver, "emit, ciao, hola")[0].is_yes
    assert {"a", "b"} <= aliases(solver.libraries)


def test_update_library_end_to_end(emitting):
    solver = emitting(update_library("lib.greeting", greeting("x", "bye")))
    solver.load_library(greeting("lib.greeting"))
    assert solve_all(solver, "hello")[0].is_yes
    assert solve_all(solver, "emit, bye")[0].is_yes
    assert solve_all(solver, "hello")[0].is_no


def test_reset_libraries_end_to_end(emitting):
    solver = emitting(reset_libraries(greeting("only")))
    assert solve_all(solver, "emit")[0].is_yes
    assert aliases(solver.libraries) == {"only"}
    assert solve_all(solver, "hello")[0].is_yes


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 3.0.1: UnloadLibraries leaves loaded libraries in place (Runtime.minus is "
    "inverted)",
)
def test_unload_libraries_end_to_end(emitting):
    solver = emitting(unload_libraries(["lib.greeting"]))
    solver.load_library(greeting("lib.greeting"))
    assert solve_all(solver, "emit")[0].is_yes
    assert "lib.greeting" not in aliases(solver.libraries)


# --- operators ---


@pytest.mark.parametrize(
    "factory, kind",
    [
        (set_operators, SetOperators),
        (reset_operators, ResetOperators),
        (remove_operators, RemoveOperators),
    ],
)
@pytest.mark.parametrize(
    "arguments",
    [lambda: (ARROW, TILDE), lambda: ([ARROW, TILDE],), lambda: (operator_set(ARROW, TILDE),)],
    ids=["varargs", "list", "operator-set"],
)
def test_operator_factories(factory, kind, arguments):
    effect = factory(*arguments())
    assert isinstance(effect, kind)
    assert set(map(str, effect.operators)) == {str(ARROW), str(TILDE)}


def test_operator_factories_single_operator():
    assert list(set_operators(ARROW).operators) == [ARROW]


def _priority(solver, functor):
    solutions = solve_all(solver, f"current_op(P, xfx, '{functor}')")
    return bindings([s for s in solutions if s.is_yes], "P")


def test_set_operators_end_to_end(emitting):
    solver = emitting(set_operators(ARROW))
    assert _priority(solver, "===>") == []
    solve_all(solver, "emit")
    assert _priority(solver, "===>") == ["700"]
    assert _priority(solver, ":-") == ["1200"]


def test_remove_operators_end_to_end(emitting):
    solver = emitting(remove_operators(operator(":-", XFX, 1200)))
    solve_all(solver, "emit")
    assert _priority(solver, ":-") == []


@pytest.mark.xfail(
    strict=True, reason="2P-Kt 3.0.1: ResetOperators merges operators instead of replacing them"
)
def test_reset_operators_end_to_end(emitting):
    solver = emitting(reset_operators(ARROW))
    solve_all(solver, "emit")
    assert _priority(solver, "===>") == ["700"]
    assert _priority(solver, ":-") == []


# --- channels ---


@pytest.mark.parametrize(
    "factory, kind, make",
    [
        (open_input_channels, OpenInputChannels, lambda: input_channel("x")),
        (reset_input_channels, ResetInputChannels, lambda: input_channel("x")),
        (open_output_channels, OpenOutputChannels, lambda: output_channel(print)),
        (reset_output_channels, ResetOutputChannels, lambda: output_channel(print)),
    ],
)
def test_channel_factories(factory, kind, make):
    a, b = make(), make()
    for effect in [factory(), factory({"a": a}), factory(a=a), factory({"a": a}, b=b)]:
        assert isinstance(effect, kind)
    channels = factory({"a": a, "b": a}, b=b)
    mapping = channels.input_channels if hasattr(channels, "input_channels") else None
    if mapping is None:
        mapping = channels.output_channels
    assert {str(k) for k in mapping.keySet()} == {"a", "b"}
    assert mapping["b"] == b


@pytest.mark.parametrize(
    "factory, kind",
    [(close_input_channels, CloseInputChannels), (close_output_channels, CloseOutputChannels)],
)
def test_close_channel_factories(factory, kind):
    assert [str(n) for n in factory("a", "b").names] == ["a", "b"]
    assert [str(n) for n in factory(["a", "b"]).names] == ["a", "b"]
    assert isinstance(factory(), kind)


@pytest.mark.parametrize("factory", [close_input_channels, close_output_channels])
def test_close_channel_factories_with_single_name(factory):
    assert [str(n) for n in factory("foo").names] == ["foo"]


def test_open_output_channels_end_to_end(emitting):
    written: list[str] = []
    solver = emitting(open_output_channels(log=output_channel(written.append)))
    solver.load_library(IOLib.INSTANCE)
    assert solve_all(solver, "emit, write(log, hello)")[0].is_yes
    assert written == ["hello"]
    assert "log" in {str(k) for k in solver.output_channels.keySet()}


def test_open_input_channels_end_to_end(emitting):
    solver = emitting(open_input_channels(data=input_channel("xy")))
    solver.load_library(IOLib.INSTANCE)
    assert bindings(solve_all(solver, "emit, get_char(data, C)"), "C") == ["x"]


def test_close_output_channels_end_to_end(emitting):
    solver = emitting(close_output_channels(["log"]), std_out=output_channel(print))
    solver.load_library(IOLib.INSTANCE)
    solve_all(solver, "true")
    solver_channels = {str(k) for k in solver.output_channels.keySet()}
    assert "log" not in solver_channels
    assert solve_all(solver, "emit")[0].is_yes


def test_reset_input_channels_end_to_end(emitting):
    solver = emitting(reset_input_channels(data=input_channel("z")))
    solve_all(solver, "emit")
    keys = {str(k) for k in solver.input_channels.keySet()}
    assert "data" in keys
    assert "user_input" not in keys


def test_close_input_channels_end_to_end(emitting):
    solver = emitting(open_input_channels(data=input_channel("z")), close_input_channels(["data"]))
    solve_all(solver, "emit")
    assert "data" not in {str(k) for k in solver.input_channels.keySet()}


def test_reset_output_channels_end_to_end(emitting):
    solver = emitting(reset_output_channels(log=output_channel(print)))
    solve_all(solver, "emit")
    keys = {str(k) for k in solver.output_channels.keySet()}
    assert "log" in keys
    assert "user_output" not in keys
