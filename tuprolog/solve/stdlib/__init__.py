"""The standard library: the predicates, functions and operators Prolog solvers load by default.

It mostly follows ISO Prolog: type checks (`atom/1`, `var/1`, ...), term inspection
(`functor/3`, `=../2`, ...), arithmetic (`is/2`, `</2`, ...), atoms (`atom_length/2`,
`sub_atom/5`, ...), the knowledge base (`assertz/1`, `retract/1`, ...), all-solutions predicates
(`findall/3`, `bagof/3`, `setof/3`), flags, control (`once/1`, `->/2`, `;/2`, `not/1`), plus
2P-Kt's additions, e.g. `between/3` and the predicates of custom data (`get_persistent/2`, ...).
Input and output beyond `write/1` and `nl/0` are in `tuprolog.solve.libs.io`.

Main objects and modules:

- `CommonBuiltins`: the standard library, as a `tuprolog.solve.library.Library`;
- `CommonPrimitives`, `CommonFunctions`, `CommonRules`: its parts;
- `tuprolog.solve.stdlib.primitive`, `tuprolog.solve.stdlib.function`,
  `tuprolog.solve.stdlib.rule`: its primitives, functions and rules, one by one;
- `tuprolog.solve.stdlib.magic`: the magic cut, used by its rules.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solver = prolog_solver()
    >>> solver.solve_once("findall(X, between(1, 3, X), L), atom_length(hello, N)").to_dict()
    {'L': [1, 2, 3], 'N': 5}

See Also:
    - 2P-Kt's [default predicates](https://tuprolog.github.io/2p-kt/reference/default-predicates/).
"""

from ._definitions import *

__all__ = ["CommonBuiltins", "CommonFunctions", "CommonPrimitives", "CommonRules"]
