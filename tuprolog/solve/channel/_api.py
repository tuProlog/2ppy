from collections.abc import Callable, Mapping
from functools import singledispatch

from jpype import JObject, JString

from tuprolog.jvmutils import jmap, kfunction

from ._definitions import InputChannel, InputStore, Listener, OutputChannel, OutputStore

__all__ = [
    "input_channel",
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


def std_in() -> InputChannel:
    return InputChannel.stdIn()


@singledispatch
def input_channel(
    generator: Callable | str, availability_checker: Callable | None = None
) -> InputChannel:
    if availability_checker is None:
        return InputChannel.of(kfunction(0)(generator))
    else:
        return InputChannel.of(kfunction(0)(generator), kfunction(0)(availability_checker))


@input_channel.register
def input_channel_from_string(string: str) -> InputChannel:
    return InputChannel.of(string)


def input_store(
    stdin: InputChannel | None = None, channels: Mapping[str, InputChannel] | None = None
) -> InputStore:
    if stdin is None and channels is None:
        return InputStore.fromStandard()
    elif channels is None:
        return InputStore.fromStandard(stdin)
    else:
        cs = {InputStore.STDIN: stdin or std_in()}
        for k, v in channels.items():
            cs[k] = v
        return InputStore.of(jmap(cs))


def std_out() -> OutputChannel:
    return OutputChannel.stdOut()


def std_err() -> OutputChannel:
    return OutputChannel.stdErr()


def warn() -> OutputChannel:
    return OutputChannel.warn()


def _pythonic(value):
    return str(value) if isinstance(value, JString) else value


def output_channel(consumer: Callable) -> OutputChannel:
    return OutputChannel.of(kfunction(1)(lambda value: consumer(_pythonic(value))))


def output_store(
    stdout: OutputChannel | None = None,
    stderr: OutputChannel | None = None,
    warnings: OutputChannel | None = None,
    channels: Mapping[str, OutputChannel] | None = None,
) -> OutputStore:
    if channels is None and all(channel is None for channel in (stdout, stderr, warnings)):
        return OutputStore.fromStandard()
    elif channels is None:
        return OutputStore.fromStandard(
            stdout or std_out(), stderr or std_err(), warnings or warn()
        )
    else:
        cs = {OutputStore.STDOUT: stdout or std_out(), OutputStore.STDERR: stderr or std_err()}
        for k, v in channels.items():
            cs[k] = v
        return OutputStore.of(jmap(cs), warnings or warn())


def listener(consumer: Callable) -> Listener:
    return JObject(kfunction(1)(consumer), Listener)
