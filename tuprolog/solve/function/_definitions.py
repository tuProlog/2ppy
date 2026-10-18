import it.unibo.tuprolog.solve.function as _function  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JImplements, JOverride

from tuprolog import logger

__all__ = [
    "AbstractLogicFunction",
    "ArithmeticUtilsKt",
    "Compute",
    "ComputeRequest",
    "ComputeResponse",
    "LogicFunction",
]


LogicFunction = _function.LogicFunction


Compute = _function.Compute


ArithmeticUtilsKt = _function.ArithmeticUtilsKt


ComputeRequest = Compute.Request


ComputeResponse = Compute.Response


@JImplements(LogicFunction)
class AbstractLogicFunction:
    @JOverride
    def compute(self, request: ComputeRequest) -> ComputeResponse:
        raise NotImplementedError()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.function.*")
