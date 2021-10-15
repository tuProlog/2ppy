# noinspection PyUnresolvedReferences
from typing import Union

import jpype.imports
# noinspection PyUnresolvedReferences
import org.gciatto.kt.math as _ktmath


BigInteger = _ktmath.BigInteger

BigDecimal = _ktmath.BigDecimal

MathContext = _ktmath.MathContext

RoundingMode = _ktmath.RoundingMode


def big_integer(value: Union[str, int], radix: int = None) -> BigInteger:
    if radix is not None:
        assert isinstance(value, str)
        return BigInteger.Companion.of(value, radix)
    if isinstance(value, str):
        return BigInteger.Companion.of(jpype.JString@value)
    return BigInteger.Companion.of(jpype.JLong@value)


def big_decimal(value) -> BigDecimal:
    return BigDecimal.Companion.of(value)
