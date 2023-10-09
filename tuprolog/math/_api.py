from typing import Union
import decimal
from tuprolog.pyutils import and_then
from ._definitions import BigInteger, BigDecimal, MathContext, RoundingMode
from jpype import JDouble, JString


def big_integer(value: Union[str, int], radix: int = None) -> BigInteger:
    if radix is not None:
        assert isinstance(value, str)
        return BigInteger.of(value, radix)
    if isinstance(value, str):
        return BigInteger.of(JString @ value)
    assert isinstance(value, int)
    return BigInteger.of(str(value))


def python_integer(value: BigInteger) -> int:
    return int.from_bytes(value.toByteArray(), byteorder='big', signed=True)


_python_rounding_modes = {decimal.ROUND_DOWN, decimal.ROUND_HALF_UP, decimal.ROUND_HALF_EVEN, decimal.ROUND_CEILING,
                          decimal.ROUND_FLOOR, decimal.ROUND_UP, decimal.ROUND_HALF_DOWN, decimal.ROUND_05UP}


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


@and_then(lambda bd: bd.stripTrailingZeros())
def big_decimal(value: Union[str, int, float, decimal.Decimal], precision=0,
                rounding=RoundingMode.HALF_UP) -> BigDecimal:
    if precision is None:
        precision = decimal.getcontext().prec
    assert isinstance(precision, int)
    if rounding is None:
        rounding = jvm_rounding_mode(decimal.getcontext().rounding)
    elif rounding in _python_rounding_modes:
        rounding = jvm_rounding_mode(rounding)
    assert isinstance(rounding, RoundingMode)
    context = MathContext(precision, rounding)
    if isinstance(value, str):
        return BigDecimal.of(value, context)
    if isinstance(value, decimal.Decimal):
        return BigDecimal.of(JString @ str(value), context)
    if isinstance(value, BigInteger):
        return BigDecimal.of(value, context)
    if isinstance(value, int):
        return BigDecimal.of(big_integer(value), context)
    assert isinstance(value, float)
    return BigDecimal.of(JDouble @ value, context)


def python_decimal(value: BigDecimal) -> decimal.Decimal:
    return decimal.Decimal(str(value))
