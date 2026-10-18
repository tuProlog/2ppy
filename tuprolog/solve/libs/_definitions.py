import it.unibo.tuprolog.solve.libs.io as _io  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["IOLib"]


IOLib: _io.IOLib = _io.IOLib.INSTANCE
"""2P-Kt's library of ISO Prolog stream and I/O predicates (alias `prolog.io`).

A `tuprolog.solve.library.Library`, offering `open/3,4`, `close/1`, `read/1,2`, `read_term/2,3`,
`write/2`, `writeq/1,2`, `write_canonical/1,2`, `write_term/2,3`, `get_char/1,2`,
`put_char/1,2`, `consult/1`, `set_theory/1`, and more: see `tuprolog.solve.libs` for the full
list, and for what is not supported.

Examples:
    >>> import io
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> output = io.StringIO()
    >>> solver = prolog_solver(libraries=IOLib, std_out=output)
    >>> solver.solve_once("current_output(S), write_canonical(S, f('B', 1 + 2))").is_yes
    True
    >>> output.getvalue()
    "f('B', '+'(1, 2))"
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.libs.*")
