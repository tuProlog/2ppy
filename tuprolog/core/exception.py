from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.core.exception as _exceptions  # type: ignore

TuPrologException = _exceptions.TuPrologException

SubstitutionException = _exceptions.SubstitutionException

SubstitutionApplicationException = _exceptions.SubstitutionApplicationException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.exception.*")
