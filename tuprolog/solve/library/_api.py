from collections.abc import Iterable, Mapping
from functools import reduce

from tuprolog.core.operators import OperatorSet, operator_set
from tuprolog.solve import Signature
from tuprolog.solve.function import LogicFunction
from tuprolog.solve.primitive import Primitive
from tuprolog.theory import Clause

from ._definititions import Library, Pluggable, Runtime


def library(
    alias: str | None = None,
    primitives: Mapping[Signature, Primitive] = {},
    clauses: Iterable[Clause] = [],
    operators: OperatorSet | None = None,
    functions: Mapping[Signature, LogicFunction] = {},
) -> Library | Pluggable:
    if operators is None:
        operators = operator_set()
    if alias is None:
        return Library.of(primitives, clauses, operators, functions)
    else:
        return Library.of(alias, primitives, clauses, operators, functions)


def aliased(alias: str, library: Library) -> Library:
    return Library.of(alias, library)


def libraries(*libs: Library | Iterable[Library], **kwargs: Library) -> Runtime:
    all_libraries = []
    queue = list(libs)
    while len(queue) > 0:
        current = queue.pop()
        if isinstance(current, Library):
            all_libraries.append(current)
        elif isinstance(current, Iterable):
            queue.extend(current)
        else:
            raise TypeError(f"Expected Library or Iterable[Library], got {type(current)}")
    for alias, library in kwargs.items():
        if isinstance(library, Library):
            all_libraries.append(aliased(alias, library))
    return reduce(lambda a, b: a.plus(b), all_libraries, Runtime.empty())
