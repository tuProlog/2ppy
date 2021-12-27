from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception as _exceptions
from ._ktadapt import *

HaltException = _exceptions.HaltException

LogicError = _exceptions.LogicError

ResolutionException = _exceptions.ResolutionException

TimeOutException = _exceptions.TimeOutException

Warning = _exceptions.Warning


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.*")
