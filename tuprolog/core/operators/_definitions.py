import it.unibo.tuprolog.core.operators as _operators  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "DEFAULT_OPERATORS",
    "EMPTY_OPERATORS",
    "FX",
    "FY",
    "STANDARD_OPERATORS",
    "XF",
    "XFX",
    "XFY",
    "YF",
    "YFX",
    "Operator",
    "OperatorSet",
    "Specifier",
]


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
