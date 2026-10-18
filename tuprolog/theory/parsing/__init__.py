"""Parsing theories, i.e. sequences of clauses, from Prolog source code.

Prolog source code is a sequence of clauses, each one terminated by a full stop (`.`), e.g.
`parent(abe, homer). grandparent(X, Z) :- parent(X, Y), parent(Y, Z).`. This package turns such
text into `tuprolog.core.Clause`s, or into a whole `tuprolog.theory.Theory`:

- *parsers* (`ClausesParser`, and the `parse_*` functions) take strings;
- *readers* (`ClausesReader`, and the `read_*` functions) take files (paths) or streams, either
  Python ones (e.g. `open("kb.pl")`, `io.StringIO`, `io.BytesIO`) or JVM ones.

Parsing depends on the *operators* in use (see `tuprolog.core.operators`): operators let terms be
written in infix, prefix or postfix notation, e.g. `X is 1 + 2` for `is(X, +(1, 2))`. By default,
the standard Prolog operators are known; custom ones can be added by passing an `OperatorSet`.

Invalid source code raises `tuprolog.errors.ParsingError`s (which are `ValueError`s), telling
where the error is.

Examples:
    >>> import io
    >>> parse_theory("parent(abe, homer). parent(homer, bart).")
    IndexedTheory{ parent(abe, homer) :- true. parent(homer, bart) :- true }
    >>> list(parse_clauses("a. b :- a."))
    [a :- true, b :- a]
    >>> read_theory(io.StringIO("likes(X, pizza)."))
    IndexedTheory{ likes(X_..., pizza) :- true }

See Also:
    `tuprolog.core.parsing`, for parsing single terms; 2P-Kt's
    [parsing architecture](https://tuprolog.github.io/2p-kt/explanation/parsing-architecture/).
"""

import tuprolog.theory.parsing._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "DEFAULT_CLAUSES_PARSER",
    "DEFAULT_CLAUSES_READER",
    "ClausesParser",
    "ClausesReader",
    "clauses_parser",
    "clauses_reader",
    "parse_clauses",
    "parse_theory",
    "read_clauses",
    "read_theory",
]
