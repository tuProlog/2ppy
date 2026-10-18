"""The JVM objects of the standard library, re-exported by `tuprolog.solve.stdlib`."""

import it.unibo.tuprolog.solve.stdlib as _stdlib  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["CommonBuiltins", "CommonFunctions", "CommonPrimitives", "CommonRules"]


CommonBuiltins: _stdlib.CommonBuiltins = _stdlib.CommonBuiltins.INSTANCE
"""The standard library, aliased `prolog.lang`: a `tuprolog.solve.library.Library`.

It bundles `CommonPrimitives`, `CommonFunctions`, `CommonRules` and the standard operators; Prolog
solvers load it (extended with a few solver-specific predicates, e.g. `call/1` and `catch/3`).

Examples:
    >>> CommonBuiltins.alias
    'prolog.lang'
"""


CommonFunctions: _stdlib.CommonFunctions = _stdlib.CommonFunctions.INSTANCE
"""The functions of the standard library (see `tuprolog.solve.stdlib.function`).

Members: `functions` (a JVM map from signatures to logic functions) and `wrappers`.
"""


CommonPrimitives: _stdlib.CommonPrimitives = _stdlib.CommonPrimitives.INSTANCE
"""The primitives of the standard library (see `tuprolog.solve.stdlib.primitive`).

Members: `primitives` (a JVM map from signatures to primitives) and `wrappers`.
"""


CommonRules: _stdlib.CommonRules = _stdlib.CommonRules.INSTANCE
"""The rules of the standard library (see `tuprolog.solve.stdlib.rule`).

Members: `clauses` (a list of clauses) and `wrappers`.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.*")
