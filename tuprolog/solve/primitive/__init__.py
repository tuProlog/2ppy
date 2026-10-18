"""Primitives: predicates implemented in Python (or Kotlin) rather than in Prolog.

A logic solver proves a goal such as `upper(abc, U)` by looking for clauses whose head matches it.
Some predicates cannot be (conveniently) written as clauses, e.g. those doing arithmetic, I/O, or
calling external code: they are implemented as **primitives**, i.e. functions the solver calls
whenever a goal invokes them.

A primitive receives a **solve request** (`SolveRequest`) describing the goal being proven: its
`signature` (name and arity, e.g. `upper/2`), its `arguments` (terms, possibly containing unbound
variables), and the **execution context** (`tuprolog.solve.ExecutionContext`) of the solver at
that moment (its knowledge base, flags, operators, libraries, I/O channels...). It replies with
zero or more **solve responses** (`SolveResponse`), one per solution, lazily: each response
carries a solution (success with a substitution binding the goal's variables, failure, or an
error), and optionally side effects on the solver's state (see `tuprolog.solve.sideffects`).
Replying with no response at all, or with a failure, means the goal has no (more) solutions.

Primitives are packed into libraries (see `tuprolog.solve.library`), which are then given to
solvers. The easiest way to write one is `predicate`, turning a plain Python function into a
primitive; `primitive` gives full control over requests and responses. The `ensuring_*` functions
check the arguments of a request, raising the standard ISO Prolog error (see
`tuprolog.solve.exception.error`) when they are not as expected.

Examples:
    A predicate from a Python function, yielding one tuple of argument values per solution:

    >>> from tuprolog.solve.library import library
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> between = predicate(lambda low, high, x: ((low, high, i) for i in range(low, high + 1)))
    >>> solver = prolog_solver(libraries=library("demo", primitives={"between/3": between}))
    >>> list(solver.query("between(1, 3, X)"))
    [{'X': 1}, {'X': 2}, {'X': 3}]

    A primitive handling the request directly, checking its first argument:

    >>> from tuprolog.core import integer
    >>> def double(request):
    ...     ensuring_argument_is_integer(request, 0)
    ...     n, result = request.arguments
    ...     doubled = integer(n.to_int() * 2)
    ...     yield request.reply_with(request.context.unificator.mgu(result, doubled))
    >>> lib = library("demo", primitives={"double/2": primitive(double)})
    >>> solver = prolog_solver(libraries=lib)
    >>> list(solver.query("double(21, X)"))
    [{'X': 42}]
    >>> solver.solve_once("catch(double(a, X), error(E, _), true)")["E"]
    type_error(integer, a)

See Also:
    `tuprolog.solve.function`, for Python-defined arithmetic functions;
    `tuprolog.solve.library`, to bundle primitives into libraries;
    2P-Kt's documentation on
    [primitives](https://tuprolog.github.io/2p-kt/reference/primitives-and-functions/).
"""

import tuprolog.solve.primitive._adapters as _

from ._api import *
from ._definitions import *

__all__ = [
    "AbstractPrimitive",
    "Primitive",
    "PrimitiveWrapper",
    "Solve",
    "SolveRequest",
    "SolveResponse",
    "check_term_is_recursively_callable",
    "ensuring_all_arguments_are_instantiated",
    "ensuring_argument_is_arity",
    "ensuring_argument_is_atom",
    "ensuring_argument_is_callable",
    "ensuring_argument_is_char",
    "ensuring_argument_is_char_code",
    "ensuring_argument_is_compound",
    "ensuring_argument_is_constant",
    "ensuring_argument_is_ground",
    "ensuring_argument_is_instantiated",
    "ensuring_argument_is_integer",
    "ensuring_argument_is_list",
    "ensuring_argument_is_non_negative_integer",
    "ensuring_argument_is_numeric",
    "ensuring_argument_is_specifier",
    "ensuring_argument_is_struct",
    "ensuring_argument_is_variable",
    "ensuring_argument_is_well_formed_clause",
    "ensuring_argument_is_well_formed_indicator",
    "ensuring_argument_is_well_formed_list",
    "ensuring_clause_procedure_has_permission",
    "ensuring_procedure_has_permission",
    "ensuring_term_is_char_code",
    "ensuring_term_is_well_formed_list",
    "is_character_code",
    "not_implemented",
    "not_supported",
    "predicate",
    "primitive",
    "python_error",
    "solve_request",
    "solve_response",
]
