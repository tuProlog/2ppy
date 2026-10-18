"""Tests for `tuprolog.pyutils`."""

import pytest

from tuprolog.pyutils import and_then, apply_to_result, dict_or_keyword_args, iterable_or_varargs


def test_iterable_or_varargs_no_args():
    assert list(iterable_or_varargs(())) == []


def test_iterable_or_varargs_many_args():
    assert list(iterable_or_varargs((1, 2, 3))) == [1, 2, 3]


def test_iterable_or_varargs_single_non_iterable():
    assert list(iterable_or_varargs((1,))) == [1]


@pytest.mark.parametrize("collection", [[1, 2], (1, 2), {1, 2}, range(1, 3)])
def test_iterable_or_varargs_single_iterable(collection):
    assert sorted(iterable_or_varargs((collection,))) == [1, 2]


def test_iterable_or_varargs_single_generator():
    assert list(iterable_or_varargs(((x for x in [1, 2]),))) == [1, 2]


@pytest.mark.parametrize("text", ["abc", "", b"abc"])
def test_iterable_or_varargs_does_not_split_a_single_string(text):
    assert list(iterable_or_varargs((text,))) == [text]


def test_iterable_or_varargs_many_strings():
    assert list(iterable_or_varargs(("ab", "cd"))) == ["ab", "cd"]


def test_iterable_or_varargs_nested_iterables_are_not_flattened():
    assert list(iterable_or_varargs(([1], [2]))) == [[1], [2]]


def test_iterable_or_varargs_dispatch():
    assert iterable_or_varargs((1, 2), lambda xs: sum(xs)) == 3
    assert iterable_or_varargs(([1, 2],), lambda xs: sum(xs)) == 3
    assert iterable_or_varargs((5,), lambda xs: sum(xs)) == 5


def test_iterable_or_varargs_requires_a_sequence():
    with pytest.raises(TypeError):
        iterable_or_varargs(x for x in [1])  # type: ignore[arg-type]


def test_dict_or_keyword_args():
    assert dict_or_keyword_args({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_dict_or_keyword_args_kwargs_win():
    assert dict_or_keyword_args({"a": 1}, {"a": 2}) == {"a": 2}


def test_dict_or_keyword_args_empty():
    assert dict_or_keyword_args({}, {}) == {}


def test_dict_or_keyword_args_dispatch():
    assert dict_or_keyword_args({"a": 1}, {"b": 2}, lambda d: sorted(d)) == ["a", "b"]


def test_dict_or_keyword_args_does_not_mutate_inputs():
    first, second = {"a": 1}, {"b": 2}
    dict_or_keyword_args(first, second)
    assert first == {"a": 1}
    assert second == {"b": 2}


def test_and_then():
    @and_then(lambda x: x * 10)
    def add(x, y=0):
        return x + y

    assert add(1, y=2) == 30


def test_apply_to_result():
    seen = []

    @apply_to_result(seen.append)
    def identity(x):
        return x

    assert identity(42) == 42
    assert seen == [42]
