from collections.abc import Callable, Iterable

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
    """The logic error for an exception raised by Python code run by a solver: 2P-Kt's exceptions
    are kept, any other one becomes a `system_error` (the JVM exception or a
    `python_error(Type, Message)` term being its culprit)."""
    if isinstance(error, ResolutionException):
        return error
    if isinstance(error, JException):
        return LogicSystemError.forUncaughtException(context, error)
    culprit = struct("python_error", atom(type(error).__name__), atom(str(error)))
    return LogicSystemError.forUncaughtException(context, culprit)


def _guarded(request: SolveRequest, responses: Callable[[], Iterable[SolveResponse]]):
    try:
        yield from responses()
    except Exception as error:  # noqa: BLE001  (surfaces as a logic error, for catch/3)
        yield request.reply_exception(python_error(request.context, error))


def primitive(callable: Callable[[SolveRequest], Iterable[SolveResponse]]) -> Primitive:
    """A primitive from a callable mapping requests to responses.

    Exceptions it raises become logic errors (see `python_error`)."""

    class CallableToPrimitiveAdapter(AbstractPrimitive):
        def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
            return _guarded(request, lambda: callable(request))

    return JObject(CallableToPrimitiveAdapter(), Primitive)


def predicate(function: Callable[..., bool | None | Iterable]) -> Primitive:
    """A primitive from a Python function taking the goal's arguments as Python values
    (see `tuprolog.core.to_python`, unbound variables are passed as they are).

    The function either returns a boolean (`None` meaning success), or returns or yields
    tuples of values (any value, if the predicate has arity 1): each tuple unifying with the
    goal's arguments is a solution, binding the goal's variables.
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
    if issuing_instant is None:
        issuing_instant = current_time_instant()
    return SolveRequest(signature, jlist(arguments), context, issuing_instant, max_duration)


def solve_response(solution: Solution, *side_effects) -> SolveResponse:
    return iterable_or_varargs(side_effects, lambda ses: SolveResponse(solution, None, jlist(ses)))


def check_term_is_recursively_callable(request: SolveRequest, term: Term):
    return PrimitiveWrapper.checkTermIsRecursivelyCallable(request, term)


def ensuring_all_arguments_are_instantiated(request: SolveRequest) -> SolveRequest:
    return PrimitiveWrapper.ensuringAllArgumentsAreInstantiated(request)


def ensuring_procedure_has_permission(
    request: SolveRequest, signature: Signature, operation
) -> SolveRequest:
    return PrimitiveWrapper.ensuringProcedureHasPermission(request, signature, operation)


def ensuring_clause_procedure_has_permission(
    request: SolveRequest, clause: Clause, operation
) -> SolveRequest:
    return PrimitiveWrapper.ensuringClauseProcedureHasPermission(request, clause, operation)


def ensuring_argument_is_well_formed_indicator(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsWellFormedIndicator(request, index)


def not_implemented(request: SolveRequest, message: str) -> SolveResponse:
    return PrimitiveWrapper.notImplemented(request, message)


def not_supported(request: SolveRequest, message: str) -> SolveResponse:
    return PrimitiveWrapper.notSupported(request, message)


def ensuring_argument_is_well_formed_clause(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsWellFormedClause(request, index)


def ensuring_argument_is_instantiated(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsInstantiated(request, index)


def ensuring_argument_is_numeric(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsNumeric(request, index)


def ensuring_argument_is_struct(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsStruct(request, index)


def ensuring_argument_is_callable(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsCallable(request, index)


def ensuring_argument_is_variable(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsVariable(request, index)


def ensuring_argument_is_compound(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsCompound(request, index)


def ensuring_argument_is_atom(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsAtom(request, index)


def ensuring_argument_is_constant(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsConstant(request, index)


def ensuring_argument_is_ground(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsGround(request, index)


def ensuring_argument_is_char(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsChar(request, index)


def ensuring_argument_is_specifier(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsSpecifier(request, index)


def ensuring_argument_is_integer(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsInteger(request, index)


def ensuring_argument_is_list(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsList(request, index)


def ensuring_argument_is_well_formed_list(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsWellFormedList(request, index)


def ensuring_argument_is_arity(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsArity(request, index)


def ensuring_argument_is_non_negative_integer(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsNonNegativeInteger(request, index)


def is_character_code(integer: Integer) -> bool:
    return PrimitiveWrapper.isCharacterCode(integer)


def ensuring_term_is_char_code(request: SolveRequest, term: Term) -> SolveRequest:
    return PrimitiveWrapper.ensuringTermIsCharCode(request, term)


def ensuring_term_is_well_formed_list(request: SolveRequest, term: Term) -> SolveRequest:
    return PrimitiveWrapper.ensuringTermIsWellFormedList(request, term)


def ensuring_argument_is_char_code(request: SolveRequest, index: int) -> SolveRequest:
    return PrimitiveWrapper.ensuringArgumentIsCharCode(request, index)
