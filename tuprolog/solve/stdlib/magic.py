import it.unibo.tuprolog.solve.stdlib.magic as _magic  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["MagicCut"]


MagicCut: _magic.MagicCut = _magic.MagicCut.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.magic.*")
