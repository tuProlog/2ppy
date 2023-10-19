from typing import Iterable
from jpype import JImplements, JOverride
from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.primitive as _primitive  # type: ignore


Primitive = _primitive.Primitive


Solve = _primitive.Solve


PrimitiveWrapper = _primitive.PrimitiveWrapper


SolveRequest = Solve.Request


SolveResponse = Solve.Response


@JImplements(Primitive)
class AbstractPrimitive(object):
    @JOverride
    def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
        raise NotImplementedError()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.primitive.*")
