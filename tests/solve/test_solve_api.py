

import pytest

from tuprolog.core import (
    atom,
    indicator,
    integer,
    struct,
    var,
)
from tuprolog.core.parsing import parse_struct
from tuprolog.solve import (
    Signature,
    signature,
)
from tuprolog.solve.prolog import prolog_solver


@pytest.fixture(scope="module")
def resolution_error():
    halt = prolog_solver().solve_once(parse_struct("X is foo + 1"))
    return halt.getException()


def test_signature_from_name_and_arity():
    sig = signature("f", 2)
    assert isinstance(sig, Signature)
    assert sig.name == "f"
    assert sig.arity == 2
    assert sig.vararg is False


def test_signature_vararg():
    assert signature("f", 2, True).vararg is True
    assert signature("f", 2, vararg=True) == signature("f", 2, True)


def test_signature_keyword_arity():
    assert signature("f", arity=1) == signature("f", 1)


@pytest.mark.xfail(
    strict=True,
    reason="signature (like yes/no/halt_solution) is a functools.singledispatch function, "
    "which requires the first argument to be positional",
)
def test_signature_all_keyword_arguments():
    assert signature(name="f", arity=1) == signature("f", 1)


def test_signature_equality_and_hash():
    assert signature("f", 2) == signature("f", 2)
    assert signature("f", 2) != signature("f", 3)
    assert signature("f", 2) != signature("f", 2, True)
    assert hash(signature("f", 2)) == hash(signature("f", 2))
    assert {signature("f", 2): 1}[signature("f", 2)] == 1


def test_signature_from_indicator():
    assert signature(indicator("f", 2)) == signature("f", 2)


def test_signature_from_signature_term():
    assert signature(struct("/", atom("f"), integer(2))) == signature("f", 2)


def test_signature_from_vararg_signature_term():
    term = struct("/", atom("f"), struct("+", integer(2), atom("vararg")))
    assert signature(term) == signature("f", 2, True)


@pytest.mark.parametrize(
    "term",
    [
        pytest.param(atom("f"), id="atom"),
        pytest.param(integer(2), id="number"),
        pytest.param(indicator(var("X"), integer(2)), id="non-ground-indicator"),
    ],
)
def test_signature_from_invalid_terms_is_none(term):
    assert signature(term) is None


def test_signature_round_trips():
    sig = signature("f", 2)
    assert sig.to_indicator() == indicator("f", 2)
    assert signature(sig.to_indicator()) == sig
    assert signature(sig.to_term()) == sig
    vararg = signature("f", 2, True)
    assert signature(vararg.to_term()) == vararg


def test_signature_with_args():
    assert signature("f", 2).with_args([atom("a"), atom("b")]) == struct("f", atom("a"), atom("b"))


def test_signature_str():
    assert str(signature("f", 2)) == "Signature(name=f, arity=2, vararg=false)"


@pytest.fixture(scope="module")
def solver():
    from tuprolog.theory.parsing import parse_theory

    return prolog_solver(static_kb=parse_theory("p(1). p(2). q(a + b)."))


