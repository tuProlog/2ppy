"""Tests for `tuprolog.math`, complementing `test_kt_math.py`."""

import decimal
from decimal import Decimal

import jpype
import pytest

from tuprolog.math import (
    BIG_DECIMAL_E,
    BIG_DECIMAL_PI,
    BIG_INTEGER_MAX_LONG,
    BIG_INTEGER_MIN_LONG,
    BigDecimal,
    BigInteger,
    MathContext,
    RoundingMode,
    big_decimal,
    big_integer,
    jvm_rounding_mode,
    python_decimal,
    python_integer,
)


def test_definitions_are_jvm_types():
    for name, jvm_type in [
        ("BigInteger", BigInteger),
        ("BigDecimal", BigDecimal),
        ("MathContext", MathContext),
        ("RoundingMode", RoundingMode),
    ]:
        assert jvm_type == jpype.JClass("org.gciatto.kt.math." + name)


def test_long_bounds():
    assert python_integer(BIG_INTEGER_MAX_LONG) == 2**63 - 1
    assert python_integer(BIG_INTEGER_MIN_LONG) == -(2**63)


def test_e_and_pi():
    assert str(python_decimal(BIG_DECIMAL_E)).startswith("2.718281828459045")
    assert str(python_decimal(BIG_DECIMAL_PI)).startswith("3.141592653589793")


# --- big_integer ----------------------------------------------------------------------------------


@pytest.mark.parametrize("value", [0, 1, -1, 2**63 - 1, 2**63, -(2**63), -(2**63) - 1, 10**50])
def test_big_integer_round_trip(value):
    assert python_integer(big_integer(value)) == value
    assert python_integer(big_integer(str(value))) == value


@pytest.mark.parametrize(
    "text, radix, value", [("ff", 16, 255), ("-ff", 16, -255), ("101", 2, 5), ("z", 36, 35)]
)
def test_big_integer_with_radix(text, radix, value):
    assert python_integer(big_integer(text, radix)) == value


def test_big_integer_from_big_integer():
    original = big_integer(42)
    assert big_integer(original) == original


@pytest.mark.parametrize("value, expected", [(True, 1), (False, 0)])
def test_big_integer_from_bool(value, expected):
    assert big_integer(value) == big_integer(expected)


@pytest.mark.parametrize("value", [1.5, None, [1], Decimal(1)])
def test_big_integer_rejects_invalid_types(value):
    with pytest.raises(TypeError):
        big_integer(value)


def test_big_integer_radix_requires_string():
    with pytest.raises(TypeError):
        big_integer(16, 16)


@pytest.mark.parametrize("text", ["zz", "1.5", ""])
def test_big_integer_rejects_malformed_strings(text):
    with pytest.raises(Exception, match="NumberFormatException"):
        big_integer(text)


def test_big_integer_comparison():
    assert big_integer(1) < big_integer(2)
    assert big_integer(2) > big_integer(1)
    assert big_integer(2) <= big_integer(2)
    assert big_integer(2) >= big_integer(2)
    assert big_integer(2) == big_integer("2")
    assert hash(big_integer(2)) == hash(big_integer("2"))


# --- python_integer / python_decimal --------------------------------------------------------------


def test_python_integer_type():
    assert type(python_integer(big_integer(3))) is int


def test_python_decimal_type():
    assert type(python_decimal(big_decimal("1.5"))) is Decimal
    assert python_decimal(big_decimal("1.5")) == Decimal("1.5")


# --- jvm_rounding_mode ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "python_mode, jvm_mode",
    [
        (decimal.ROUND_DOWN, "DOWN"),
        (decimal.ROUND_UP, "UP"),
        (decimal.ROUND_FLOOR, "FLOOR"),
        (decimal.ROUND_CEILING, "CEILING"),
        (decimal.ROUND_HALF_UP, "HALF_UP"),
        (decimal.ROUND_HALF_EVEN, "HALF_EVEN"),
        (decimal.ROUND_HALF_DOWN, "HALF_DOWN"),
    ],
)
def test_jvm_rounding_mode(python_mode, jvm_mode):
    assert jvm_rounding_mode(python_mode) == getattr(RoundingMode, jvm_mode)


def test_jvm_rounding_mode_05up_is_unsupported():
    with pytest.raises(ValueError, match="no Java correspondence"):
        jvm_rounding_mode(decimal.ROUND_05UP)


@pytest.mark.parametrize("mode", ["ROUND_WHATEVER", None, 1])
def test_jvm_rounding_mode_invalid(mode):
    with pytest.raises(ValueError, match="Not a rounding mode"):
        jvm_rounding_mode(mode)


# --- big_decimal ----------------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["1.5", 1.5, Decimal("1.5")])
def test_big_decimal_from_python_values(value):
    assert python_decimal(big_decimal(value)) == Decimal("1.5")


@pytest.mark.parametrize("value", [10, big_integer(10), "10", 10.0, Decimal(10)])
def test_big_decimal_from_integral_values(value):
    result = big_decimal(value)
    assert python_decimal(result) == 10
    assert str(result) == "10"


@pytest.mark.parametrize("value", ["100", "1E+2", 100.0, Decimal("1E+2"), 100])
def test_big_decimal_has_no_negative_scale(value):
    result = big_decimal(value)
    assert result.getScale() >= 0
    assert str(result) == "100"


def test_big_decimal_strips_trailing_zeros():
    assert str(big_decimal("1.500")) == "1.5"


def test_big_decimal_from_float_is_exact():
    assert python_decimal(big_decimal(0.1)) == Decimal(0.1)  # noqa: RUF032


@pytest.mark.parametrize(
    "rounding, expected",
    [
        (RoundingMode.HALF_UP, "1.24"),
        (RoundingMode.DOWN, "1.23"),
        (decimal.ROUND_CEILING, "1.24"),
        (decimal.ROUND_FLOOR, "1.23"),
    ],
)
def test_big_decimal_with_precision_and_rounding(rounding, expected):
    assert str(big_decimal("1.235", precision=3, rounding=rounding)) == expected


def test_big_decimal_precision_from_python_context():
    with decimal.localcontext() as context:
        context.prec = 5
        assert str(big_decimal("1.23456789", precision=None)) == "1.2346"


def test_big_decimal_rounding_from_python_context():
    with decimal.localcontext() as context:
        context.rounding = decimal.ROUND_DOWN
        assert str(big_decimal("1.29", precision=2, rounding=None)) == "1.2"


def test_big_decimal_rounding_05up_is_unsupported():
    with pytest.raises(ValueError):
        big_decimal("1.5", precision=1, rounding=decimal.ROUND_05UP)


@pytest.mark.parametrize("value", [None, [1.5], object()])
def test_big_decimal_rejects_invalid_values(value):
    with pytest.raises(TypeError):
        big_decimal(value)


def test_big_decimal_rejects_invalid_precision():
    with pytest.raises(TypeError):
        big_decimal("1", precision="3")


def test_big_decimal_rejects_invalid_rounding():
    with pytest.raises(TypeError):
        big_decimal("1", rounding="not a rounding mode")


def test_big_decimal_rejects_malformed_strings():
    with pytest.raises(Exception, match="NumberFormatException"):
        big_decimal("abc")


def test_big_decimal_comparison():
    assert big_decimal("1.5") < big_decimal("2")
    assert big_decimal("2") > big_decimal("1.5")
    assert big_decimal("1.50") == big_decimal("1.5")
