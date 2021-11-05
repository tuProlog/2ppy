from tuprolog import logger
from ._ktadapt import *
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.utils as _utils

Taggable = _utils.Taggable

logger.debug("Loaded JVM classes from it.unibo.tuprolog.utils.*")
