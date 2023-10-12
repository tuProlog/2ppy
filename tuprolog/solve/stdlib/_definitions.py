from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.stdlib as _stdlib  # type: ignore


CommonBuiltins: _stdlib.CommonBuiltins = _stdlib.CommonBuiltins.INSTANCE


CommonFunctions: _stdlib.CommonFunctions = _stdlib.CommonFunctions.INSTANCE


CommonPrimitives: _stdlib.CommonPrimitives = _stdlib.CommonPrimitives.INSTANCE


CommonRules: _stdlib.CommonRules = _stdlib.CommonRules.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.*")
