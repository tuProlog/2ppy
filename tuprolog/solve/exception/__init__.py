from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.exception as _exceptions  # type: ignore

HaltException = _exceptions.HaltException

LogicError = _exceptions.LogicError

ResolutionException = _exceptions.ResolutionException

TimeOutException = _exceptions.TimeOutException

Warning = _exceptions.Warning


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.*")
