"""The JVM types of channels and channel stores, re-exported by `tuprolog.solve.channel`."""

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
    "ReaderChannel",
    "WriterChannel",
]


Channel = _channel.Channel
"""A channel of communication between a solver and the outside world (base of input and output).

Members: `close()`, `is_closed`, `stream_term` (the term denoting the channel in Prolog
programs), and `addListener(listener)`, `removeListener(listener)`, `clearListeners()`, to
register callbacks receiving every element transiting the channel (see `listener`).
"""


ChannelStore = _channel.ChannelStore
"""An immutable map of channels by alias (base of `InputStore` and `OutputStore`).

Besides the read-only JVM map members (e.g. `keys()`, `get(alias)`), stores have the `current`
channel (aliased `$current`, where predicates like `write/1` write by default), `aliases_of(channel)`
and `find_by_term(stream_term)`. Changes return new stores: `plus(...)` (alias-channel pairs),
`minus(...)` (aliases), `set_current(...)`, `close(channel)`.
"""


InputChannel = _channel.InputChannel
"""A channel solvers read strings from, e.g. their standard input.

Members: `read()` (the next string, `None` at the end), `peek()` (the next string, without
consuming it), `available`, `is_over`, and those of `Channel`. Create input channels with
`input_channel`.

Examples:
    >>> from tuprolog.solve.channel import input_channel
    >>> channel = input_channel("ab")
    >>> channel.read(), channel.peek(), channel.read(), channel.read()
    ('a', 'b', 'b', None)
"""


InputStore = _channel.InputStore
"""The input channels of a solver, by alias (a `ChannelStore`).

Its standard input, `std_in`, is aliased `stdin` (`InputStore.STDIN`, also `user_input`). Create
input stores with `input_store`.
"""


OutputChannel = _channel.OutputChannel
"""A channel solvers write on, e.g. their standard output, standard error, or warnings.

Members: `write(value)`, `flush()`, and those of `Channel`. Create output channels with
`output_channel`.

Examples:
    >>> from tuprolog.solve.channel import output_channel
    >>> received = []
    >>> output_channel(received.append).write("hello")
    >>> received
    ['hello']
"""


OutputStore = _channel.OutputStore
"""The output channels of a solver, by alias (a `ChannelStore`), plus the channel of warnings.

Its standard output, `std_out`, is aliased `stdout` (`OutputStore.STDOUT`, also `user_output`),
its standard error, `std_err`, `stderr` (`OutputStore.STDERR`); the channel of warnings,
`warnings`, has no alias. Create output stores with `output_store`.
"""


Listener = _kfunctions.Function1
"""A callback receiving every element transiting a channel: a Kotlin function of one argument.

Create listeners from Python callables with `listener`, and register them with
`channel.addListener(listener)`.
"""


ReaderChannel = _channel.ReaderChannel
"""An input channel reading a JVM `java.io.Reader` (or `InputStream`), one character at a time.

`input_channel` creates one for JVM input streams (see `tuprolog.jvmioutils`).
"""


WriterChannel = _channel.WriterChannel
"""An output channel writing on a JVM `java.io.Writer` (or `OutputStream`)."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.channel.*")
