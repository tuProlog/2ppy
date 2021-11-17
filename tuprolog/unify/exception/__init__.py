from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.unify.exception as _exceptions
from ._ktadapt import *


NoUnifyException = _exceptions.NoUnifyException

OccurCheckException = _exceptions.OccurCheckException


logger.debug("Loaded JVM classes from it.unibo.tuprolog.unify.exception.*")
