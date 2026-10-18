from collections.abc import Iterable

import it.unibo.tuprolog.solve.primitive as _primitive  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JOverride

from tuprolog import logger
from tuprolog.jvmutils import jimplements

__all__ = [
    "AbstractPrimitive",
    "Primitive",
    "PrimitiveWrapper",
    "Solve",
    "SolveRequest",
    "SolveResponse",
]


Primitive = _primitive.Primitive
"""A predicate implemented by code: a function from a `SolveRequest` to responses.

The JVM interface every primitive implements: its single method, `solve(request)`, returns the
(lazy) sequence of `SolveResponse`s answering the request, one per solution. Primitives are
registered in libraries under a signature (see `tuprolog.solve.library.library`).

Build primitives with `primitive` (from a callable handling requests) or `predicate` (from a plain
Python function), or by subclassing `AbstractPrimitive`; `Primitive.of(callable)` is 2P-Kt's own
factory, and `Primitive.enforcingSignature(signature, primitive)` restricts a primitive to one
signature.
"""


Solve = _primitive.Solve
"""The base type of `SolveRequest` (`Solve.Request`) and `SolveResponse` (`Solve.Response`)."""


PrimitiveWrapper = _primitive.PrimitiveWrapper
"""2P-Kt's base class of the primitives it implements, wrapping a function under a signature.

Its static methods back the argument checks of this package (e.g. `ensuring_argument_is_atom`
calls `PrimitiveWrapper.ensuringArgumentIsAtom`); `PrimitiveWrapper.wrap(signature, primitive)`
builds a wrapper from a signature and a `Primitive`, and `wrapper.implementation` (also
`wrapper.signature`, `wrapper.description_pair`) gives back the checked primitive.
"""


SolveRequest = Solve.Request
"""A request, issued by a solver, to prove a goal by means of a primitive.

Members (snake_case aliases as well):

- `signature`: the `tuprolog.solve.Signature` (name and arity) of the goal, e.g. `upper/2`;
- `arguments`: the goal's arguments (a JVM list of `tuprolog.core.Term`s, possibly containing
  unbound variables), indexable and iterable;
- `query`: the goal itself, as a `tuprolog.core.Struct` (e.g. `upper(abc, U)`);
- `context`: the solver's `tuprolog.solve.ExecutionContext` when the request was issued (its
  knowledge bases, flags, operators, libraries, channels, and `unificator`);
- `start_time` and `max_duration`: when the request was issued, and how long (in milliseconds)
  it may take before timing out;
- `unificator`: the context's unification algorithm (see `tuprolog.unify`), e.g.
  `request.unificator.mgu(a, b)` gives the substitution unifying `a` and `b`.

Reply to it with responses built by its methods, each optionally taking side effects
(`tuprolog.solve.sideffects`) as further arguments:

- `reply_with(outcome)`: a success or a failure from a substitution (failed substitutions mean
  failure), a `tuprolog.solve.Solution`, or a boolean;
- `reply_success(substitution=None)`: a success, binding the goal's variables as `substitution`
  says (nothing, by default);
- `reply_fail()`: a failure;
- `reply_exception(exception)`: an error, i.e. a `tuprolog.solve.exception.ResolutionException`
  (raising it from the primitive has the same effect).

`solve(goal, max_duration=None)` proves another goal in a sub-solver sharing this request's
context (by default within the time left to this request), giving back its solutions.

Build requests (e.g. for testing primitives) with `solve_request`.

Examples:
    >>> from tuprolog.solve.library import library
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> from tuprolog.solve.primitive import primitive
    >>> requests = []
    >>> def spy(request):
    ...     requests.append(request)
    ...     yield request.reply_success()
    >>> solver = prolog_solver(libraries=library("spy", primitives={"spy/2": primitive(spy)}))
    >>> solver.solve_once("spy(a, f(X))").is_yes
    True
    >>> request = requests[0]
    >>> request.signature.name, request.signature.arity
    ('spy', 2)
    >>> [str(argument) for argument in request.arguments]
    ['a', 'f(X_...)']
    >>> request.reply_fail().solution.is_no
    True
"""


SolveResponse = Solve.Response
"""A response to a `SolveRequest`: one solution of the goal, plus side effects.

Members (snake_case aliases as well): `solution`, the `tuprolog.solve.Solution` (a success
with its substitution, a failure, or an error); `side_effects`, the (possibly empty) list of
`tuprolog.solve.sideffects.SideEffect`s to apply to the solver's state (e.g. asserting clauses,
setting flags); `side_effect_manager`, solver-specific state for control-flow primitives (`None`
unless changed).

Build responses with the `reply_*` methods of requests, or with `solve_response`.
"""


@jimplements(Primitive)
class AbstractPrimitive:
    """A base class for primitives implemented in Python, as subclasses overriding `solve`.

    Instances implement the JVM interface `Primitive`; `primitive` is the shortcut building one
    from a callable, also turning the Python exceptions `solve` raises into logic errors.

    Examples:
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> from tuprolog.solve.primitive import AbstractPrimitive
        >>> class Hello(AbstractPrimitive):
        ...     def solve(self, request):
        ...         yield request.reply_success()
        >>> hello = Hello()
        >>> solver = prolog_solver(libraries=library("demo", primitives={"hello/0": hello}))
        >>> solver.solve_once("hello").is_yes
        True
    """

    @JOverride
    def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
        """Answers a request with its responses, one per solution (lazily, e.g. as a generator).

        Args:
            request: the request to prove a goal invoking this primitive.

        Returns:
            The responses to `request`; none, or a failure, if the goal has no (more) solutions.

        Raises:
            NotImplementedError: unless overridden.
        """
        raise NotImplementedError()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.primitive.*")
