from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.stdlib as _stdlib  # type: ignore


CommonBuiltins = _stdlib.CommonBuiltins

CommonFunctions = _stdlib.CommonFunctions

CommonPrimitives = _stdlib.CommonPrimitives

CommonRules = _stdlib.CommonRules


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.*")
