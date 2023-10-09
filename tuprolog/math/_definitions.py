import jpype.imports
import org.gciatto.kt.math as _ktmath # type: ignore
import java.lang as _java_lang # type: ignore


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
