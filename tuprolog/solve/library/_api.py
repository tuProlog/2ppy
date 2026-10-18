from collections.abc import Iterable, Mapping
from functools import reduce

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
    """A library: primitives and functions are keyed by signature, or by `name/arity` string."""
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
    return Library.of(alias, library)


def libraries(*libs: Library | Runtime | Iterable[Library], **kwargs: Library) -> Runtime:
    all_libraries: list[Library] = []

    def collect(item):
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
