import pytest

import tuprolog.theory as theory_module
from tuprolog.core import Clause, atom, fact, rule, struct, var
from tuprolog.theory import MutableTheory, RetractResult, Theory, mutable_theory, theory

P_A = fact(struct("p", atom("a")))
P_B = fact(struct("p", atom("b")))
Q_X = rule(struct("q", var("X")), struct("p", var("X")))


def test_definitions_are_jvm_types():
    assert Theory.class_.getName() == "it.unibo.tuprolog.theory.Theory"
    assert MutableTheory.class_.getName() == "it.unibo.tuprolog.theory.MutableTheory"
    assert RetractResult.class_.getName() == "it.unibo.tuprolog.theory.RetractResult"
    assert issubclass(MutableTheory, Theory)


def test_public_names_are_exported():
    for name in ("theory", "mutable_theory", "Theory", "MutableTheory", "RetractResult"):
        assert hasattr(theory_module, name)


@pytest.mark.parametrize("factory", [theory, mutable_theory])
def test_empty_factories(factory):
    t = factory()
    assert len(t) == 0
    assert t.is_empty
    assert not t.is_non_empty
    assert not t
    assert list(t) == []


def test_theory_is_immutable():
    t = theory(P_A)
    assert isinstance(t, Theory)
    assert not isinstance(t, MutableTheory)
    assert not t.is_mutable


def test_mutable_theory_is_mutable():
    t = mutable_theory(P_A)
    assert isinstance(t, MutableTheory)
    assert t.is_mutable


@pytest.mark.parametrize("factory", [theory, mutable_theory])
@pytest.mark.parametrize(
    "make_args",
    [
        pytest.param(lambda: (P_A, P_B, Q_X), id="varargs"),
        pytest.param(lambda: ([P_A, P_B, Q_X],), id="list"),
        pytest.param(lambda: ((P_A, P_B, Q_X),), id="tuple"),
        pytest.param(lambda: (iter([P_A, P_B, Q_X]),), id="iterator"),
        pytest.param(lambda: ((c for c in [P_A, P_B, Q_X]),), id="generator"),
    ],
)
def test_factories_accept_varargs_or_iterables(factory, make_args):
    t = factory(*make_args())
    assert len(t) == 3
    assert list(t) == [P_A, P_B, Q_X]


@pytest.mark.parametrize("factory", [theory, mutable_theory])
def test_factories_accept_a_single_clause(factory):
    t = factory(P_A)
    assert len(t) == 1
    assert list(t) == [P_A]


@pytest.mark.parametrize("factory", [theory, mutable_theory])
def test_factories_accept_another_theory(factory):
    source = theory(P_A, P_B)
    t = factory(source)
    assert len(t) == 2
    assert t == source


def test_factories_preserve_clause_order_and_duplicates():
    t = theory(P_B, P_A, P_B)
    assert list(t) == [P_B, P_A, P_B]


def test_factory_items_are_clauses():
    assert all(isinstance(c, Clause) for c in theory(P_A, Q_X))


def test_factories_reject_non_clauses():
    with pytest.raises(Exception):  # noqa: B017 - JVM-side ClassCastException
        list(theory(1, 2))


def test_mutable_theory_is_not_shared_with_its_source():
    source = theory(P_A)
    t = mutable_theory(source)
    t.assert_z(P_B)
    assert len(t) == 2
    assert len(source) == 1
