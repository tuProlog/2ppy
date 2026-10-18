import it.unibo.tuprolog.solve.stdlib as _stdlib  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["CommonBuiltins", "CommonFunctions", "CommonPrimitives", "CommonRules"]


CommonBuiltins: _stdlib.CommonBuiltins = _stdlib.CommonBuiltins.INSTANCE


CommonFunctions: _stdlib.CommonFunctions = _stdlib.CommonFunctions.INSTANCE


CommonPrimitives: _stdlib.CommonPrimitives = _stdlib.CommonPrimitives.INSTANCE


CommonRules: _stdlib.CommonRules = _stdlib.CommonRules.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.*")
