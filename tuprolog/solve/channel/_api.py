import codecs
import sys
from collections.abc import Callable, Mapping
from functools import singledispatch
from io import IOBase, TextIOBase
from typing import IO, Any

from java.lang import Throwable  # type: ignore
from jpype import JObject, JString

from tuprolog.jvmioutils import InputStream, ensure_reader
from tuprolog.jvmutils import jmap, kfunction

from ._definitions import (
    InputChannel,
    InputStore,
    Listener,
    OutputChannel,
    OutputStore,
    ReaderChannel,
)

__all__ = [
    "ensure_input_channel",
    "ensure_output_channel",
    "input_channel",
    "input_channel_from_stream",
    "input_channel_from_string",
    "input_store",
    "listener",
    "output_channel",
    "output_store",
    "std_err",
    "std_in",
    "std_out",
    "warn",
]


def _read_char_from_stdin() -> str | None:
    sys.stdout.flush()  # like input(), show pending prompts before blocking
    return sys.stdin.read(1) or None


def std_in() -> InputChannel:
    """The input channel reading from Python's current `sys.stdin`."""
    return input_channel(_read_char_from_stdin)


@singledispatch
def input_channel(
    generator: Callable | str | IOBase, availability_checker: Callable | None = None
) -> InputChannel:
    if availability_checker is None:
        return InputChannel.of(kfunction(0)(generator))
    else:
        return InputChannel.of(kfunction(0)(generator), kfunction(0)(availability_checker))


@input_channel.register
def input_channel_from_string(string: str) -> InputChannel:
    return InputChannel.of(string)


@input_channel.register
def input_channel_from_stream(stream: IOBase) -> InputChannel:
    """The input channel reading from a Python stream (text, or UTF-8 encoded binary)."""
    if isinstance(stream, InputStream):
        return ReaderChannel(ensure_reader(stream))
    # read by code points: 2P-Kt's ReaderChannel splits astral characters into surrogates
    text = stream if isinstance(stream, TextIOBase) else codecs.getreader("utf-8")(stream)
    return input_channel(lambda: text.read(1) or None)  # type: ignore[attr-defined]


def ensure_input_channel(
    channel: InputChannel | IOBase | Callable | None, default: Callable[[], InputChannel] = std_in
) -> InputChannel:
    """Turns a Python stream, or a generator of strings, into an input channel."""
    if channel is None:
        return default()
    elif isinstance(channel, InputChannel):
        return channel
    elif isinstance(channel, IOBase) or callable(channel):
        return input_channel(channel)
    else:
        raise TypeError(f"Invalid type: {type(channel)}")


def input_store(
    stdin: InputChannel | IOBase | None = None,
    channels: Mapping[str, InputChannel | IOBase] | None = None,
) -> InputStore:
    cs = {InputStore.STDIN: ensure_input_channel(stdin)}
    for k, v in (channels or {}).items():
        cs[k] = ensure_input_channel(v)
    return InputStore.of(jmap(cs))


def _write_to(stream: IO | IOBase, value: Any) -> None:
    # warnings are printed by message, one per line, as 2P-Kt does
    text = f"{value.getMessage()}\n" if isinstance(value, Throwable) else str(value)
    stream.write(text if isinstance(stream, TextIOBase) else text.encode("utf-8"))  # type: ignore[attr-defined]


def std_out() -> OutputChannel:
    """The output channel writing on Python's current `sys.stdout`."""
    return output_channel(lambda value: _write_to(sys.stdout, value))


def std_err() -> OutputChannel:
    """The output channel writing on Python's current `sys.stderr`."""
    return output_channel(lambda value: _write_to(sys.stderr, value))


def warn() -> OutputChannel:
    """The output channel writing warnings' messages on Python's current `sys.stderr`."""
    return output_channel(lambda warning: _write_to(sys.stderr, warning))


def _pythonic(value: Any) -> Any:
    return str(value) if isinstance(value, JString) else value


def output_channel(consumer: Callable | IOBase) -> OutputChannel:
    """The output channel feeding a Python callable, or writing on a Python stream."""
    if isinstance(consumer, IOBase):
        stream = consumer
        return OutputChannel.of(kfunction(1)(lambda value: _write_to(stream, value)))
    return OutputChannel.of(kfunction(1)(lambda value: consumer(_pythonic(value))))


def ensure_output_channel(
    channel: OutputChannel | IOBase | Callable | None,
    default: Callable[[], OutputChannel] = std_out,
) -> OutputChannel:
    """Turns a Python stream, or a consumer, into an output channel."""
    if channel is None:
        return default()
    elif isinstance(channel, OutputChannel):
        return channel
    elif isinstance(channel, IOBase) or callable(channel):
        return output_channel(channel)
    else:
        raise TypeError(f"Invalid type: {type(channel)}")


def output_store(
    stdout: OutputChannel | IOBase | None = None,
    stderr: OutputChannel | IOBase | None = None,
    warnings: OutputChannel | IOBase | None = None,
    channels: Mapping[str, OutputChannel | IOBase] | None = None,
) -> OutputStore:
    cs = {
        OutputStore.STDOUT: ensure_output_channel(stdout, std_out),
        OutputStore.STDERR: ensure_output_channel(stderr, std_err),
    }
    for k, v in (channels or {}).items():
        cs[k] = ensure_output_channel(v)
    return OutputStore.of(jmap(cs), ensure_output_channel(warnings, warn))


def listener(consumer: Callable) -> Listener:
    return JObject(kfunction(1)(consumer), Listener)
