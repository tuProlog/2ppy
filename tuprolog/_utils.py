from collections.abc import Iterable

def iterable_or_varargs(args, dispatch=lambda x: x):
    assert isinstance(args, Iterable)
    if len(args) == 1:
        item = args[0]
        if isinstance(item, Iterable):
            return dispatch(item)
        else:
            return dispatch([item])
    else:
        return dispatch(args)
    