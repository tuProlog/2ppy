from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib import CommonBuiltins
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib import CommonFunctions
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib import CommonPrimitives
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib import CommonRules


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.*")
