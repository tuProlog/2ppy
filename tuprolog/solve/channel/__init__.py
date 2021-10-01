from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.channel as _channel
# noinspection PyUnresolvedReferences
import kotlin.jvm.functions as _kfunctions
from tuprolog.jvmutils import jmap, kfunction
from typing import Callable, Mapping
from functools import singledispatch

Channel = _channel.Channel

ChannelStore = _channel.ChannelStore

InputChannel = _channel.InputChannel

InputStore = _channel.InputStore

OutputChannel = _channel.OutputChannel

OutputStore = _channel.OutputStore

Listener = _kfunctions.Function1


def std_in() -> InputChannel:
    return InputChannel.stdIn()


@singledispatch
def input_channel(generator: Callable, availability_checker: Callable = None) -> InputChannel:
    if availability_checker is None:
        return InputChannel.of(kfunction(0)(generator))
    else:
        return InputChannel.of(kfunction(0)(generator), kfunction(0)(availability_checker))


@input_channel.register
def input_channel_from_string(string: str) -> InputChannel:
    return InputChannel.of(string)


def input_store(stdin: InputChannel = None, channels: Mapping[str, InputChannel] = None) -> InputStore:
    if stdin is None and channels is None:
        return InputStore.fromStandard()
    elif channels is None:
        return InputStore.fromStandard(stdin)
    else:
        cs = {InputStore.STDIN: stdin or std_in()}
        for k, v in channels:
            cs[k] = v
        return InputStore.of(jmap(cs))


def std_out() -> OutputChannel:
    return OutputChannel.stdOut()


def std_err() -> OutputChannel:
    return OutputChannel.stdErr()


def warn() -> OutputChannel:
    return OutputChannel.warn()


def output_channel(consumer: Callable) -> OutputChannel:
    return OutputChannel.of(kfunction(1)(consumer))


def output_store(
        stdout: OutputChannel = None,
        stderr: OutputChannel = None,
        warnings: OutputChannel = None,
        channels: Mapping[str, OutputChannel] = None
) -> OutputStore:
    if all((channel is None for channel in (stdout, stderr, warnings))):
        return OutputStore.fromStandard()
    elif channels is None:
        return OutputStore.fromStandard(
            stdout or std_out(),
            stderr or std_err(),
            warnings or warn()
        )
    else:
        cs = {
            OutputStore.STDOUT: stdout or std_out(),
            OutputStore.STDERR: stderr or std_err()
        }
        for k, v in channels:
            cs[k] = v
        return OutputStore.of(jmap(cs), warnings or warn())


def listener(consumer: Callable) -> Listener:
    return kfunction(1)(consumer)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.channel.*")
