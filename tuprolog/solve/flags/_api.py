from typing import Iterable, Union, Mapping
from tuprolog.core import Term
from tuprolog.jvmutils import kpair, jmap, jarray
from ._definitions import FlagStore, NotableFlag, Flag


def flag(first: Union[str, NotableFlag, Iterable], value: Term = None) -> Flag:
    if isinstance(first, NotableFlag):
        if value is None:
            return first.toPair()
        else:
            return first.to(value)
    elif isinstance(first, str):
        if value is None:
            raise ValueError("Argument value is None")
        return Flag(first, value)
    elif isinstance(first, Iterable) and value is None:
        return kpair(first)
    else:
        raise ValueError("Argument first is not iterable nor str")


def flag_store(*flags: Union[NotableFlag, Flag, Iterable, FlagStore], **kwargs: Mapping[str, Term]):
    normal_flags = []
    notable_flags = []
    other_stores = []
    for f in flags:
        if isinstance(f, NotableFlag):
            notable_flags.append(f)
        elif isinstance(f, Flag):
            normal_flags.append(f)
        elif isinstance(f, FlagStore):
            other_stores.append(f)
        else:
            normal_flags.append(flag(f))
    store1 = FlagStore.of(jarray(NotableFlag)@notable_flags)
    store2 = FlagStore.of(jarray(Flag)@normal_flags)
    store3 = FlagStore.of(jmap(kwargs))
    store = store1.plus(store2).plus(store3)
    for s in other_stores:
        store = store.plus(s)
    return store
