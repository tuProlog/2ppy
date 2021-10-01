from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.stdlib as _stdlib


CommonBuiltins = _stdlib.CommonBuiltins

CommonFunctions = _stdlib.CommonFunctions

CommonPrimitives = _stdlib.CommonPrimitives

CommonRules = _stdlib.CommonRules


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.*")
