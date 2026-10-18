import decimal

from jpype import JDouble, JString

from tuprolog.pyutils import and_then

from ._definitions import BigDecimal, BigInteger, MathContext, RoundingMode

__all__ = ["big_decimal", "big_integer", "jvm_rounding_mode", "python_decimal", "python_integer"]


def big_integer(value: str | int | BigInteger, radix: int | None = None) -> BigInteger:
    """Converts a Python integer, or a string of digits, into a `BigInteger`.

    Args:
        value: the value: an `int` (booleans count as 0 and 1), a string of digits (in base 10, or
            with a prefix such as `0x`, unless `radix` is given), or a `BigInteger` (returned as it
            is).
        radix: the base of the digits in `value`, which must be a string then. If `None`, base 10.

    Returns:
        The `BigInteger`.

    Raises:
        TypeError: if `value` has another type (e.g. a `float`), or `radix` is given with a
            non-string `value`.

    Examples:
        >>> big_integer(42), big_integer("-123456789012345678901234567890"), big_integer("ff", 16)
        (42, -123456789012345678901234567890, 255)
    """
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
    """Converts a `BigInteger` into a Python `int`, without loss of precision.

    Args:
        value: the `BigInteger`.

    Returns:
        The `int`.

    Examples:
        >>> python_integer(big_integer(2**70)) == 2**70
        True
    """
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


def jvm_rounding_mode(mode: str) -> RoundingMode:
    """Converts a rounding mode of Python's `decimal` module into a `RoundingMode`.

    Args:
        mode: one of `decimal.ROUND_UP`, `ROUND_DOWN`, `ROUND_CEILING`, `ROUND_FLOOR`,
            `ROUND_HALF_UP`, `ROUND_HALF_DOWN`, `ROUND_HALF_EVEN`.

    Returns:
        The corresponding `RoundingMode`.

    Raises:
        ValueError: if `mode` is `decimal.ROUND_05UP` (which has no JVM counterpart), or is not a
            rounding mode.

    Examples:
        >>> import decimal
        >>> jvm_rounding_mode(decimal.ROUND_HALF_EVEN)
        HALF_EVEN
    """
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
    value: str | float | decimal.Decimal,
    precision: int | None = 0,
    rounding: RoundingMode = RoundingMode.HALF_UP,
) -> BigDecimal:
    """Converts a Python number, or a string, into a `BigDecimal`.

    Trailing zeros are dropped (e.g. `"1.50"` gives `1.5`, and `"1E+2"` gives `100`).

    Args:
        value: the value: a string (e.g. `"3.14"`, `"1e-3"`), a `float` (converted exactly, with all
            the digits of its binary value, unless `precision` limits them), a `decimal.Decimal`, an
            `int`, or a `BigInteger`.
        precision: the number of significant digits to keep: 0 for all of them (the default), or
            `None` for the precision of the current `decimal` context.
        rounding: how to round when digits are discarded, as a `RoundingMode` or a rounding mode of
            Python's `decimal` module (e.g. `decimal.ROUND_HALF_EVEN`); `None` for the rounding of
            the current `decimal` context.

    Returns:
        The `BigDecimal`.

    Raises:
        TypeError: if `value`, `precision`, or `rounding` have another type.
        ValueError: if `rounding` is a Python rounding mode with no JVM counterpart.

    Examples:
        >>> big_decimal("1.50"), big_decimal(0.1, precision=3), big_decimal("1E+2")
        (1.5, 0.1, 100)
        >>> big_decimal(0.1)
        0.1000000000000000055511151231257827021181583404541015625
        >>> import decimal
        >>> big_decimal("2.5", precision=1), big_decimal("2.5", 1, decimal.ROUND_HALF_EVEN)
        (3, 2)
    """
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
    """Converts a `BigDecimal` into a `decimal.Decimal`, without loss of precision.

    Args:
        value: the `BigDecimal`.

    Returns:
        The `decimal.Decimal`.

    Examples:
        >>> python_decimal(big_decimal("3.14"))
        Decimal('3.14')
    """
    return decimal.Decimal(str(value))
