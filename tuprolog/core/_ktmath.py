# noinspection PyUnresolvedReferences
from typing import Union
import decimal
import jpype.imports
# noinspection PyUnresolvedReferences
import org.gciatto.kt.math as _ktmath
# noinspection PyUnresolvedReferences
import java.lang as _java_lang
from math import ceil

from tuprolog.pyutils import and_then

BigInteger = _ktmath.BigInteger

BigDecimal = _ktmath.BigDecimal

MathContext = _ktmath.MathContext

RoundingMode = _ktmath.RoundingMode

_MAX_LONG = _java_lang.Long.MAX_VALUE

_MIN_LONG = _java_lang.Long.MIN_VALUE

BIG_INTEGER_MAX_LONG = BigInteger.of(_MAX_LONG)

BIG_INTEGER_MIN_LONG = BigInteger.of(_MIN_LONG)

BIG_INTEGER_ZERO = BigInteger.ZERO

BIG_INTEGER_TEN = BigInteger.TEN

BIG_INTEGER_ONE = BigInteger.ONE

BIG_INTEGER_NEGATIVE_ONE = BigInteger.NEGATIVE_ONE

BIG_INTEGER_TWO = BigInteger.TWO

BIG_DECIMAL_ZERO = BigDecimal.ZERO

BIG_DECIMAL_ONE = BigDecimal.ONE

BIG_DECIMAL_ONE_HALF = BigDecimal.ONE_HALF

BIG_DECIMAL_ONE_TENTH = BigDecimal.ONE_TENTH

BIG_DECIMAL_E = BigDecimal.E

BIG_DECIMAL_PI = BigDecimal.PI


def _int_to_bytes(n: int) -> bytes:
    try:
        size = n.bit_length() // 8 + 1
        return n.to_bytes(size, 'big', signed=True)
    except OverflowError as e:
        e.args = ["%s: %d, whose size is %d" % (e.args[0], n, size)]
        raise e


def big_integer(value: Union[str, int], radix: int = None) -> BigInteger:
    if radix is not None:
        assert isinstance(value, str)
        return BigInteger.of(value, radix)
    if isinstance(value, str):
        return BigInteger.of(jpype.JString @ value)
    assert isinstance(value, int)
    bs = _int_to_bytes(value)
    return BigInteger(jpype.JArray(jpype.JByte) @ bs, 0, len(bs))


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
        return BigDecimal.of(jpype.JString @ str(value), context)
    if isinstance(value, BigInteger):
        return BigDecimal.of(value, context)
    if isinstance(value, int):
        return BigDecimal.of(big_integer(value), context)
    assert isinstance(value, float)
    return BigDecimal.of(jpype.JDouble @ value, context)


def python_decimal(value: BigDecimal) -> decimal.Decimal:
    return decimal.Decimal(str(value))
