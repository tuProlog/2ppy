from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.core.exception as _exceptions

TuPrologException = _exceptions.TuPrologException

SubstitutionException = _exceptions.TuPrologException

SubstitutionApplicationException = _exceptions.TuPrologException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.exception.*")
