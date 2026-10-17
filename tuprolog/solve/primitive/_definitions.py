from collections.abc import Iterable

import it.unibo.tuprolog.solve.primitive as _primitive  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JImplements, JOverride

from tuprolog import logger

Primitive = _primitive.Primitive


Solve = _primitive.Solve


PrimitiveWrapper = _primitive.PrimitiveWrapper


SolveRequest = Solve.Request


SolveResponse = Solve.Response


@JImplements(Primitive)
class AbstractPrimitive:
    @JOverride
    def solve(self, request: SolveRequest) -> Iterable[SolveResponse]:
        raise NotImplementedError()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.primitive.*")
