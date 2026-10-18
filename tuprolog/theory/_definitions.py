import it.unibo.tuprolog.theory as _theory  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["MutableTheory", "RetractResult", "Theory"]


Theory = _theory.Theory

MutableTheory = _theory.MutableTheory

RetractResult = _theory.RetractResult

logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.*")
