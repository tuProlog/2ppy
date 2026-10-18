import decimal

from jpype import JDouble, JString

from tuprolog.pyutils import and_then

from ._definitions import BigDecimal, BigInteger, MathContext, RoundingMode

__all__ = ["big_decimal", "big_integer", "jvm_rounding_mode", "python_decimal", "python_integer"]


def big_integer(value: str | int | BigInteger, radix: int | None = None) -> BigInteger:
    if radix is not None:
        if not isinstance(value, str):
            raise TypeError(f"A radix can only be used with strings, not {type(value)}")
        return BigInteger.of(value, radix)
    if isinstance(value, BigInteger):
        return value
    if isinstance(value, str):
        return BigInteger.of(JString @ value)
    if not isinstance(value, int):
        raise TypeError(f"Cannot convert {type(value)} into BigInteger")
    return BigInteger.of(str(int(value)))  # int() turns bools into 0/1


def python_integer(value: BigInteger) -> int:
    return int.from_bytes(value.toByteArray(), byteorder="big", signed=True)


_python_rounding_modes = {
    decimal.ROUND_DOWN,
    decimal.ROUND_HALF_UP,
    decimal.ROUND_HALF_EVEN,
    decimal.ROUND_CEILING,
    decimal.ROUND_FLOOR,
    decimal.ROUND_UP,
    decimal.ROUND_HALF_DOWN,
    decimal.ROUND_05UP,
}


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


def _normalize(value: BigDecimal) -> BigDecimal:
    value = value.stripTrailingZeros()
    # a negative scale (e.g. 1E+2) makes 2P-Kt format reals as unparsable text (e.g. 1E+2.0)
    return value.setScale(0) if value.getScale() < 0 else value


@and_then(_normalize)
def big_decimal(
    value: str | float | decimal.Decimal, precision=0, rounding=RoundingMode.HALF_UP
) -> BigDecimal:
    if precision is None:
        precision = decimal.getcontext().prec
    if not isinstance(precision, int):
        raise TypeError(f"Invalid precision: {precision!r}")
    if rounding is None:
        rounding = jvm_rounding_mode(decimal.getcontext().rounding)
    elif rounding in _python_rounding_modes:
        rounding = jvm_rounding_mode(rounding)
    if not isinstance(rounding, RoundingMode):
        raise TypeError(f"Invalid rounding mode: {rounding!r}")
    context = MathContext(precision, rounding)
    if isinstance(value, str):
        return BigDecimal.of(value, context)
    if isinstance(value, decimal.Decimal):
        return BigDecimal.of(JString @ str(value), context)
    if isinstance(value, BigInteger):
        return BigDecimal.of(value, context)
    if isinstance(value, int):
        return BigDecimal.of(big_integer(value), context)
    if not isinstance(value, float):
        raise TypeError(f"Cannot convert {type(value)} into BigDecimal")
    return BigDecimal.of(JDouble @ value, context)


def python_decimal(value: BigDecimal) -> decimal.Decimal:
    return decimal.Decimal(str(value))
