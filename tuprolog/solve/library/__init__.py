"""Libraries: bundles of predicates, functions, clauses and operators that solvers load.

A *library* extends solvers with:

- *primitives*: predicates implemented in Python (see `tuprolog.solve.primitive`);
- *functions*: functions usable in arithmetic, e.g. by `is/2` (see `tuprolog.solve.function`);
- *clauses*: predicates written in Prolog;
- *operators*: e.g. `::` for ProbLog (see `tuprolog.core.operators`).

Primitives and functions are keyed by *signature*, i.e. name and arity (see
`tuprolog.solve.signature`). Libraries have an *alias*, i.e. a name made of dot-separated words
(e.g. `prolog.lang`, the standard library), identifying them in solvers.

A solver loads a *runtime*, i.e. a set of libraries with distinct aliases: e.g. the standard
library, plus the ones given to `tuprolog.solve.prolog.prolog_solver(libraries=...)`.

Main types and functions:

- `Library`, created by `library` (and re-aliased by `aliased`);
- `Runtime`, created by `libraries`;
- `Pluggable`, what libraries and runtimes have in common.

Examples:
    >>> from tuprolog.solve.function import function
    >>> from tuprolog.solve.primitive import predicate
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> from tuprolog.theory.parsing import parse_clauses
    >>> strings = library(
    ...     "my.strings",
    ...     primitives={"upper/2": predicate(lambda text, _: [(text, text.upper())])},
    ...     functions={"half/1": function(lambda x: x / 2)},
    ...     clauses=parse_clauses("shout(X, Y) :- upper(X, Y)."),
    ... )
    >>> solver = prolog_solver(libraries=strings)
    >>> list(solver.query("shout(hello, Y), H is half(3)"))
    [{'Y': 'HELLO', 'H': 1.5}]

See Also:
    - `tuprolog.solve.libs`, the libraries shipped with 2P-Kt (e.g. input/output).
    - `tuprolog.solve.library.exception`, the errors of loading libraries.
    - 2P-Kt's [libraries](https://tuprolog.github.io/2p-kt/reference/libraries/).
"""

import tuprolog.solve.library._adapters as _

from ._api import *
from ._definitions import *

__all__ = ["Library", "Pluggable", "Runtime", "aliased", "libraries", "library"]
