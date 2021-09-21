from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.function import LogicFunction
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.function import Compute

# noinspection PyUnresolvedReferences
from tuprolog.core import Term
# noinspection PyUnresolvedReferences
from tuprolog.solve import ExecutionContext, Signature, current_time_instant, MAX_TIME_DURATION

from typing import List


ComputeRequest = Compute.Request

ComputeResponse = Compute.Request


@jpype.JImplements(LogicFunction)
class AbstractLogicFunction(object):
    @jpype.JOverride
    def compute(self, request: ComputeRequest) -> ComputeResponse:
        raise NotImplementedError()


def compute_request(
        signature: Signature,
        arguments: List[Term],
        context: ExecutionContext,
        issuing_instant: int = current_time_instant,
        max_duration: int = MAX_TIME_DURATION
) -> ComputeRequest:
    return ComputeRequest(signature, arguments, context, issuing_instant, max_duration)


def compute_response(result: Term) -> ComputeResponse:
    return ComputeResponse(result)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.function.*")
