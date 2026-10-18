"""Pure-Python helpers used throughout the `tuprolog` package.

They let factories accept their arguments in several shapes (e.g. `theory(c1, c2)` as well as
`theory([c1, c2])`), and compose functions with post-processing steps. None of them needs the JVM.
"""

from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, TypeVar

__all__ = [
    "and_then",
    "apply_to_result",
    "dict_or_keyword_args",
    "iterable_or_varargs",
    "register_single_value_type",
]


_T = TypeVar("_T")


# types whose instances are single values even if iterable (e.g. strings, logic lists)
_single_value_types: tuple[type, ...] = (str, bytes)


def register_single_value_type(cls: type) -> None:
    """Makes `iterable_or_varargs` treat the instances of `cls` as single values.

    Strings and bytes are single values out of the box, although they are iterable; packages
    register their own iterable value types, e.g. logic lists, which must not be split into their
    items when passed as the only argument of a factory.

    Args:
        cls: The type whose instances are single values.
    """
    global _single_value_types
    _single_value_types += (cls,)


def iterable_or_varargs(
    args: Sequence[Any], dispatch: Callable[[Iterable[Any]], Any] = lambda x: x
) -> Any:
    """Accepts items given either as several arguments or as one iterable.

    It lets a function with signature `f(*items)` be called both as `f(a, b)` and as `f([a, b])`.

    Args:
        args: The positional arguments received, i.e. `items` in `f(*items)`.
        dispatch: The function to call with the items (the identity, unless given).

    Returns:
        What `dispatch` returns when given the items: the only argument, if it is an iterable but
        not a single value (see `register_single_value_type`); the only argument wrapped in a
        list, if it is not iterable; or all the arguments, otherwise.

    Examples:
        >>> iterable_or_varargs((1, 2, 3))
        (1, 2, 3)
        >>> iterable_or_varargs(([1, 2, 3],))
        [1, 2, 3]
        >>> iterable_or_varargs(("abc",), list)
        ['abc']
    """
    assert isinstance(args, Sequence)
    if len(args) == 1:
        item = args[0]
        if isinstance(item, Iterable) and not isinstance(item, _single_value_types):
            return dispatch(item)
        else:
            return dispatch([item])
    else:
        return dispatch(args)


def dict_or_keyword_args(
    dictionary: Mapping[str, _T],
    kwargs: Mapping[str, _T],
    dispatch: Callable[[Mapping[str, _T]], Any] = lambda x: x,
) -> Any:
    """Accepts key-value pairs given as a mapping, as keyword arguments, or both.

    It lets a function with signature `f(dictionary={}, **kwargs)` be called as `f({"a": 1})`,
    as `f(a=1)`, or as `f({"a": 1}, b=2)`.

    Args:
        dictionary: The pairs given as a mapping.
        kwargs: The pairs given as keyword arguments, overriding those in `dictionary`.
        dispatch: The function to call with the merged pairs (the identity, unless given).

    Returns:
        What `dispatch` returns when given a new dictionary of all the pairs.

    Examples:
        >>> dict_or_keyword_args({"a": 1, "b": 2}, {"b": 3})
        {'a': 1, 'b': 3}
    """
    all_data: dict[str, _T] = {}
    for k in dictionary:
        all_data[k] = dictionary[k]
    for k in kwargs:
        all_data[k] = kwargs[k]
    return dispatch(all_data)


def and_then(continuation: Callable[[Any], Any]) -> Callable[[Callable], Callable]:
    """Creates a decorator post-processing the results of the decorated function.

    Args:
        continuation: The function the results are passed to.

    Returns:
        The decorator: the decorated function returns `continuation(result)` instead of `result`.

    Examples:
        >>> @and_then(list)
        ... def numbers(n):
        ...     return range(n)
        >>> numbers(3)
        [0, 1, 2]
    """

    def call_and_then_continue(function: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            return continuation(result)

        return wrapper

    return call_and_then_continue


def apply_to_result(consumer: Callable[[Any], Any]) -> Callable[[Callable], Callable]:
    """Creates a decorator passing the results of the decorated function to a consumer, too.

    Unlike `and_then`, the decorated function still returns its own results.

    Args:
        consumer: The function the results are passed to, whose own results are ignored.

    Returns:
        The decorator.

    Examples:
        >>> log = []
        >>> @apply_to_result(log.append)
        ... def double(x):
        ...     return 2 * x
        >>> double(21), log
        (42, [42])
    """

    def call_and_then_apply(function: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            consumer(result)
            return result

        return wrapper

    return call_and_then_apply
