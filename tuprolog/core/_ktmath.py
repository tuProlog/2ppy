# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import org.gciatto.kt.math as _ktmath


BigInteger = _ktmath.BigInteger

BigDecimal = _ktmath.BigDecimal

MathContext = _ktmath.MathContext

RoundingMode = _ktmath.RoundingMode


def big_integer(value) -> BigInteger:
    return BigInteger.Companion.of(value)


def big_decimal(value) -> BigDecimal:
    return BigDecimal.Companion.of(value)
