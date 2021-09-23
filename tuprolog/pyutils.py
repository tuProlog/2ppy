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
