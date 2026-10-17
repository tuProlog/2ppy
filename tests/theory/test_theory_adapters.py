import pytest

from tuprolog.core import atom, directive, fact, indicator, rule, struct, var
from tuprolog.theory import Theory, mutable_theory, theory

P_A = fact(struct("p", atom("a")))


P_B = fact(struct("p", atom("b")))


Q_X = rule(struct("q", var("X")), struct("p", var("X")))


DYN = directive(struct("dynamic", indicator("r", 1)))


Z = fact(atom("z"))


SHADOWED = (
    "the Theory customizer is registered on the interface, so concrete classes' methods "
    "shadow it (and it calls a non-existent `{}_`, JPype keeps the original as `_{}`)"
)


@pytest.fixture(params=[theory, mutable_theory], ids=["immutable", "mutable"])
def factory(request):
    return request.param


@pytest.fixture
def kb(factory):
    return factory(P_A, P_B, Q_X)


@pytest.mark.parametrize("method, expected", [("assert_a", [Z, P_A]), ("assert_z", [P_A, Z])])
def test_assert_returns_the_updated_theory(factory, method, expected):
    t = factory(P_A)
    result = getattr(t, method)(Z)
    assert isinstance(result, Theory)
    assert list(result) == expected


@pytest.mark.parametrize(
    "method, expected",
    [("assert_a", [P_B, Z, P_A]), ("assert_z", [P_A, P_B, Z])],
)
@pytest.mark.parametrize(
    "make_args",
    [
        pytest.param(lambda: (P_B, Z), id="varargs"),
        pytest.param(lambda: ([P_B, Z],), id="list"),
        pytest.param(lambda: ((c for c in [P_B, Z]),), id="generator"),
        pytest.param(lambda: (theory(P_B, Z),), id="theory"),
    ],
)
def test_assert_many_clauses(factory, method, expected, make_args):
    result = getattr(factory(P_A), method)(*make_args())
    assert list(result) == expected


@pytest.mark.parametrize("method", ["assert_a", "assert_z"])
def test_assert_struct_as_fact(factory, method):
    result = getattr(factory(), method)(struct("p", atom("a")))
    assert list(result) == [P_A]


def test_assert_leaves_immutable_theory_unchanged():
    t = theory(P_A)
    t.assert_z(Z)
    t.assert_a(Z)
    assert list(t) == [P_A]


def test_assert_changes_mutable_theory_in_place():
    t = mutable_theory(P_A)
    t.assert_z(Z)
    t.assert_a(P_B)
    assert list(t) == [P_B, P_A, Z]


TO_STRING_SHADOWED = pytest.mark.xfail(
    strict=True,
    reason="MutableTheory.to_string(True) resolves to the auto-generated java.lang.Object.to_string "
    "(Object precedes the Theory interface in MutableIndexedTheory's MRO), so the Theory "
    "customizer is shadowed",
)


FACTORIES_TO_STRING = [
    pytest.param(theory, id="immutable"),
    pytest.param(mutable_theory, id="mutable", marks=TO_STRING_SHADOWED),
]
