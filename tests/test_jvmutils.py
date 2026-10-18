"""Tests for `tuprolog.jvmutils`."""

from collections.abc import Iterable as PyIterable

import jpype
import pytest

from tuprolog.core import atom, integer, struct, substitution, var
from tuprolog.jvmutils import (
    ArrayList,
    Arrays,
    Iterable,
    Iterator,
    JavaSystem,
    Map,
    NoSuchElementException,
    Object,
    Pair,
    PyUtils,
    Sequence,
    SequencesKt,
    Triple,
    jarray,
    jiterable,
    jiterator,
    jlist,
    jmap,
    kfunction,
    kpair,
    ksequence,
    ktriple,
    protect_iterable,
    to_snake_case,
)
from tuprolog.unify.exception import NoUnifyException

CollectionsKt = jpype.JClass("kotlin.collections.CollectionsKt")
Stream = jpype.JClass("java.util.stream.Stream")
RuntimeException = jpype.JClass("java.lang.RuntimeException")


def test_definitions():
    assert Arrays == jpype.JClass("java.util.Arrays")
    assert ArrayList == jpype.JClass("java.util.ArrayList")
    assert Iterator == jpype.JClass("java.util.Iterator")
    assert Map == jpype.JClass("java.util.Map")
    assert NoSuchElementException == jpype.JClass("java.util.NoSuchElementException")
    assert Iterable == jpype.JClass("java.lang.Iterable")
    assert JavaSystem == jpype.JClass("java.lang.System")
    assert Object == jpype.JClass("java.lang.Object")
    assert Pair == jpype.JClass("kotlin.Pair")
    assert Triple == jpype.JClass("kotlin.Triple")
    assert Sequence == jpype.JClass("kotlin.sequences.Sequence")
    assert SequencesKt == jpype.JClass("kotlin.sequences.SequencesKt")
    assert PyUtils == jpype.JClass("it.unibo.tuprolog.utils.PyUtils")


# --- pairs and triples ----------------------------------------------------------------------------


@pytest.mark.parametrize("items", [(1, 2), [1, 2], iter([1, 2])])
def test_kpair(items):
    pair = kpair(items)
    assert isinstance(pair, Pair)
    assert pair.first == 1
    assert pair.second == 2


def test_kpair_of_pair_is_identity():
    pair = Pair(1, 2)
    assert kpair(pair) is pair


@pytest.mark.parametrize("items", [[], [1], [1, 2, 3]])
def test_kpair_wrong_size(items):
    with pytest.raises(ValueError):
        kpair(items)


def test_pair_conversion():
    pair = Pair @ ("a", atom("b"))
    assert pair.first == "a"
    assert pair.second == atom("b")


def test_pair_conversion_excludes_strings():
    with pytest.raises(TypeError):
        Pair @ "ab"


@pytest.mark.parametrize("items", [(1, 2, 3), [1, 2, 3], iter([1, 2, 3])])
def test_ktriple(items):
    triple = ktriple(items)
    assert isinstance(triple, Triple)
    assert (triple.first, triple.second, triple.third) == (1, 2, 3)


def test_ktriple_of_triple_is_identity():
    triple = Triple(1, 2, 3)
    assert ktriple(triple) is triple


@pytest.mark.parametrize("items", [[1, 2], [1, 2, 3, 4]])
def test_ktriple_wrong_size(items):
    with pytest.raises(ValueError):
        ktriple(items)


def test_triple_conversion():
    assert (Triple @ (1, 2, 3)).third == 3


# --- lists, iterables, iterators, maps, arrays ----------------------------------------------------


@pytest.mark.parametrize("items", [[1, 2, 3], (1, 2, 3), range(1, 4), (x for x in [1, 2, 3])])
def test_jlist(items):
    result = jlist(items)
    assert isinstance(result, jpype.JClass("java.util.List"))
    assert list(result) == [1, 2, 3]
    assert result.size() == 3


def test_jlist_empty():
    assert list(jlist([])) == []


def test_jlist_of_terms():
    assert list(jlist([atom("a"), integer(1)])) == [atom("a"), integer(1)]


def test_jlist_rejects_non_iterables():
    with pytest.raises(AssertionError):
        jlist(1)  # type: ignore[arg-type]


def test_jiterable_is_a_jvm_iterable():
    iterable = jiterable([1, 2, 3])
    assert list(CollectionsKt.toList(iterable)) == [1, 2, 3]


def test_jiterable_can_be_iterated_twice():
    iterable = jiterable([1, 2])
    assert list(CollectionsKt.toList(iterable)) == [1, 2]
    assert list(CollectionsKt.toList(iterable)) == [1, 2]


def test_jiterable_of_generator_can_be_iterated_twice():
    iterable = jiterable(x for x in [1, 2])
    assert list(CollectionsKt.toList(iterable)) == [1, 2]
    assert list(CollectionsKt.toList(iterable)) == [1, 2]


def test_jiterable_of_infinite_generator_is_lazy():
    def naturals():
        n = 0
        while True:
            yield n
            n += 1

    iterator = jiterable(naturals()).iterator()
    assert [iterator.next() for _ in range(3)] == [0, 1, 2]


def test_jiterable_conversion():
    assert list(CollectionsKt.toList(Iterable @ [1, 2])) == [1, 2]


def test_jiterable_rejects_non_iterables():
    with pytest.raises(AssertionError):
        jiterable(1)  # type: ignore[arg-type]


def test_jiterator():
    iterator = jiterator(iter([1, 2]))
    assert iterator.hasNext()
    assert iterator.hasNext()
    assert iterator.next() == 1
    assert iterator.next() == 2
    assert not iterator.hasNext()
    with pytest.raises(NoSuchElementException):
        iterator.next()


def test_jiterator_empty():
    iterator = jiterator(iter([]))
    assert not iterator.hasNext()
    with pytest.raises(NoSuchElementException):
        iterator.next()


def test_jiterator_next_without_has_next():
    iterator = jiterator(iter("ab"))
    assert iterator.next() == "a"
    assert iterator.next() == "b"
    assert not iterator.hasNext()


def test_jiterator_used_by_jvm():
    assert list(SequencesKt.toList(SequencesKt.asSequence(jiterator(iter([1, 2]))))) == [1, 2]


def test_jiterator_rejects_iterables():
    with pytest.raises(AssertionError):
        jiterator([1, 2])  # type: ignore[arg-type]


def test_jmap():
    result = jmap({"a": 1, "b": 2})
    assert isinstance(result, Map)
    assert result.size() == 2
    assert result["a"] == 1
    assert dict(result) == {"a": 1, "b": 2}


def test_jmap_empty():
    assert jmap({}).isEmpty()


def test_jmap_of_terms():
    X = var("X")
    assert jmap({X: atom("a")})[X] == atom("a")


def test_jmap_rejects_non_mappings():
    with pytest.raises(AssertionError):
        jmap([("a", 1)])  # type: ignore[arg-type]


@pytest.mark.parametrize("rank, name", [(1, "int[]"), (2, "int[][]")])
def test_jarray(rank, name):
    array_type = jarray(jpype.JInt, rank)
    assert array_type.class_.getSimpleName() == name


def test_jarray_default_rank():
    assert list(jarray(jpype.JInt)([1, 2])) == [1, 2]


# --- sequences, streams, iterables from the JVM ---------------------------------------------------


def test_ksequence():
    sequence = ksequence([1, 2, 3])
    assert isinstance(sequence, Sequence)
    assert list(sequence) == [1, 2, 3]


def test_ksequence_of_generator():
    assert list(ksequence(x for x in range(3))) == [0, 1, 2]


def test_sequence_conversion():
    assert list(Sequence @ [1, 2]) == [1, 2]


def test_sequences_are_python_iterables():
    sequence = SequencesKt.sequenceOf(1, 2, 3)
    assert isinstance(sequence, PyIterable)
    assert list(sequence) == [1, 2, 3]


def test_term_variables_sequence_is_python_iterable():
    X, Y = var("X"), var("Y")
    assert list(struct("f", X, Y, X).variables) == [X, Y, X]


def test_streams_are_python_iterables():
    stream = Stream.of(1, 2, 3)
    assert isinstance(stream, PyIterable)
    assert list(stream) == [1, 2, 3]


def test_protect_iterable():
    assert list(protect_iterable(jlist([1, 2]))) == [1, 2]
    assert list(protect_iterable(SequencesKt.sequenceOf(1, 2))) == [1, 2]


# --- generic customizations -----------------------------------------------------------------------


def test_jvm_objects_repr_uses_to_string():
    assert repr(struct("f", atom("a"))) == "f(a)"
    assert repr(jlist([1, 2])) == "[1, 2]"


def test_comparable_operators():
    one, two = jpype.JClass("java.lang.Integer")(1), jpype.JClass("java.lang.Integer")(2)
    assert one < two
    assert two > one
    assert one <= jpype.JClass("java.lang.Integer")(1)
    assert two >= one
    assert not (one > two)


def test_throwable_message():
    assert RuntimeException("boom").message == "boom"
    assert RuntimeException().message is None


def test_throwable_message_uses_overrides():
    exception = NoUnifyException(atom("a"), atom("b"))
    assert exception.message == exception.getMessage()
    assert exception.message is not None


def test_snake_case_accessors_are_virtual():
    # Integer.getValue is declared by Constant, and overridden in the implementations
    assert integer(3).value == 3


def test_snake_case_bean_properties():
    lst = jlist([1, 2])
    assert lst.is_empty is False
    assert lst.hash_code() == lst.hashCode()
    assert lst.to_string() == "[1, 2]"


def test_snake_case_setter_properties():
    thread = jpype.JClass("java.lang.Thread")("before")
    assert thread.name == "before"
    thread.name = "after"
    assert thread.getName() == "after"


@pytest.mark.parametrize(
    "camel, snake",
    [
        ("getFooBar", "get_foo_bar"),
        ("isGround", "is_ground"),
        ("freshCopy", "fresh_copy"),
        ("x", "x"),
        ("value", "value"),
        ("setArgs", "set_args"),
    ],
)
def test_to_snake_case(camel, snake):
    assert to_snake_case(camel) == snake


@pytest.mark.parametrize(
    "camel, snake", [("toURI", "to_uri"), ("getHTTPCode", "get_http_code"), ("getX", "get_x")]
)
def test_to_snake_case_acronyms(camel, snake):
    assert to_snake_case(camel) == snake


# --- Kotlin functions -----------------------------------------------------------------------------


@pytest.mark.parametrize("arity", [0, 1, 2, 3])
def test_kfunction(arity):
    function = kfunction(arity)(lambda *args: sum(args) + 1)
    args = list(range(arity))
    assert function(*args) == sum(args) + 1
    assert function.invoke(*args) == sum(args) + 1


def test_kfunction_classes_are_cached():
    assert kfunction(1) is kfunction(1)
    assert kfunction(1) is not kfunction(2)


def test_kfunction_checks_arity():
    with pytest.raises(AssertionError):
        kfunction(1)(lambda x: x)(1, 2)


def test_kfunction_is_a_kotlin_function():
    function = jpype.JObject(kfunction(1)(lambda x: x), "kotlin.jvm.functions.Function1")
    assert function.invoke(5) == 5


def test_kfunction_used_by_jvm():
    a, b, X, Y = atom("a"), atom("b"), var("X"), var("Y")
    function = jpype.JObject(kfunction(2)(lambda v, t: v == X), "kotlin.jvm.functions.Function2")
    assert substitution({X: a, Y: b}).filter(function) == substitution({X: a})
