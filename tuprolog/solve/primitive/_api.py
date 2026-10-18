from collections.abc import Callable, Iterable, Iterator
from typing import Any

from jpype import JException, JObject

from tuprolog.core import Clause, Integer, Term, atom, struct, to_python, to_term
from tuprolog.jvmutils import jlist
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.solve import MAX_TIMEOUT, ExecutionContext, Signature, Solution, current_time_instant
from tuprolog.solve.exception import ResolutionException
from tuprolog.solve.exception.error.system import SystemError as LogicSystemError

from ._definitions import (
    AbstractPrimitive,
    Primitive,
    PrimitiveWrapper,
    SolveRequest,
    SolveResponse,
)

__all__ = [
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


def python_error(context: ExecutionContext, error: BaseException) -> ResolutionException:
    """The logic error for an exception raised by Python code run by a solver.

    Errors of 2P-Kt (`tuprolog.solve.exception.ResolutionException`s) are kept as they are; any
    other exception becomes a `system_error`, whose culprit is the JVM exception, or the term
    `python_error(Type, Message)` for Python exceptions (e.g. `python_error('ValueError', 'oops')`).
    This is how `primitive` (and so `predicate`) turns the exceptions of Python code into logic
    errors, which Prolog code can handle with `catch/3`.

    Args:
        context: the execution context in which the error occurred (e.g. `request.context`).
        error: the exception raised.

    Returns:
        The logic error to reply with (e.g. by `request.reply_exception`).

    Examples:
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.primitive import predicate
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> def fail_loudly():
        ...     raise ValueError("oops")
        >>> lib = library("demo", primitives={"oops/0": predicate(fail_loudly)})
        >>> solver = prolog_solver(libraries=lib)
        >>> solver.solve_once("catch(oops, error(E, _), true)")["E"]
        system_error
        >>> solver.solve_once("oops").get_exception().message
        "Uncaught exception `python_error('ValueError', oops)`"
    """
    if isinstance(error, ResolutionException):
        return error
    if isinstance(error, JException):
        return LogicSystemError.forUncaughtException(context, error)
    culprit = struct("python_error", atom(type(error).__name__), atom(str(error)))
    return LogicSystemError.forUncaughtException(context, culprit)


def _guarded(
    request: SolveRequest, responses: Callable[[], Iterable[SolveResponse]]
) -> Iterator[SolveResponse]:
    try:
        yield from responses()
    except Exception as error:  # noqa: BLE001  (surfaces as a logic error, for catch/3)
        yield request.reply_exception(python_error(request.context, error))


def primitive(callable: Callable[[SolveRequest], Iterable[SolveResponse]]) -> Primitive:
    """Makes a primitive from a callable mapping requests to responses.

    The callable receives each `SolveRequest` issued for the goals invoking the primitive, and
    returns (or yields, being a generator) its `SolveResponse`s, built by the `reply_*` methods of
    the request: one per solution, none if there are no solutions. Exceptions it raises (even after
    some responses) become logic errors, as `python_error` says, ending the solutions.

    Args:
        callable: the implementation, from a request to an iterable of responses.

    Returns:
        A primitive, to be registered in a library (see `tuprolog.solve.library.library`).

    Examples:
        >>> from tuprolog.core import atom
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.primitive import primitive
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> def colour(request):
        ...     [argument] = request.arguments
        ...     for name in ("red", "green"):
        ...         yield request.reply_with(request.unificator.mgu(argument, atom(name)))
        >>> lib = library("demo", primitives={"colour/1": primitive(colour)})
        >>> list(prolog_solver(libraries=lib).query("colour(C)"))
        [{'C': 'red'}, {'C': 'green'}]

    See Also:
        `predicate`, to write primitives as plain Python functions.
    """

    class CallableToPrimitiveAdapter(AbstractPrimitive):
        def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
            return _guarded(request, lambda: callable(request))

    return JObject(CallableToPrimitiveAdapter(), Primitive)


def predicate(function: Callable[..., bool | None | Iterable]) -> Primitive:
    """Makes a primitive from a Python function taking the goal's arguments as Python values.

    The arguments of the goal are converted by `tuprolog.core.to_python` (e.g. atoms become strings,
    integers ints, lists lists); unbound variables, and terms without a Python counterpart, are
    passed as they are (as `tuprolog.core.Term`s). The function then either:

    - returns a boolean: `True` (or `None`) means success, without binding any variable, and `False`
      failure;
    - returns or yields tuples of values, one per solution, as long as the goal's arguments: each
      tuple is converted by `tuprolog.core.to_term` and unified with the arguments, binding the
      goal's variables; tuples not unifying are skipped. For predicates of arity 1, plain values may
      be returned instead of 1-tuples.

    Exceptions it raises become logic errors (see `python_error`).

    Args:
        function: the implementation, called with as many arguments as the goal's arity.

    Returns:
        A primitive, to be registered in a library (see `tuprolog.solve.library.library`).

    Raises:
        ValueError: (as a logic `system_error`) if a tuple of values is not as long as the goal's
            arguments.

    Examples:
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.primitive import predicate
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> lib = library(
        ...     "demo",
        ...     primitives={
        ...         "even/1": predicate(lambda n: n % 2 == 0),
        ...         "upper/2": predicate(lambda s, _: [(s, s.upper())]),
        ...         "digit/1": predicate(lambda _: range(3)),
        ...     },
        ... )
        >>> solver = prolog_solver(libraries=lib)
        >>> solver.solve_once("even(4)").is_yes, solver.solve_once("even(3)").is_yes
        (True, False)
        >>> list(solver.query("upper(abc, U)"))
        [{'U': 'ABC'}]
        >>> list(solver.query("digit(D)"))
        [{'D': 0}, {'D': 1}, {'D': 2}]
    """

    def solve(request: SolveRequest) -> Iterable[SolveResponse]:
        arguments = list(request.arguments)
        outcome = function(*(to_python(argument) for argument in arguments))
        if outcome is None or isinstance(outcome, bool):
            yield request.reply_success() if outcome is not False else request.reply_fail()
            return
        goal = struct("goal", arguments)
        unificator = request.context.unificator
        for values in outcome:
            if len(arguments) == 1 and not isinstance(values, tuple):
                values = (values,)
            if len(values) != len(arguments):
                raise ValueError(f"Expected {len(arguments)} values, got {values!r}")
            mgu = unificator.mgu(goal, struct("goal", [to_term(v) for v in values]))
            if not mgu.isFailed():
                yield request.reply_success(mgu)

    return primitive(solve)


def solve_request(
    signature: Signature,
    arguments: Iterable[Term],
    context: ExecutionContext,
    issuing_instant: int | None = None,
    max_duration: int = MAX_TIMEOUT,
) -> SolveRequest:
    """Creates a request to prove a goal by means of a primitive.

    Solvers issue requests by themselves: build them only to call primitives directly (e.g. when
    testing them).

    Args:
        signature: the signature of the goal (see `tuprolog.solve.signature`).
        arguments: the arguments of the goal, as many as `signature`'s arity.
        context: the execution context of the request (e.g. another request's `context`).
        issuing_instant: when the request is issued, in milliseconds since the epoch; now, by
            default (see `tuprolog.solve.current_time_instant`).
        max_duration: how long (in milliseconds) the request may take; unlimited by default.

    Returns:
        The request, whose `query` is the goal.

    Examples:
        >>> from tuprolog.core import atom, var
        >>> from tuprolog.solve import signature
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.primitive import predicate, primitive, solve_request
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> contexts = []
        >>> def capture(request):
        ...     contexts.append(request.context)
        ...     yield request.reply_success()
        >>> lib = library("demo", primitives={"capture/0": primitive(capture)})
        >>> _ = prolog_solver(libraries=lib).solve_once("capture")
        >>> upper = predicate(lambda s, _: [(s, s.upper())])
        >>> request = solve_request(signature("upper", 2), [atom("abc"), var("U")], contexts[0])
        >>> request.query
        upper(abc, U_...)
        >>> [str(response.solution.substitution) for response in upper.solve(request)]
        ["{U_...='ABC'}"]
    """
    if issuing_instant is None:
        issuing_instant = current_time_instant()
    return SolveRequest(signature, jlist(arguments), context, issuing_instant, max_duration)


def solve_response(solution: Solution, *side_effects: Any) -> SolveResponse:
    """Creates a response with a solution and some side effects.

    Requests' `reply_*` methods are the handier way of building responses.

    Args:
        solution: the solution (see `tuprolog.solve.yes_solution`, `no_solution`, `halt_solution`).
        *side_effects: the side effects on the solver's state (see `tuprolog.solve.sideffects`),
            or a single iterable of them.

    Returns:
        The response.
    """
    return iterable_or_varargs(side_effects, lambda ses: SolveResponse(solution, None, jlist(ses)))


def check_term_is_recursively_callable(request: SolveRequest, term: Term) -> Any:
    """Checks whether a term can be called as a goal, its sub-goals included.

    A term is callable if it is a structure (e.g. an atom or a compound term) or a variable;
    conjunctions, disjunctions and implications (`,`, `;`, `->`) are callable if their sub-goals
    are.

    Args:
        request: the request on whose behalf the check is made (giving the error's context).
        term: the term to check.

    Returns:
        `None`, if `term` is callable, or the `type_error(callable, Culprit)` to raise otherwise
        (a `tuprolog.solve.exception.error.type.TypeError`, not raised by this function).
    """
    return PrimitiveWrapper.checkTermIsRecursivelyCallable(request, term)


def ensuring_all_arguments_are_instantiated(request: SolveRequest) -> SolveRequest:
    """Checks that no argument of a request is an unbound variable.

    Args:
        request: the request whose arguments are checked.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.instantiation.InstantiationError: `instantiation_error`, for
            the first unbound argument.
    """
    return PrimitiveWrapper.ensuringAllArgumentsAreInstantiated(request)


def ensuring_procedure_has_permission(
    request: SolveRequest, signature: Signature, operation: Any
) -> SolveRequest:
    """Checks that a procedure can be modified, i.e. that it is neither a library one nor static.

    Used by primitives altering the knowledge base (e.g. `assert/1`, `retract/1`).

    Args:
        request: the request on whose behalf the check is made.
        signature: the signature of the procedure to modify (`None` passes the check).
        operation: the attempted operation (e.g. `OPERATION_MODIFY`, see
            `tuprolog.solve.exception.error.permission`).

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.permission.PermissionError:
            `permission_error(Operation, private_procedure, Name/Arity)` if a library defines the
            procedure, or `permission_error(Operation, static_procedure, Name/Arity)` if the static
            knowledge base does.
    """
    return PrimitiveWrapper.ensuringProcedureHasPermission(request, signature, operation)


def ensuring_clause_procedure_has_permission(
    request: SolveRequest, clause: Clause, operation: Any
) -> SolveRequest:
    """Checks that the procedure of a clause (i.e. its head's) can be modified.

    As `ensuring_procedure_has_permission`, for the signature of `clause`'s head.

    Args:
        request: the request on whose behalf the check is made.
        clause: the clause whose procedure is checked.
        operation: the attempted operation (e.g. `OPERATION_MODIFY`).

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.permission.PermissionError: if the procedure is a library or
            static one.
    """
    return PrimitiveWrapper.ensuringClauseProcedureHasPermission(request, clause, operation)


def ensuring_argument_is_well_formed_indicator(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a well-formed predicate indicator.

    A predicate indicator is a `Name/Arity` term, with an atom `Name` and an integer `Arity`.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.instantiation.InstantiationError: if the argument, its name,
            or its arity are unbound.
        tuprolog.solve.exception.error.type.TypeError: `type_error(predicate_indicator, Culprit)` if
            the argument is not `_/_`, `type_error(atom, Name)` or `type_error(integer, Arity)` if
            its parts are not.
        tuprolog.solve.exception.error.domain.DomainError: `domain_error(not_less_than_zero, Arity)`
            for negative arities.
        tuprolog.solve.exception.error.representation.RepresentationError:
            `representation_error(max_arity)` if the arity exceeds the `max_arity` flag.
    """
    return PrimitiveWrapper.ensuringArgumentIsWellFormedIndicator(request, index)


def not_implemented(request: SolveRequest, message: str) -> SolveResponse:
    """Raises the error reporting that a primitive is not implemented yet.

    Args:
        request: the request answered.
        message: the error message.

    Returns:
        Never returns: it raises.

    Raises:
        tuprolog.solve.exception.error.system.SystemError: always, with `message`.
    """
    return PrimitiveWrapper.notImplemented(request, message)


def not_supported(request: SolveRequest, message: str) -> SolveResponse:
    """Raises the error reporting that a primitive does not support an operation.

    Args:
        request: the request answered.
        message: the error message.

    Returns:
        Never returns: it raises.

    Raises:
        tuprolog.solve.exception.error.system.SystemError: always, with `message`.
    """
    return PrimitiveWrapper.notSupported(request, message)


def ensuring_argument_is_well_formed_clause(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a well-formed clause.

    Well-formed clauses are callable terms, or `Head :- Body` ones with a callable head and body.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.instantiation.InstantiationError: if the argument is unbound.
        tuprolog.solve.exception.error.type.TypeError: `type_error(callable, Culprit)` if the
            argument is not a structure.
        tuprolog.solve.exception.error.domain.DomainError: `domain_error(clause, Culprit)` for
            ill-formed `:-/2` terms.
    """
    return PrimitiveWrapper.ensuringArgumentIsWellFormedClause(request, index)


def ensuring_argument_is_instantiated(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is not an unbound variable.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.instantiation.InstantiationError: `instantiation_error`, if
            the argument is unbound.
    """
    return PrimitiveWrapper.ensuringArgumentIsInstantiated(request, index)


def ensuring_argument_is_numeric(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a number (an integer or a real).

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(number, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsNumeric(request, index)


def ensuring_argument_is_struct(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a structure (an atom or a compound term).

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(callable, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsStruct(request, index)


def ensuring_argument_is_callable(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is callable, i.e. a structure.

    The same as `ensuring_argument_is_struct`.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(callable, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsCallable(request, index)


def ensuring_argument_is_variable(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is an unbound variable.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(variable, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsVariable(request, index)


def ensuring_argument_is_compound(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a compound term (not an atom).

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(compound, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsCompound(request, index)


def ensuring_argument_is_atom(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is an atom.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(atom, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsAtom(request, index)


def ensuring_argument_is_constant(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is atomic, i.e. an atom or a number.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(atomic, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsConstant(request, index)


def ensuring_argument_is_ground(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is ground (contains no unbound variable).

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.instantiation.InstantiationError: `instantiation_error`, for
            its first variable, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsGround(request, index)


def ensuring_argument_is_char(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a character, i.e. an atom of length 1.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(character, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsChar(request, index)


def ensuring_argument_is_specifier(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is an operator specifier.

    Operator specifiers are atoms such as `xfx` or `fy` (see `tuprolog.core.operators`).

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.domain.DomainError:
            `domain_error(operator_specifier, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsSpecifier(request, index)


def ensuring_argument_is_integer(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is an integer.

    Examples:
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.primitive import ensuring_argument_is_integer, primitive
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> def check(request):
        ...     yield ensuring_argument_is_integer(request, 0).reply_success()
        >>> lib = library("demo", primitives={"check/1": primitive(check)})
        >>> solver = prolog_solver(libraries=lib)
        >>> solver.solve_once("check(1)").is_yes
        True
        >>> solver.solve_once("catch(check(a), error(E, _), true)")["E"]
        type_error(integer, a)

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(integer, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsInteger(request, index)


def ensuring_argument_is_list(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a list (possibly a partial one).

    Partial lists end with a variable, e.g. `[a | T]`.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(list, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringArgumentIsList(request, index)


def ensuring_argument_is_well_formed_list(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a well-formed list (ending with `[]`).

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(list, Culprit)` if the argument
            is not a list.
        tuprolog.solve.exception.error.domain.DomainError: `domain_error(well_formed_list, Culprit)`
            for partial lists.
    """
    return PrimitiveWrapper.ensuringArgumentIsWellFormedList(request, index)


def ensuring_argument_is_arity(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a valid arity.

    Valid arities are non-negative integers not exceeding the `max_arity` flag.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(integer, Culprit)` if the
            argument is not an integer.
        tuprolog.solve.exception.error.domain.DomainError:
            `domain_error(not_less_than_zero, Culprit)` if it is negative.
        tuprolog.solve.exception.error.representation.RepresentationError:
            `representation_error(max_arity)` if it exceeds the flag.
    """
    return PrimitiveWrapper.ensuringArgumentIsArity(request, index)


def ensuring_argument_is_non_negative_integer(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a non-negative integer.

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(integer, Culprit)` if the
            argument is not an integer.
        tuprolog.solve.exception.error.domain.DomainError:
            `domain_error(not_less_than_zero, Culprit)` if it is negative.
    """
    return PrimitiveWrapper.ensuringArgumentIsNonNegativeInteger(request, index)


def is_character_code(integer: Integer) -> bool:
    """Checks whether an integer is **not** a valid character code.

    Note:
        Despite its name, this wraps 2P-Kt's `PrimitiveWrapper.isCharacterCode`, which returns
        `True` for integers *outside* the range of character codes (0 to 65535).

    Args:
        integer: the logic integer to check.

    Returns:
        `True` if `integer` is not a character code, `False` if it is one.

    Examples:
        >>> from tuprolog.core import integer
        >>> from tuprolog.solve.primitive import is_character_code
        >>> is_character_code(integer(65)), is_character_code(integer(-1))
        (False, True)
    """
    return PrimitiveWrapper.isCharacterCode(integer)


def ensuring_term_is_char_code(request: SolveRequest, term: Term) -> SolveRequest:
    """Checks that a term is a character code, i.e. an integer from 0 to 65535.

    Args:
        request: the request on whose behalf the check is made.
        term: the term to check.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.representation.RepresentationError:
            `representation_error(character_code)`, otherwise.
    """
    return PrimitiveWrapper.ensuringTermIsCharCode(request, term)


def ensuring_term_is_well_formed_list(request: SolveRequest, term: Term) -> SolveRequest:
    """Checks that a term is a well-formed list, i.e. one ending with `[]`.

    Args:
        request: the request on whose behalf the check is made.
        term: the term to check.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.domain.DomainError:
            `domain_error(well_formed_list, Culprit)`, otherwise.
    """
    return PrimitiveWrapper.ensuringTermIsWellFormedList(request, term)


def ensuring_argument_is_char_code(request: SolveRequest, index: int) -> SolveRequest:
    """Checks that the `index`-th argument of a request is a character code (0 to 65535).

    Args:
        request: the request whose argument is checked.
        index: the (0-based) position of the argument.

    Returns:
        `request` itself, if the check passes, so that checks can be chained.

    Raises:
        tuprolog.solve.exception.error.type.TypeError: `type_error(integer, Culprit)` if the
            argument is not an integer.
        tuprolog.solve.exception.error.representation.RepresentationError:
            `representation_error(character_code)` if it is out of range.
    """
    return PrimitiveWrapper.ensuringArgumentIsCharCode(request, index)
