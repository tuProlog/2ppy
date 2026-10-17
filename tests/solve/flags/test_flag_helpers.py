"""The `flag()` and `flag_store()` helpers."""

import pytest
from jpype import JException

from tuprolog.core import Term, atom, integer
from tuprolog.solve.flags import (
    Flag,
    MaxArity,
    Unknown,
    flag,
)


def as_tuple(f) -> tuple[str, str]:
    return str(f.first), str(f.second)


def test_flag_from_notable_flag_takes_its_default():
    assert as_tuple(flag(Unknown)) == ("unknown", "warning")


def test_flag_from_notable_flag_and_value():
    f = flag(Unknown, Unknown.FAIL)
    assert isinstance(f, Flag)
    assert as_tuple(f) == ("unknown", "fail")


def test_flag_from_notable_flag_rejects_inadmissible_values():
    with pytest.raises(JException):
        flag(Unknown, atom("bad"))


def test_flag_from_name_and_value():
    f = flag("custom", atom("v"))
    assert isinstance(f, Flag)
    assert as_tuple(f) == ("custom", "v")


def test_flag_from_jvm_string_name():
    assert as_tuple(flag(Unknown.name, Unknown.FAIL)) == ("unknown", "fail")


def test_flag_from_name_requires_value():
    with pytest.raises(ValueError):
        flag("custom")


@pytest.mark.parametrize(
    "pair",
    [("custom", atom("v")), ["custom", atom("v")], iter(["custom", atom("v")])],
    ids=["tuple", "list", "iterator"],
)
def test_flag_from_pair(pair):
    assert as_tuple(flag(pair)) == ("custom", "v")


def test_flag_from_flag_is_identity():
    f = flag("custom", atom("v"))
    assert flag(f) is f


@pytest.mark.parametrize(
    "wrong",
    [
        (),
        ("custom",),
        ("custom", atom("v"), atom("w")),
        (Unknown, MaxArity),
        (1, atom("v")),
        [atom("custom"), atom("v")],
    ],
    ids=["empty", "one", "three", "notables", "int-name", "term-name"],
)
def test_flag_rejects_malformed_pairs(wrong):
    with pytest.raises(ValueError):
        flag(wrong)


@pytest.mark.parametrize("wrong", [1, None, atom("a")])
def test_flag_rejects_other_types(wrong):
    with pytest.raises(ValueError):
        flag(wrong)


def test_flag_rejects_pair_and_value():
    with pytest.raises(ValueError):
        flag(("custom", atom("v")), atom("w"))


@pytest.mark.xfail(
    strict=True,
    reason="flag() does not convert Python values into terms: flag('a', 1) holds a JVM Long",
)
def test_flag_converts_python_values_to_terms():
    assert isinstance(flag("custom", 1).second, Term)
    assert flag("custom", 1).second == integer(1)
