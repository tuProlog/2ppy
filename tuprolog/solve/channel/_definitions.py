import it.unibo.tuprolog.solve.channel as _channel  # type: ignore
import jpype.imports  # noqa: F401
import kotlin.jvm.functions as _kfunctions  # type: ignore

from tuprolog import logger

__all__ = [
    "Channel",
    "ChannelStore",
    "InputChannel",
    "InputStore",
    "Listener",
    "OutputChannel",
    "OutputStore",
]


Channel = _channel.Channel


ChannelStore = _channel.ChannelStore


InputChannel = _channel.InputChannel


InputStore = _channel.InputStore


OutputChannel = _channel.OutputChannel


OutputStore = _channel.OutputStore


Listener = _kfunctions.Function1


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.channel.*")
