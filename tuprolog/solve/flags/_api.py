from collections.abc import Iterable, Mapping

from jpype import JString

from tuprolog.core import Term, to_term
from tuprolog.jvmutils import jmap

from ._definitions import Flag, FlagStore, NotableFlag

__all__ = ["flag", "flag_store"]


def flag(first: str | NotableFlag | Iterable, value: Term | str | float | None = None) -> Flag:
    if isinstance(first, NotableFlag):
        if value is None:
            return first.toPair()
        else:
            return first.to(to_term(value))
    elif isinstance(first, (str, JString)):
        if value is None:
            raise ValueError("Argument value is None")
        return Flag(first, to_term(value))
    elif isinstance(first, Flag) and value is None:
        return first
    elif isinstance(first, Iterable) and value is None:
        items = list(first)
        if len(items) != 2 or not isinstance(items[0], (str, JString)):
            raise ValueError(f"Expected a (name, value) pair, got {items}")
        return Flag(items[0], to_term(items[1]))
    else:
        raise ValueError("Argument first is not iterable nor str")


def _is_pair(items: list) -> bool:
    return len(items) == 2 and isinstance(items[0], (str, JString))


def flag_store(
    *flags: NotableFlag | Flag | Iterable | FlagStore | Mapping[str, Term], **kwargs: Term
) -> FlagStore:
    """Merges flags in argument order (later ones override earlier ones), keyword arguments last."""
    store = FlagStore.EMPTY
    for f in flags:
        if isinstance(f, (NotableFlag, Flag, FlagStore)):
            store = store.plus(f)
        elif isinstance(f, Mapping):
            store = store.plus(jmap({k: to_term(v) for k, v in f.items()}))
        elif isinstance(f, (Term, str, JString)) or not isinstance(f, Iterable):
            # ValueError, consistently with flag()
            raise ValueError(f"Expected flags, flag stores, or iterables of them, got {f!r}")  # noqa: TRY004
        else:
            items = list(f)  # materialized once, as f may be a one-shot iterator
            if _is_pair(items):
                store = store.plus(flag(items))
            else:  # an iterable of flags
                store = store.plus(flag_store(*items))
    if kwargs:
        store = store.plus(jmap({k: to_term(v) for k, v in kwargs.items()}))
    return store
