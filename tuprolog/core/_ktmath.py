# noinspection PyUnresolvedReferences
from typing import Union
import decimal
import jpype.imports
# noinspection PyUnresolvedReferences
import org.gciatto.kt.math as _ktmath
# noinspection PyUnresolvedReferences
import java.lang as _java_lang

BigInteger = _ktmath.BigInteger

BigDecimal = _ktmath.BigDecimal

MathContext = _ktmath.MathContext

RoundingMode = _ktmath.RoundingMode

_MAX_LONG = _java_lang.Long.MAX_VALUE


def big_integer(value: Union[str, int], radix: int = None) -> BigInteger:
    if radix is not None:
        assert isinstance(value, str)
        return BigInteger.of(value, radix)
    if isinstance(value, str):
        return BigInteger.of(jpype.JString @ value)
    assert isinstance(value, int)
    if value > _MAX_LONG:
        return BigInteger.of(jpype.JString @ str(value))
    return BigInteger.of(jpype.JInt @ value)


def jvm_rounding_mode(mode):
    if mode == decimal.ROUND_DOWN:
        return RoundingMode.DOWN
    elif mode == decimal.ROUND_UP:
        return RoundingMode.UP
    elif mode == decimal.ROUND_FLOOR:
        return RoundingMode.FLOOR
    elif mode == decimal.ROUND_CEILING:
        return RoundingMode.CEILING
    elif mode == decimal.ROUND_HALF_UP:
        return RoundingMode.HALF_UP
    elif mode == decimal.ROUND_HALF_EVEN:
        return RoundingMode.HALF_EVEN
    elif mode == decimal.ROUND_HALF_DOWN:
        return RoundingMode.HALF_DOWN
    elif mode == decimal.ROUND_05UP:
        raise ValueError(f"Rounding mode {decimal.ROUND_05UP} has no Java correspondence")
    else:
        raise ValueError(f"Not a rounding mode {mode}")


def big_decimal(value: Union[str, int, float, decimal.Decimal], precision=None, rounding=None) -> BigDecimal:
    if precision is None:
        precision = decimal.getcontext().prec
    assert isinstance(precision, int)
    if rounding is None:
        rounding = jvm_rounding_mode(decimal.getcontext().rounding)
    elif rounding in decimal:
        rounding = jvm_rounding_mode(rounding)
    assert isinstance(rounding, RoundingMode)
    context = MathContext(precision, rounding)
    if isinstance(value, decimal.Decimal):
        return BigDecimal.of(jpype.JString @ str(value), context)
    if isinstance(value, BigInteger):
        return BigDecimal.of(value, context)
    if isinstance(value, int):
        return BigDecimal.of(big_integer(value), context)
    assert isinstance(value, float)
    return BigDecimal.of(jpype.JDouble @ value, context)
