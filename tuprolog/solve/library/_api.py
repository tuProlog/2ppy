"""The factory functions of libraries and runtimes, re-exported by `tuprolog.solve.library`."""

from collections.abc import Iterable, Mapping
from functools import reduce
from typing import Any

from tuprolog.core import Clause
from tuprolog.core.operators import Operator, OperatorSet, operator_set
from tuprolog.solve import Signature, signature
from tuprolog.solve.function import LogicFunction
from tuprolog.solve.primitive import Primitive

from ._definitions import Library, Pluggable, Runtime

__all__ = ["aliased", "libraries", "library"]


def library(
    alias: str | None = None,
    primitives: Mapping[Signature | str, Primitive] = {},
    clauses: Iterable[Clause] = [],
    operators: OperatorSet | Iterable[Operator] | None = None,
    functions: Mapping[Signature | str, LogicFunction] = {},
) -> Library | Pluggable:
    """Creates a library of primitives, functions, clauses and operators.

    Args:
        alias: The alias of the library, i.e. dot-separated words (e.g. `my.lib`); `default` if
            `None`.
        primitives: The primitives (see `tuprolog.solve.primitive`), keyed by signature or by
            `name/arity` string.
        clauses: The clauses (`tuprolog.core.Clause`), as a list or another JVM-convertible
            collection (not a lazy sequence, like that of `tuprolog.theory.parsing.parse_clauses`).
        operators: The operators, as an `OperatorSet` or an iterable of operators.
        functions: The functions (see `tuprolog.solve.function`), keyed by signature or by
            `name/arity` string.

    Returns:
        The library.

    Examples:
        >>> from tuprolog.core import atom, fact
        >>> lib = library("my.facts", clauses=[fact(atom("sunny"))])
        >>> lib.alias, lib.clauses
        ('my.facts', [sunny :- true])
    """
    primitives = {_signature(k): v for k, v in primitives.items()}
    functions = {_signature(k): v for k, v in functions.items()}
    if operators is None:
        operators = operator_set()
    elif not isinstance(operators, OperatorSet):
        operators = operator_set(list(operators))
    if alias is None:
        return Library.of(primitives, clauses, operators, functions)
    else:
        return Library.of(alias, primitives, clauses, operators, functions)


def _signature(key: Signature | str) -> Signature:
    return signature(key) if isinstance(key, str) else key


def aliased(alias: str, library: Library) -> Library:
    """Returns a copy of a library with another alias.

    Args:
        alias: The new alias.
        library: The library, left unchanged.

    Returns:
        The library with the new alias.

    Examples:
        >>> aliased("new.name", library("old.name")).alias
        'new.name'
    """
    return Library.of(alias, library)


def libraries(*libs: Library | Runtime | Iterable[Library], **kwargs: Library) -> Runtime:
    """Creates a runtime, i.e. a set of libraries with distinct aliases.

    Args:
        *libs: Libraries, runtimes (contributing their libraries), or iterables of them.
        **kwargs: More libraries, loaded under the keyword as alias.

    Returns:
        The runtime; empty without arguments.

    Raises:
        TypeError: If an argument is none of the above.
        tuprolog.solve.library.exception.AlreadyLoadedLibraryException: If two libraries have
            the same alias.

    Examples:
        >>> runtime = libraries(library("a.lib"), [library("b.lib")], c=library("whatever"))
        >>> list(runtime.aliases)
        ['a.lib', 'b.lib', 'c']
    """
    all_libraries: list[Library] = []

    def collect(item: Any) -> None:
        if isinstance(item, Library):
            all_libraries.append(item)
        elif isinstance(item, Runtime):
            all_libraries.extend(item.libraries)
        elif isinstance(item, Iterable) and not isinstance(item, str):
            for nested in item:
                collect(nested)
        else:
            raise TypeError(f"Expected Library, Runtime or Iterable[Library], got {type(item)}")

    collect(libs)
    for alias, library in kwargs.items():
        if not isinstance(library, Library):
            raise TypeError(f"Expected Library for alias {alias}, got {type(library)}")
        all_libraries.append(aliased(alias, library))
    return reduce(lambda a, b: a.plus(b), all_libraries, Runtime.empty())
