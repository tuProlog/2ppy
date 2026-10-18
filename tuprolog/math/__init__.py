"""Arbitrary-precision numbers, as used by numeric terms.

Logic numbers never overflow nor lose digits: `tuprolog.core.Integer` terms hold a `BigInteger`,
and `tuprolog.core.Real` terms a `BigDecimal` (a decimal number, not a binary floating-point one).
This package exposes these JVM types, with `MathContext` and `RoundingMode` (the settings of
decimal arithmetic) and some constants, and converts them from and to Python numbers:
`big_integer` and `python_integer` (for `int`s), `big_decimal` and `python_decimal` (for `float`s
and `decimal.Decimal`s), `jvm_rounding_mode` (for the rounding modes of Python's `decimal`).

Examples:
    >>> from tuprolog.math import big_decimal, big_integer, python_decimal, python_integer
    >>> python_integer(big_integer(2**100)) == 2**100
    True
    >>> python_decimal(big_decimal("0.1"))
    Decimal('0.1')

See Also:
    `tuprolog.core.integer` and `tuprolog.core.real`, building numeric terms.
"""

from ._api import *
from ._definitions import *

__all__ = [
    "BIG_DECIMAL_E",
    "BIG_DECIMAL_ONE",
    "BIG_DECIMAL_ONE_HALF",
    "BIG_DECIMAL_ONE_TENTH",
    "BIG_DECIMAL_PI",
    "BIG_DECIMAL_ZERO",
    "BIG_INTEGER_MAX_LONG",
    "BIG_INTEGER_MIN_LONG",
    "BIG_INTEGER_NEGATIVE_ONE",
    "BIG_INTEGER_ONE",
    "BIG_INTEGER_TEN",
    "BIG_INTEGER_TWO",
    "BIG_INTEGER_ZERO",
    "BigDecimal",
    "BigInteger",
    "MathContext",
    "RoundingMode",
    "big_decimal",
    "big_integer",
    "jvm_rounding_mode",
    "python_decimal",
    "python_integer",
]
