"""JVM types of theory parsers, re-exported from 2P-Kt's
`it.unibo.tuprolog.theory.parsing`."""

import it.unibo.tuprolog.theory.parsing as _parsing  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["DEFAULT_CLAUSES_PARSER", "DEFAULT_CLAUSES_READER", "ClausesParser", "ClausesReader"]


ClausesParser = _parsing.ClausesParser
"""A parser of clauses and theories from strings.

Each parser has a default operator set, used unless another one is passed to its methods.
Create parsers with `tuprolog.theory.parsing.clauses_parser`.

Members:
    - `parse_theory(input, operators=None)`: the `tuprolog.theory.Theory` of the clauses in a
      string.
    - `parse_clauses(input, operators=None)`: the list of the clauses in a string.
    - `parse_clauses_lazily(input, operators=None)`: the clauses in a string, as a lazy iterable
      parsing them on demand.
    - `default_operator_set`: the operators the parser knows by default.

Examples:
    >>> parser = ClausesParser.withDefaultOperators()
    >>> parser.parse_clauses("a. b.")
    [a :- true, b :- true]

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.theory.parsing.ClausesParser` interface.
"""


ClausesReader = _parsing.ClausesReader
"""A reader of clauses and theories from files or streams.

Inputs may be paths (strings or path-like objects), Python streams (text ones are UTF-8
encoded), or JVM input streams. Create readers with `tuprolog.theory.parsing.clauses_reader`.

Members:
    - `read_theory(input, operators=None)`: the `tuprolog.theory.Theory` of the clauses in
      the input.
    - `read_clauses(input, operators=None)`: the list of the clauses in the input.
    - `read_clauses_lazily(input, operators=None)`: the clauses in the input, as a lazy
      iterable reading them on demand.
    - `default_operator_set`: the operators the reader knows by default.

Examples:
    >>> import io
    >>> ClausesReader.withDefaultOperators().read_clauses(io.StringIO("a. b."))
    [a :- true, b :- true]

Note:
    Wraps 2P-Kt's `it.unibo.tuprolog.theory.parsing.ClausesReader` interface.
"""


DEFAULT_CLAUSES_PARSER = ClausesParser.withDefaultOperators()
"""The `ClausesParser` knowing the standard Prolog operators, used by
`tuprolog.theory.parsing.parse_theory` and `tuprolog.theory.parsing.parse_clauses`."""


DEFAULT_CLAUSES_READER = ClausesReader.withDefaultOperators()
"""The `ClausesReader` knowing the standard Prolog operators, used by
`tuprolog.theory.parsing.read_theory` and `tuprolog.theory.parsing.read_clauses`."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.parsing.*")
