"""Tests for `tuprolog.core.operators` (API, definitions and OperatorSet adapters)."""

import jpype
import pytest

from tuprolog.core import atom, integer, struct, var
from tuprolog.core.operators import (
    DEFAULT_OPERATORS,
    EMPTY_OPERATORS,
    FX,
    FY,
    STANDARD_OPERATORS,
    XF,
    XFX,
    XFY,
    YF,
    YFX,
    Operator,
    OperatorSet,
    Specifier,
    operator,
    operator_set,
    specifier,
)

IllegalArgumentException = jpype.JClass("java.lang.IllegalArgumentException")


@pytest.fixture
def plusplus():
    return operator("++", XFX, 500)


@pytest.fixture
def minusminus():
    return operator("--", FY, 200)


def test_definitions_are_jvm_types():
    package = "it.unibo.tuprolog.core.operators."
    assert Operator == jpype.JClass(package + "Operator")
    assert OperatorSet == jpype.JClass(package + "OperatorSet")
    assert Specifier == jpype.JClass(package + "Specifier")


def test_specifier_constants():
    assert [XF, YF, FX, FY, XFX, XFY, YFX] == [
        Specifier.XF,
        Specifier.YF,
        Specifier.FX,
        Specifier.FY,
        Specifier.XFX,
        Specifier.XFY,
        Specifier.YFX,
    ]
    assert set(Specifier.values()) == {XF, YF, FX, FY, XFX, XFY, YFX}


def test_operator_set_constants():
    assert len(EMPTY_OPERATORS) == 0
    assert EMPTY_OPERATORS == OperatorSet.EMPTY
    assert DEFAULT_OPERATORS == OperatorSet.DEFAULT
    assert STANDARD_OPERATORS == OperatorSet.STANDARD
    assert len(DEFAULT_OPERATORS) > 0


@pytest.mark.parametrize(
    "functor, spec, priority",
    [(":-", XFX, 1200), (",", XFY, 1000), ("+", YFX, 500), ("-", FY, 200), ("\\+", FY, 900)],
)
def test_default_operators_contain_iso_operators(functor, spec, priority):
    op = operator(functor, spec, priority)
    assert op in DEFAULT_OPERATORS
    found = [o for o in DEFAULT_OPERATORS if o == op]
    assert found[0].priority == priority


# --- operator -------------------------------------------------------------------------------------


def test_operator_from_python_values(plusplus):
    assert isinstance(plusplus, Operator)
    assert plusplus.functor == "++"
    assert plusplus.specifier == XFX
    assert plusplus.priority == 500


def test_operator_from_terms(plusplus):
    assert operator(integer(500), atom("xfx"), atom("++")) == plusplus
    assert operator(integer(500), atom("xfx"), atom("++")).priority == 500


def test_operator_from_struct(plusplus):
    op = operator(struct("op", integer(500), atom("xfx"), atom("++")))
    assert op == plusplus
    assert op.priority == 500


def test_operator_from_non_operator_struct_is_none():
    assert operator(struct("foo", atom("a"))) is None
    assert operator(atom("++")) is None


def test_operator_to_term_round_trip(plusplus):
    term = plusplus.to_term()
    assert term == struct("op", integer(500), atom("xfx"), atom("++"))
    assert operator(term) == plusplus


def test_operator_repr(plusplus):
    assert repr(plusplus) == "Operator(500, XFX, '++')"


def test_operator_equality_ignores_priority_but_ordering_does_not():
    low = operator("++", XFX, 100)
    high = operator("++", XFX, 200)
    assert low == high
    assert hash(low) == hash(high)
    assert low < high
    assert high > low
    assert low != operator("++", XFY, 100)
    assert low != operator("--", XFX, 100)


def test_operator_wrong_argument_types():
    with pytest.raises(TypeError):
        operator(atom("++"), atom("xfx"), integer(500))


# --- specifier ------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["xfx", "XFX", "xFx"])
def test_specifier_from_string(name):
    assert specifier(name) == XFX


@pytest.mark.parametrize("name", ["xf", "yf", "fx", "fy", "xfx", "xfy", "yfx"])
def test_specifier_from_term_round_trip(name):
    spec = specifier(atom(name))
    assert spec.to_term() == atom(name)
    assert specifier(spec.to_term()) == spec


def test_specifier_from_invalid_string():
    with pytest.raises(IllegalArgumentException):
        specifier("foo")


@pytest.mark.parametrize("term", [atom("foo"), struct("f", atom("a")), var("X"), integer(1)])
def test_specifier_from_invalid_term(term):
    with pytest.raises(IllegalArgumentException):
        specifier(term)


@pytest.mark.parametrize("value", [1, None, 1.5])
def test_specifier_from_invalid_type(value):
    with pytest.raises(TypeError):
        specifier(value)


def test_specifier_properties():
    assert XFX.is_infix and not XFX.is_prefix and not XFX.is_postfix
    assert FY.is_prefix and not FY.is_infix
    assert YF.is_postfix and not YF.is_infix


def test_specifier_ordering():
    assert sorted([YFX, XF, FX]) == [XF, FX, YFX]


# --- operator_set ---------------------------------------------------------------------------------


def test_operator_set_empty():
    assert operator_set() == EMPTY_OPERATORS


def test_operator_set_varargs(plusplus, minusminus):
    ops = operator_set(plusplus, minusminus)
    assert isinstance(ops, OperatorSet)
    assert len(ops) == 2
    assert plusplus in ops
    assert minusminus in ops
    assert set(ops) == {plusplus, minusminus}


def test_operator_set_singleton(plusplus):
    ops = operator_set(plusplus)
    assert len(ops) == 1
    assert list(ops) == [plusplus]


@pytest.mark.parametrize("collection", [list, tuple, set, iter])
def test_operator_set_single_iterable(collection, plusplus, minusminus):
    assert operator_set(collection([plusplus, minusminus])) == operator_set(plusplus, minusminus)


def test_operator_set_generator(plusplus, minusminus):
    ops = operator_set(op for op in [plusplus, minusminus])
    assert ops == operator_set(plusplus, minusminus)


def test_operator_set_from_operator_set(plusplus):
    assert operator_set(operator_set(plusplus)) == operator_set(plusplus)


def test_operator_set_add_operator(plusplus, minusminus):
    assert operator_set(plusplus) + minusminus == operator_set(plusplus, minusminus)


def test_operator_set_add_operator_set(plusplus, minusminus):
    assert operator_set(plusplus) + operator_set(minusminus) == operator_set(plusplus, minusminus)


def test_operator_set_add_overrides_priority(plusplus):
    ops = operator_set(plusplus) + operator("++", XFX, 700)
    assert len(ops) == 1
    assert next(iter(ops)).priority == 700


def test_operator_set_iadd(plusplus, minusminus):
    ops = operator_set(plusplus)
    ops += minusminus
    assert ops == operator_set(plusplus, minusminus)


def test_operator_set_sub_operator(plusplus, minusminus):
    assert operator_set(plusplus, minusminus) - minusminus == operator_set(plusplus)


def test_operator_set_sub_operator_set(plusplus, minusminus):
    assert operator_set(plusplus, minusminus) - operator_set(plusplus) == operator_set(minusminus)


def test_operator_set_sub_missing(plusplus, minusminus):
    assert operator_set(plusplus) - minusminus == operator_set(plusplus)


def test_operator_set_equality_and_hash(plusplus, minusminus):
    assert operator_set(plusplus, minusminus) == operator_set(minusminus, plusplus)
    assert hash(operator_set(plusplus, minusminus)) == hash(operator_set(minusminus, plusplus))
    assert operator_set(plusplus) != operator_set(minusminus)


def test_operator_set_does_not_mutate(plusplus, minusminus):
    ops = operator_set(plusplus)
    _ = ops + minusminus
    assert ops == operator_set(plusplus)
