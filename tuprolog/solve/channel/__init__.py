"""Input and output channels: how solvers read and write, e.g. for `write/1` or warnings.

A *channel* connects a solver to the outside world: solvers read strings from *input channels*
(e.g. their standard input), and write strings on *output channels* (e.g. their standard output
and error), plus warnings on a dedicated channel. Channels are created from Python callables or
streams, so the output of `write/1` can go to `sys.stdout`, an `io.StringIO`, or a list.

Solvers hold their channels in *stores*, by name (an *alias*): `InputStore` (with `stdin`) and
`OutputStore` (with `stdout` and `stderr`), where predicates opening streams add theirs.

Main types and functions:

- `InputChannel` and `OutputChannel` (both `Channel`s), created by `input_channel` and
  `output_channel`; `ensure_input_channel` and `ensure_output_channel` convert Python streams and
  callables;
- `std_in`, `std_out`, `std_err` and `warn`: channels on Python's `sys.stdin`, `sys.stdout` and
  `sys.stderr`, the default ones of solvers;
- `InputStore` and `OutputStore` (both `ChannelStore`s), created by `input_store` and
  `output_store`;
- `Listener`, created by `listener`: a callback receiving everything transiting a channel.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> written = []
    >>> solver = prolog_solver(std_out=output_channel(written.append))
    >>> solver.solve_once("write(hello), write(world)").is_yes
    True
    >>> written
    ['hello', 'world']

See Also:
    - `tuprolog.solve.libs.io`, for predicates reading and writing streams and files.
    - 2P-Kt's [solver API](https://tuprolog.github.io/2p-kt/reference/solver-api/) and its
      [I/O library](https://tuprolog.github.io/2p-kt/reference/io-lib/).
"""

from ._api import *
from ._definitions import *

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
