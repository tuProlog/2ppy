import it.unibo.tuprolog.unify.exception as _exceptions  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["NoUnifyException", "OccurCheckException"]


NoUnifyException = _exceptions.NoUnifyException

OccurCheckException = _exceptions.OccurCheckException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.unify.exception.*")
