from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.stdlib.magic as _magic  # type: ignore


MagicCut : _magic.MagicCut = _magic.MagicCut.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.magic.*")
