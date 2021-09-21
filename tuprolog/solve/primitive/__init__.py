from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.primitive import Primitive
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.primitive import Solve

# noinspection PyUnresolvedReferences
from tuprolog.core import Term
# noinspection PyUnresolvedReferences
from tuprolog.solve import ExecutionContext, Signature, Solution, current_time_instant, MAX_TIME_DURATION
# noinspection PyUnresolvedReferences
from tuprolog.solve.sideffcts import SideEffect
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jlist

from typing import List, Iterable


SolveRequest = Solve.Request

SolveResponse = Solve.Request


@jpype.JImplements(Primitive)
class AbstractPrimitive(object):
    @jpype.JOverride
    def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
        raise NotImplementedError()


def solve_request(
        signature: Signature,
        arguments: List[Term],
        context: ExecutionContext,
        issuing_instant: int = current_time_instant(),
        max_duration: int = MAX_TIME_DURATION
) -> SolveRequest:
    return SolveRequest(signature, arguments, context, issuing_instant, max_duration)


def solve_response(solution: Solution, *side_effects: SideEffect) -> SolveResponse:
    return iterable_or_varargs(side_effects, lambda ses: SolveResponse(solution, None, jlist(ses)))


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.primitive.*")
