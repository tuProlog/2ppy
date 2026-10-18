"""Pythonic API of tuprolog.collections (it.unibo.tuprolog.collections)."""

from collections.abc import Sized

import pytest

from tuprolog.collections import (
    ClauseCollection,
    ClauseMultiSet,
    ClauseQueue,
    MutableClauseCollection,
    MutableClauseMultiSet,
    MutableClauseQueue,
    RetrieveResult,
    clause_multi_set,
    clause_queue,
)
from tuprolog.core import atom, directive, fact, indicator, rule, struct, var
from tuprolog.unify import strict_unificator

P_A = fact(struct("p", atom("a")))
P_B = fact(struct("p", atom("b")))
Q_X = rule(struct("q", var("X")), struct("p", var("X")))
DYN = directive(struct("dynamic", indicator("r", 1)))


def p_x():
    return fact(struct("p", var("X")))


FACTORIES = [
    pytest.param((clause_multi_set, False, ClauseMultiSet), id="multi_set"),
    pytest.param((clause_multi_set, True, MutableClauseMultiSet), id="mutable_multi_set"),
    pytest.param((clause_queue, False, ClauseQueue), id="queue"),
    pytest.param((clause_queue, True, MutableClauseQueue), id="mutable_queue"),
]


@pytest.fixture(params=FACTORIES)
def make(request):
    factory, mutable, expected_type = request.param

    def build(*clauses, **kwargs):
        collection = factory(*clauses, mutable=mutable, **kwargs)
        assert isinstance(collection, expected_type)
        assert isinstance(collection, ClauseCollection)
        assert isinstance(collection, MutableClauseCollection) == mutable
        return collection

    build.mutable = mutable
    return build


def test_factories_accept_varargs_and_iterables(make):
    assert list(make(P_A, P_B)) == list(make([P_A, P_B]))
    assert len(make()) == 0


def test_sized_iterable_and_truthiness(make):
    collection = make(P_A, P_B, P_A)
    assert isinstance(collection, Sized)
    assert len(collection) == 3
    assert sorted(map(str, collection)) == sorted(map(str, [P_A, P_A, P_B]))
    assert collection
    assert not make()


def test_contains(make):
    collection = make(P_A, Q_X)
    assert P_A in collection
    assert P_B not in collection
    assert collection.contains_all(P_A, Q_X)
    assert collection.contains_all([P_A])
    assert not collection.contains_all(P_A, P_B)


def test_rules_and_directives(make):
    collection = make(P_A, Q_X, DYN)
    assert list(collection.rules) == [P_A, Q_X]
    assert list(collection.directives) == [DYN]


def test_unificator_keyword(make):
    unificator = strict_unificator()
    assert make(P_A, unificator=unificator).unificator == unificator


def test_add(make):
    collection = make(P_A)
    added = collection + P_B
    assert len(added) == 2
    assert len(collection.add_all(P_B, Q_X)) == 3 + (1 if make.mutable else 0)
    assert len(make(P_A) + [P_B, Q_X]) == 3


def test_add_changes_only_mutable_collections(make):
    collection = make(P_A)
    collection.add(P_B)
    assert len(collection) == (2 if make.mutable else 1)


def test_retrieve(make):
    collection = make(P_A, P_B, Q_X)
    result = collection.retrieve(p_x())
    assert isinstance(result, RetrieveResult)
    assert result and result.is_success
    assert len(result.clauses) == 1
    assert result.first_clause in (P_A, P_B)
    assert len(result.collection) == 2


def test_retrieve_all(make):
    result = make(P_A, P_B, Q_X).retrieve_all(p_x())
    assert sorted(map(str, result.clauses)) == sorted(map(str, [P_A, P_B]))
    assert list(result.collection) == [Q_X]


def test_failed_retrieve(make):
    collection = make(P_A)
    result = collection.retrieve(fact(struct("r", var("X"))))
    assert not result
    assert result.is_failure
    assert list(result.collection) == [P_A]


def test_retrieve_changes_only_mutable_collections(make):
    collection = make(P_A, P_B)
    collection.retrieve(p_x())
    assert len(collection) == (1 if make.mutable else 2)


def test_lookup_by_unification(make):
    collection = make(P_A, P_B, Q_X)
    assert sorted(map(str, collection[p_x()])) == sorted(map(str, [P_A, P_B]))
    assert collection[fact(struct("r", var("X")))] == []


def test_multi_set_counts_duplicates():
    multi_set = clause_multi_set(P_A, P_B, P_A)
    assert multi_set.count(P_A) == 2
    assert multi_set.count(Q_X) == 0


def test_multi_set_equality_ignores_order():
    assert clause_multi_set(P_A, P_B, P_A) == clause_multi_set(P_B, P_A, P_A)
    assert clause_multi_set(P_A, P_B) != clause_multi_set(P_A, P_A)


def test_queue_equality_depends_on_order():
    assert clause_queue(P_A, P_B) == clause_queue(P_A, P_B)
    assert clause_queue(P_A, P_B) != clause_queue(P_B, P_A)


def test_queue_order():
    queue = clause_queue(P_A, P_B).add_first(Q_X).add_last(fact(struct("p", atom("c"))))
    assert next(iter(queue)) == Q_X
    assert [str(c) for c in queue.fifo_ordered(p_x())] == [
        "p(a) :- true",
        "p(b) :- true",
        "p(c) :- true",
    ]
    assert queue.lifo_ordered(p_x()) == list(reversed(queue.fifo_ordered(p_x())))
    assert queue[p_x()] == queue.fifo_ordered(p_x())


def test_queue_retrieve_first():
    result = clause_queue(P_A, P_B).retrieve_first(p_x())
    assert result.first_clause == P_A
    assert list(result.collection) == [P_B]


def test_immutable_collections_are_hashable():
    assert hash(clause_multi_set(P_A)) == hash(clause_multi_set(P_A))
    assert hash(clause_queue(P_A)) == hash(clause_queue(P_A))


@pytest.mark.parametrize("factory", [clause_multi_set, clause_queue])
def test_mutable_collections_are_unhashable(factory):
    with pytest.raises(TypeError, match="unhashable"):
        hash(factory(P_A, mutable=True))
