from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.theory as _theory  # type: ignore

Theory = _theory.Theory

MutableTheory = _theory.MutableTheory

RetractResult = _theory.RetractResult

logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.*")
