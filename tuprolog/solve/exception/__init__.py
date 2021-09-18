from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.exception import HaltException
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.exception import LogicError
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.exception import ResolutionException
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.exception import TimeOutException
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.exception import Warning


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.*")
