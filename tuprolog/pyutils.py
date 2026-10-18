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
    global _single_value_types
    _single_value_types += (cls,)


def iterable_or_varargs(
    args: Sequence[Any], dispatch: Callable[[Iterable[Any]], Any] = lambda x: x
) -> Any:
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
    all_data: dict[str, _T] = {}
    for k in dictionary:
        all_data[k] = dictionary[k]
    for k in kwargs:
        all_data[k] = kwargs[k]
    return dispatch(all_data)


def and_then(continuation):
    def call_and_then_continue(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return continuation(result)

        return wrapper

    return call_and_then_continue


def apply_to_result(consumer):
    def call_and_then_apply(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            consumer(result)
            return result

        return wrapper

    return call_and_then_apply
