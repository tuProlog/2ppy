import re
from collections.abc import Sized

import pytest

from tuprolog.core import atom, directive, fact, indicator, rule, struct, var
from tuprolog.theory import MutableTheory, RetractResult, Theory, mutable_theory, theory

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


def test_theory_is_sized(kb):
    assert isinstance(kb, Sized)
    assert len(kb) == 3
    assert kb.size == 3


def test_iteration_yields_clauses_in_order(kb):
    assert list(kb) == [P_A, P_B, Q_X]
    assert list(kb) == list(kb)  # re-iterable


def test_truthiness_follows_size(factory):
    assert not factory()
    assert factory(P_A)


@pytest.mark.parametrize(
    "item, expected",
    [
        pytest.param(P_A, True, id="clause"),
        pytest.param(Z, False, id="missing-clause"),
        pytest.param(struct("p", atom("a")), True, id="head"),
        pytest.param(struct("p", atom("c")), False, id="missing-head"),
        pytest.param(indicator("p", 1), True, id="indicator"),
        pytest.param(indicator("q", 1), True, id="rule-indicator"),
        pytest.param(indicator("p", 2), False, id="missing-indicator"),
    ],
)
def test_contains(kb, item, expected):
    assert (item in kb) is expected


def test_contains_rejects_non_terms(kb):
    with pytest.raises(TypeError):
        assert 1 in kb


def test_getitem_by_clause_unifies(kb):
    assert list(kb[fact(struct("p", var("Y")))]) == [P_A, P_B]
    assert list(kb[fact(struct("p", atom("b")))]) == [P_B]
    assert list(kb[Z]) == []


def test_getitem_by_head(kb):
    assert list(kb[struct("q", atom("a"))]) == [Q_X]
    assert list(kb[struct("r", atom("a"))]) == []


def test_getitem_by_indicator(kb):
    assert list(kb[indicator("p", 1)]) == [P_A, P_B]
    assert list(kb[indicator("z", 0)]) == []


def test_getitem_rejects_python_values(kb):
    with pytest.raises(TypeError):
        kb["p"]


def test_add_clause(factory):
    t = factory(P_A) + P_B
    assert list(t) == [P_A, P_B]


def test_add_theory(factory):
    t = factory(P_A) + theory(P_B, Q_X)
    assert list(t) == [P_A, P_B, Q_X]


def test_add_does_not_change_immutable_operands():
    left, right = theory(P_A), theory(P_B)
    result = left + right
    assert len(result) == 2
    assert len(left) == 1
    assert len(right) == 1


def test_add_changes_mutable_theory_in_place():
    t = mutable_theory(P_A)
    t + P_B
    assert len(t) == 2


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


def test_retract_single_clause(kb):
    result = kb.retract(P_A)
    assert isinstance(result, RetractResult)
    assert result.is_success
    assert not result.is_failure
    assert list(result.clauses) == [P_A]
    assert result.first_clause == P_A
    assert list(result.theory) == [P_B, Q_X]


def test_retract_by_head(kb):
    result = kb.retract(struct("p", var("_")))
    assert result.is_success
    assert result.first_clause == P_A


def test_retract_missing_clause_fails(kb):
    result = kb.retract(Z)
    assert result.is_failure
    assert result.clauses is None
    assert result.first_clause is None
    assert len(result.theory) == 3


def test_retract_leaves_immutable_theory_unchanged():
    t = theory(P_A, P_B)
    t.retract(P_A)
    assert len(t) == 2


def test_retract_changes_mutable_theory_in_place():
    t = mutable_theory(P_A, P_B)
    t.retract(P_A)
    assert list(t) == [P_B]


@pytest.mark.xfail(strict=True, reason=SHADOWED.format("retract", "retract"))
def test_retract_varargs(kb):
    result = kb.retract(P_A, P_B)
    assert list(result.clauses) == [P_A, P_B]
    assert list(result.theory) == [Q_X]


@pytest.mark.xfail(
    strict=True,
    reason="retract(list) is ambiguous between Iterable and Sequence overloads, as the "
    "Theory.retract customizer is shadowed by concrete classes",
)
def test_retract_iterable(kb):
    result = kb.retract([P_A, P_B])
    assert list(result.theory) == [Q_X]


def test_retract_all(kb):
    result = kb.retract_all(fact(struct("p", var("_"))))
    assert result.is_success
    assert list(result.clauses) == [P_A, P_B]
    assert list(result.theory) == [Q_X]


def test_retract_all_by_head(kb):
    result = kb.retract_all(struct("p", var("_")))
    assert list(result.theory) == [Q_X]


def test_retract_all_missing(kb):
    assert kb.retract_all(Z).is_failure


def test_abolish_by_indicator(kb):
    assert list(kb.abolish(indicator("p", 1))) == [Q_X]


def test_abolish_missing_indicator_is_noop(kb):
    assert len(kb.abolish(indicator("p", 7))) == 3


@pytest.mark.xfail(strict=True, reason=SHADOWED.format("abolish", "abolish"))
def test_abolish_by_name_and_arity(kb):
    assert list(kb.abolish("p", 1)) == [Q_X]


@pytest.mark.xfail(strict=True, reason=SHADOWED.format("abolish", "abolish"))
def test_abolish_by_indicator_keyword(kb):
    assert list(kb.abolish(indicator=indicator("p", 1))) == [Q_X]


def test_abolish_without_arguments_raises_value_error(kb):
    with pytest.raises(ValueError):
        kb.abolish(None)


def test_equality(factory):
    assert factory(P_A, P_B) == theory(P_A, P_B)
    assert factory(P_A, P_B) == mutable_theory(P_A, P_B)
    assert factory(P_A, P_B) != theory(P_B, P_A)
    assert factory(P_A) != theory(P_A, P_B)
    assert factory(P_A) != P_A
    assert factory() != 0


def test_equality_compares_complete_variable_names():
    one = theory(fact(struct("f", var("X"))))
    other = theory(fact(struct("f", var("X"))))
    assert one != other
    assert one.equals(other, True) is False
    assert one.equals(other, False) is True


@pytest.mark.xfail(strict=True, reason=SHADOWED.format("equals", "equals"))
def test_equals_with_keyword_argument():
    one = theory(fact(struct("f", var("X"))))
    other = theory(fact(struct("f", var("X"))))
    assert one.equals(other, use_var_complete_name=False) is True


def test_theories_are_hashable():
    assert hash(theory(P_A, P_B)) == hash(theory(P_A, P_B))
    assert len({theory(P_A), theory(P_A), theory(P_B)}) == 2


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


def test_to_string_default(kb):
    assert re.fullmatch(
        r"(Mutable)?IndexedTheory\{ p\(a\) :- true\. p\(b\) :- true\. q\(X_\d+\) :- p\(X_\d+\) \}",
        str(kb),
    )


@pytest.mark.parametrize("factory", FACTORIES_TO_STRING)
def test_to_string(factory):
    kb = factory(P_A, P_B)
    assert kb.to_string() == str(kb)
    assert kb.to_string(False) == str(kb)


@pytest.mark.parametrize("factory", FACTORIES_TO_STRING)
def test_to_string_as_prolog_text(factory):
    assert factory(P_A, P_B).to_string(True) == "p(a) :- true.\np(b) :- true.\n"


@pytest.mark.parametrize("factory", FACTORIES_TO_STRING)
def test_to_string_as_prolog_text_is_parsable(factory):
    from tuprolog.theory.parsing import parse_theory

    kb = factory(P_A, P_B, Q_X)
    assert len(parse_theory(kb.to_string(True))) == 3


def test_conversions(factory):
    t = factory(P_A)
    assert isinstance(t.to_mutable_theory(), MutableTheory)
    assert not isinstance(t.to_immutable_theory(), MutableTheory)
    assert t.to_immutable_theory() == t
    assert t.clone() == t


def test_mutable_clone_is_independent():
    t = mutable_theory(P_A)
    c = t.clone()
    c.assert_z(Z)
    assert len(t) == 1
    assert len(c) == 2


def test_mutable_theory_clauses_is_iterable():
    assert list(mutable_theory(P_A, Q_X, DYN).clauses) == [P_A, Q_X, DYN]


@pytest.mark.xfail(
    strict=True,
    reason="IndexedTheory.clauses/rules/directives return anonymous Kotlin Iterables "
    "that are not Python-iterable (README 'known issues'; needs protect_iterable)",
)
@pytest.mark.parametrize(
    "prop, expected",
    [("clauses", [P_A, Q_X, DYN]), ("rules", [P_A, Q_X]), ("directives", [DYN])],
)
def test_theory_clause_views_are_iterable(prop, expected):
    assert list(getattr(theory(P_A, Q_X, DYN), prop)) == expected


def test_tags_and_unificator(kb):
    assert len(kb.tags) == 0
    assert kb.unificator is not None
