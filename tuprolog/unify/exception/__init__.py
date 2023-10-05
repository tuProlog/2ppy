from tuprolog import logger
import jpype.imports
import it.unibo.tuprolog.unify.exception as _exceptions # type: ignore


NoUnifyException = _exceptions.NoUnifyException

OccurCheckException = _exceptions.OccurCheckException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.unify.exception.*")
