from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
from tuprolog.core import Term, Clause, Integer
from tuprolog.solve import ExecutionContext, Signature, Solution, current_time_instant, MAX_TIMEOUT
# from tuprolog.solve.sideffcts import SideEffect
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jlist
from typing import List, Iterable, Callable
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.primitive as _primitive


Primitive = _primitive.Primitive

Solve = _primitive.Solve

PrimitiveWrapper = _primitive.PrimitiveWrapper

SolveRequest = Solve.Request

SolveResponse = Solve.Request


@jpype.JImplements(Primitive)
class AbstractPrimitive(object):
    @jpype.JOverride
    def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
        raise NotImplementedError()


def primitive(callable: Callable[[SolveResponse], Iterable[SolveResponse]]) -> Primitive:
    class CallableToPrimitiveAdapter(AbstractPrimitive):
        def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
            return callable(request)

    return CallableToPrimitiveAdapter()


def solve_request(
        signature: Signature,
        arguments: List[Term],
        context: ExecutionContext,
        issuing_instant: int = current_time_instant(),
        max_duration: int = MAX_TIMEOUT
) -> SolveRequest:
    return SolveRequest(signature, arguments, context, issuing_instant, max_duration)


def solve_response(solution: Solution, *side_effects) -> SolveResponse:
    return iterable_or_varargs(side_effects, lambda ses: SolveResponse(solution, None, jlist(ses)))


def check_term_is_recursively_callable(request: SolveRequest, term: Term):
    return PrimitiveWrapper.checkTermIsRecursivelyCallable(request, term)


def ensuring_all_arguments_are_instantiated(request: SolveRequest) -> SolveRequest:
    return PrimitiveWrapper.ensuringAllArgumentsAreInstantiated(request)


def ensuring_procedure_has_permission(request: SolveRequest, signature: Signature, operation) -> SolveRequest:
    return PrimitiveWrapper.ensuringProcedureHasPermission(request, signature, operation)


def ensuring_clause_procedure_has_permission(request: SolveRequest, clause: Clause, operation) -> SolveRequest:
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
    return PrimitiveWrapper.ensuringArgumentIsCompound(request, index)


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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.primitive.*")
