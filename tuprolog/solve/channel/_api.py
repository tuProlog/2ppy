"""The factory functions of channels and channel stores, re-exported by `tuprolog.solve.channel`."""

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
    """Creates an input channel reading Python's `sys.stdin`, one character at a time.

    `sys.stdin` is looked up at each read, so it follows its replacements (e.g. by tests), and
    `sys.stdout` is flushed before each read, as `input()` does, to show pending prompts.

    Returns:
        The input channel; solvers use one by default.
    """
    return input_channel(_read_char_from_stdin)


@singledispatch
def input_channel(
    generator: Callable | str | IOBase, availability_checker: Callable | None = None
) -> InputChannel:
    """Creates an input channel from a Python callable, a string, or a Python stream.

    Strings and streams are read one character at a time (see `input_channel_from_string` and
    `input_channel_from_stream`).

    Args:
        generator: A callable taking no argument, and returning the next string at each call,
            or `None` at the end; or a string, or a Python stream.
        availability_checker: For callables, a callable taking no argument and returning whether
            more strings are available; by default, they are while `generator` returns strings.

    Returns:
        The input channel.

    Examples:
        >>> lines = iter(["first", "second"])
        >>> channel = input_channel(lambda: next(lines, None))
        >>> channel.read(), channel.read(), channel.read()
        ('first', 'second', None)
    """
    if availability_checker is None:
        return InputChannel.of(kfunction(0)(generator))
    else:
        return InputChannel.of(kfunction(0)(generator), kfunction(0)(availability_checker))


@input_channel.register
def input_channel_from_string(string: str) -> InputChannel:
    """Creates an input channel reading a string, one character at a time.

    Args:
        string: The text to read.

    Returns:
        The input channel, also returned by `input_channel(string)`.

    Examples:
        >>> channel = input_channel_from_string("hi")
        >>> channel.read(), channel.read(), channel.read()
        ('h', 'i', None)
    """
    return InputChannel.of(string)


@input_channel.register
def input_channel_from_stream(stream: IOBase) -> InputChannel:
    """Creates an input channel reading a Python stream, one character at a time.

    Args:
        stream: A text stream, a binary stream (decoded as UTF-8), or a JVM input stream from
            `tuprolog.jvmioutils` (read through a `ReaderChannel`).

    Returns:
        The input channel, also returned by `input_channel(stream)`.

    Examples:
        >>> import io
        >>> channel = input_channel_from_stream(io.BytesIO("né".encode()))
        >>> channel.read(), channel.read(), channel.read()
        ('n', 'é', None)
    """
    if isinstance(stream, InputStream):
        return ReaderChannel(ensure_reader(stream))
    # read by code points: 2P-Kt's ReaderChannel splits astral characters into surrogates
    text = stream if isinstance(stream, TextIOBase) else codecs.getreader("utf-8")(stream)
    return input_channel(lambda: text.read(1) or None)  # type: ignore[attr-defined]


def ensure_input_channel(
    channel: InputChannel | IOBase | Callable | None, default: Callable[[], InputChannel] = std_in
) -> InputChannel:
    """Converts a Python stream or callable into an input channel, leaving input channels as they are.

    Args:
        channel: An input channel, a Python stream, a callable (see `input_channel`), or `None`.
        default: A function creating the input channel to return for `None`; by default,
            `std_in`.

    Returns:
        The input channel.

    Raises:
        TypeError: If `channel` is of none of the types above.
    """
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
    """Creates a store of input channels.

    Args:
        stdin: The standard input, converted by `ensure_input_channel`; by default, `std_in()`.
        channels: More input channels (or Python streams), by alias.

    Returns:
        The input store, also aliasing the standard input as the current input.

    Examples:
        >>> store = input_store(channels={"data": input_channel("x")})
        >>> sorted(store.keys())
        ['$current', 'data', 'stdin']
    """
    cs = {InputStore.STDIN: ensure_input_channel(stdin)}
    for k, v in (channels or {}).items():
        cs[k] = ensure_input_channel(v)
    return InputStore.of(jmap(cs))


def _write_to(stream: IO | IOBase, value: Any) -> None:
    # warnings are printed by message, one per line, as 2P-Kt does
    text = f"{value.getMessage()}\n" if isinstance(value, Throwable) else str(value)
    stream.write(text if isinstance(stream, TextIOBase) else text.encode("utf-8"))  # type: ignore[attr-defined]


def std_out() -> OutputChannel:
    """Creates an output channel writing on Python's `sys.stdout`, as looked up at each write.

    Returns:
        The output channel; solvers use one by default.
    """
    return output_channel(lambda value: _write_to(sys.stdout, value))


def std_err() -> OutputChannel:
    """Creates an output channel writing on Python's `sys.stderr`, as looked up at each write.

    Returns:
        The output channel; solvers use one as standard error by default.
    """
    return output_channel(lambda value: _write_to(sys.stderr, value))


def warn() -> OutputChannel:
    """Creates an output channel writing the messages of warnings on Python's `sys.stderr`.

    Each warning's message is written on a line of its own; `sys.stderr` is looked up at each
    write.

    Returns:
        The output channel; solvers use one for warnings by default.
    """
    return output_channel(lambda warning: _write_to(sys.stderr, warning))


def _pythonic(value: Any) -> Any:
    return str(value) if isinstance(value, JString) else value


def output_channel(consumer: Callable | IOBase) -> OutputChannel:
    """Creates an output channel feeding a Python callable, or writing on a Python stream.

    Args:
        consumer: A callable taking each value written (a Python string for strings, else the
            JVM object, e.g. a `tuprolog.solve.exception.Warning`); or a text stream, or a binary
            stream (written in UTF-8), on which values are written as strings (warnings as their
            message, on a line of their own).

    Returns:
        The output channel.

    Examples:
        >>> import io
        >>> buffer = io.StringIO()
        >>> output_channel(buffer).write("hello")
        >>> buffer.getvalue()
        'hello'
    """
    if isinstance(consumer, IOBase):
        stream = consumer
        return OutputChannel.of(kfunction(1)(lambda value: _write_to(stream, value)))
    return OutputChannel.of(kfunction(1)(lambda value: consumer(_pythonic(value))))


def ensure_output_channel(
    channel: OutputChannel | IOBase | Callable | None,
    default: Callable[[], OutputChannel] = std_out,
) -> OutputChannel:
    """Converts a Python stream or callable into an output channel, leaving output channels as they are.

    Args:
        channel: An output channel, a Python stream, a callable (see `output_channel`), or
            `None`.
        default: A function creating the output channel to return for `None`; by default,
            `std_out`.

    Returns:
        The output channel.

    Raises:
        TypeError: If `channel` is of none of the types above.
    """
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
    """Creates a store of output channels.

    Args:
        stdout: The standard output, converted by `ensure_output_channel`; by default,
            `std_out()`.
        stderr: The standard error; by default, `std_err()`.
        warnings: The channel of warnings; by default, `warn()`.
        channels: More output channels (or Python streams or callables), by alias.

    Returns:
        The output store, also aliasing the standard output as the current output.

    Examples:
        >>> sorted(output_store().keys())
        ['$current', 'stderr', 'stdout']
    """
    cs = {
        OutputStore.STDOUT: ensure_output_channel(stdout, std_out),
        OutputStore.STDERR: ensure_output_channel(stderr, std_err),
    }
    for k, v in (channels or {}).items():
        cs[k] = ensure_output_channel(v)
    return OutputStore.of(jmap(cs), ensure_output_channel(warnings, warn))


def listener(consumer: Callable) -> Listener:
    """Creates a listener of channels from a Python callable.

    Args:
        consumer: A callable taking each element transiting the channels it listens to.

    Returns:
        The listener, to register with `channel.addListener(listener)`.

    Examples:
        >>> seen = []
        >>> channel = output_channel(lambda _: None)
        >>> channel.addListener(listener(seen.append))
        >>> channel.write("x")
        >>> seen
        ['x']
    """
    return JObject(kfunction(1)(consumer), Listener)
