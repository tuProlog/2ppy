import it.unibo.tuprolog.core.exception as _exceptions  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["SubstitutionApplicationException", "SubstitutionException", "TuPrologException"]


TuPrologException = _exceptions.TuPrologException

SubstitutionException = _exceptions.SubstitutionException

SubstitutionApplicationException = _exceptions.SubstitutionApplicationException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.exception.*")
