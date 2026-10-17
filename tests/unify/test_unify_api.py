"""Tests for `tuprolog.unify` (API, definitions and exceptions)."""

import jpype
import pytest

from tuprolog.core import (
    Substitution,
    atom,
    integer,
    logic_list,
    struct,
    substitution,
    var,
)
from tuprolog.core.exception import TuPrologException
from tuprolog.unify import (
    DEFAULT_UNIFICATOR,
    Unificator,
    cached_unificator,
    match,
    mgu,
    naive_unificator,
    strict_unificator,
    unificator,
    unify,
)
from tuprolog.unify.exception import NoUnifyException, OccurCheckException


@pytest.fixture
def X():
    return var("X")


@pytest.fixture
def Y():
    return var("Y")


@pytest.fixture
def a():
    return atom("a")


@pytest.fixture
def b():
    return atom("b")


def test_definitions():
    assert Unificator == jpype.JClass("it.unibo.tuprolog.unify.Unificator")
    assert isinstance(DEFAULT_UNIFICATOR, Unificator)
    assert Unificator.DEFAULT_CACHE_CAPACITY > 0


# --- mgu ------------------------------------------------------------------------------------------


def test_mgu_success(a, X, Y):
    b = atom("b")
    result = mgu(struct("f", X, b), struct("f", a, Y))
    assert isinstance(result, Substitution.Unifier)
    assert result == substitution({X: a, Y: b})


def test_mgu_of_identical_terms_is_empty(a):
    assert mgu(struct("f", a), struct("f", a)) == substitution()


def test_mgu_failure(a, b):
    result = mgu(a, b)
    assert isinstance(result, Substitution.Fail)
    assert result.is_failed


def test_mgu_arity_mismatch(a):
    assert mgu(struct("f", a), struct("f", a, a)).is_failed


def test_mgu_occur_check_enabled_by_default(X):
    assert mgu(X, struct("f", X)).is_failed


@pytest.mark.parametrize("by_keyword", [False, True])
def test_mgu_without_occur_check(by_keyword, X):
    t = struct("f", X)
    result = mgu(X, t, occur_check=False) if by_keyword else mgu(X, t, False)
    assert result.is_success
    assert result[X] == t


def test_mgu_lists(a, b, X, Y):
    assert mgu(logic_list(X, b), logic_list(a, Y)) == substitution({X: a, Y: b})


def test_mgu_numbers():
    assert mgu(integer(1), integer(1)).is_success
    assert mgu(integer(1), integer(2)).is_failed


# --- unify ----------------------------------------------------------------------------------------


def test_unify_success(a, X):
    assert unify(struct("f", X), struct("f", a)) == struct("f", a)


def test_unify_failure_returns_none(a, b):
    assert unify(a, b) is None


def test_unify_occur_check(X):
    assert unify(X, struct("f", X)) is None
    assert unify(X, struct("f", X), False) is not None


# --- match ----------------------------------------------------------------------------------------


def test_match(a, b, X):
    assert match(struct("f", X), struct("f", a)) is True
    assert match(a, b) is False


def test_match_occur_check(X):
    assert match(X, struct("f", X)) is False
    assert match(X, struct("f", X), False) is True


# --- unificator factories -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "factory", [strict_unificator, naive_unificator, unificator], ids=lambda f: f.__name__
)
def test_unificator_without_context(factory, a, X):
    u = factory()
    assert isinstance(u, Unificator)
    assert u.context == substitution()
    assert u.mgu(X, a) == substitution({X: a})


@pytest.mark.parametrize(
    "factory", [strict_unificator, naive_unificator, unificator], ids=lambda f: f.__name__
)
def test_unificator_with_context(factory, a, b, X):
    u = factory(substitution({X: b}))
    assert u.context == substitution({X: b})
    assert u.mgu(X, a).is_failed
    assert u.mgu(X, b).is_success


def test_strict_and_naive_unificators_differ_on_numbers():
    assert strict_unificator().match(integer(1), atom("1")) is False
    assert naive_unificator().match(integer(1), integer(1)) is True


def test_cached_unificator(a, X):
    base = strict_unificator()
    cached = cached_unificator(base, 2)
    assert isinstance(cached, Unificator)
    for _ in range(3):
        assert cached.mgu(X, a) == substitution({X: a})


def test_cached_unificator_default_capacity(a, X):
    assert cached_unificator(strict_unificator()).mgu(X, a) == substitution({X: a})


def test_unificator_merge(a, X, Y):
    merged = DEFAULT_UNIFICATOR.merge(substitution({X: Y}), substitution({Y: a}))
    assert merged == substitution({X: a, Y: a})


# --- exceptions -----------------------------------------------------------------------------------


def test_no_unify_exception(a, b):
    exception = NoUnifyException(a, b)
    # the message comes from a Kotlin override of getMessage()
    assert exception.message == "Cannot match term `a` with term `b`"
    assert exception.message == exception.getMessage()
    assert isinstance(exception, TuPrologException)
    with pytest.raises(NoUnifyException):
        raise exception


def test_occur_check_exception(X):
    t = struct("f", X)
    exception = OccurCheckException(X, t, X, t)
    assert isinstance(exception, NoUnifyException)
    assert "occurs in term" in exception.message
