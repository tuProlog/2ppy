import java.lang as _java_lang  # type: ignore
import jpype.imports  # noqa: F401
import org.gciatto.kt.math as _ktmath  # type: ignore

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
]


BigInteger = _ktmath.BigInteger
"""An immutable integer of arbitrary precision, as used by `tuprolog.core.Integer` terms.

Build them with `big_integer` (and convert them back with `python_integer`), or `BigInteger.of`.
Members include arithmetic (`plus`, `minus`, `times`, `div`, `rem`, `pow`, ...),
comparison (`compareTo`), and `toString(radix)`.

Examples:
    >>> from tuprolog.math import big_decimal, big_integer
    >>> big_integer(6).times(big_integer(7))
    42

Note:
    The JVM class `org.gciatto.kt.math.BigInteger`, a multi-platform port of Java's
    `java.math.BigInteger`.
"""


BigDecimal = _ktmath.BigDecimal
"""An immutable decimal number of arbitrary precision, as used by `tuprolog.core.Real` terms.

Build them with `big_decimal` (and convert them back with `python_decimal`), or `BigDecimal.of`.
Members include arithmetic (`plus`, `minus`, `times`, `div`, ..., optionally taking a
`MathContext`), comparison (`compareTo`), `getScale()`, `getPrecision()`, and
`stripTrailingZeros()`.

Examples:
    >>> from tuprolog.math import big_decimal, big_integer
    >>> big_decimal("2.5").plus(big_decimal("1.25"))
    3.75

Note:
    The JVM class `org.gciatto.kt.math.BigDecimal`, a multi-platform port of Java's
    `java.math.BigDecimal`.
"""


MathContext = _ktmath.MathContext
"""The settings of arithmetic on `BigDecimal`s: a precision (the number of significant digits, 0 for
unlimited) and a `RoundingMode`, as `MathContext(precision, rounding_mode)`.

The constants `MathContext.UNLIMITED`, `DECIMAL32`, `DECIMAL64` and `DECIMAL128` give common
settings.

Examples:
    >>> from tuprolog.math import big_decimal, big_integer
    >>> big_decimal(1).div(big_decimal(3), MathContext(5, RoundingMode.HALF_UP))
    0.33333

Note:
    The JVM class `org.gciatto.kt.math.MathContext`, a port of Java's `java.math.MathContext`.
"""


RoundingMode = _ktmath.RoundingMode
"""How to round decimal numbers when digits must be discarded, an enumeration: `UP`, `DOWN`,
`CEILING`, `FLOOR`, `HALF_UP`, `HALF_DOWN`, `HALF_EVEN`, `UNNECESSARY` (raising an error when
rounding is needed).

`jvm_rounding_mode` converts the rounding modes of Python's `decimal` module into these.

Note:
    The JVM class `org.gciatto.kt.math.RoundingMode`, a port of Java's `java.math.RoundingMode`.
"""


_MAX_LONG = _java_lang.Long.MAX_VALUE


_MIN_LONG = _java_lang.Long.MIN_VALUE


BIG_INTEGER_MAX_LONG = BigInteger.of(_MAX_LONG)
"""The largest 64-bit signed integer, 2^63 - 1, as a `BigInteger`."""


BIG_INTEGER_MIN_LONG = BigInteger.of(_MIN_LONG)
"""The smallest 64-bit signed integer, -2^63, as a `BigInteger`."""


BIG_INTEGER_ZERO = BigInteger.ZERO
"""The integer 0, as a `BigInteger`."""


BIG_INTEGER_TEN = BigInteger.TEN
"""The integer 10, as a `BigInteger`."""


BIG_INTEGER_ONE = BigInteger.ONE
"""The integer 1, as a `BigInteger`."""


BIG_INTEGER_NEGATIVE_ONE = BigInteger.NEGATIVE_ONE
"""The integer -1, as a `BigInteger`."""


BIG_INTEGER_TWO = BigInteger.TWO
"""The integer 2, as a `BigInteger`."""


BIG_DECIMAL_ZERO = BigDecimal.ZERO
"""The number 0, as a `BigDecimal`."""


BIG_DECIMAL_ONE = BigDecimal.ONE
"""The number 1, as a `BigDecimal`."""


BIG_DECIMAL_ONE_HALF = BigDecimal.ONE_HALF
"""The number 0.5, as a `BigDecimal`."""


BIG_DECIMAL_ONE_TENTH = BigDecimal.ONE_TENTH
"""The number 0.1, as a `BigDecimal`."""


BIG_DECIMAL_E = BigDecimal.E
"""Euler's number e (2.71828...), as a `BigDecimal` with many digits."""


BIG_DECIMAL_PI = BigDecimal.PI
"""The number pi (3.14159...), as a `BigDecimal` with many digits."""
