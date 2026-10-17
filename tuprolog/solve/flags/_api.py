from collections.abc import Iterable, Mapping

from jpype import JString

from tuprolog.core import Term
from tuprolog.jvmutils import jmap

from ._definitions import Flag, FlagStore, NotableFlag


def flag(first: str | NotableFlag | Iterable, value: Term = None) -> Flag:
    if isinstance(first, NotableFlag):
        if value is None:
            return first.toPair()
        else:
            return first.to(value)
    elif isinstance(first, (str, JString)):
        if value is None:
            raise ValueError("Argument value is None")
        return Flag(first, value)
    elif isinstance(first, Flag) and value is None:
        return first
    elif isinstance(first, Iterable) and value is None:
        items = list(first)
        if len(items) != 2 or not isinstance(items[0], (str, JString)):
            raise ValueError(f"Expected a (name, value) pair, got {items}")
        return Flag(*items)
    else:
        raise ValueError("Argument first is not iterable nor str")


def flag_store(
    *flags: NotableFlag | Flag | Iterable | FlagStore | Mapping[str, Term], **kwargs: Term
) -> FlagStore:
    """Merges flags in argument order (later ones override earlier ones), keyword arguments last."""
    store = FlagStore.EMPTY
    for f in flags:
        if isinstance(f, (NotableFlag, Flag, FlagStore)):
            store = store.plus(f)
        elif isinstance(f, Mapping):
            store = store.plus(jmap(f))
        else:
            store = store.plus(flag(f))
    if kwargs:
        store = store.plus(jmap(kwargs))
    return store
