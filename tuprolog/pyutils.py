from typing import Iterable, Mapping, TypeVar, Union, Callable

T = TypeVar('T')
R = TypeVar('R')


def iterable_or_varargs(
        args: Union[Iterable[T], Iterable[Iterable[T]]],
        dispatch: Callable[[Iterable[T]], R] = lambda x: x
) -> R:
    assert isinstance(args, Iterable)
    if len(args) == 1:
        item = args[0]
        if isinstance(item, Iterable):
            return dispatch(item)
        else:
            return dispatch([item])
    else:
        return dispatch(args)


def dict_or_keyword_args(
        dictionary: Mapping[str, T],
        kwargs: Mapping[str, T],
        dispatch: Callable[[Mapping[str, T]], R] = lambda x: x
) -> R:
    all_data = dict()
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
