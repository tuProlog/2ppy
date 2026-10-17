from jpype import JImplements, JOverride
from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.function as _function  # type: ignore


LogicFunction = _function.LogicFunction


Compute = _function.Compute


ArithmeticUtilsKt = _function.ArithmeticUtilsKt


ComputeRequest = Compute.Request


ComputeResponse = Compute.Request


@JImplements(LogicFunction)
class AbstractLogicFunction(object):
    @JOverride
    def compute(self, request: ComputeRequest) -> ComputeResponse:
        raise NotImplementedError()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.function.*")
