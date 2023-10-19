from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.core.operators as _operators  # type: ignore


Operator = _operators.Operator


OperatorSet = _operators.OperatorSet


Specifier = _operators.Specifier


EMPTY_OPERATORS: OperatorSet = OperatorSet.EMPTY


DEFAULT_OPERATORS: OperatorSet = OperatorSet.DEFAULT


STANDARD_OPERATORS: OperatorSet = OperatorSet.STANDARD


XF: Specifier = Specifier.XF


YF: Specifier = Specifier.YF


FX: Specifier = Specifier.FX


FY: Specifier = Specifier.FY


XFX: Specifier = Specifier.XFX


XFY: Specifier = Specifier.XFY


YFX: Specifier = Specifier.YFX


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.operators.*")
