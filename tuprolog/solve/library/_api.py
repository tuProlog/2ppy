from typing import Union, Mapping, Iterable
from functools import reduce
from tuprolog.jvmutils import protect_iterable
from tuprolog.core.operators import OperatorSet, operator_set
from tuprolog.theory import Clause
from tuprolog.solve import Signature
from tuprolog.solve.primitive import Primitive
from tuprolog.solve.function import LogicFunction
from ._definititions import Library, Pluggable


def library(
    alias: str = None,
    primitives: Mapping[Signature, Primitive] = dict(),
    clauses: Iterable[Clause] = [],
    operators: OperatorSet = operator_set(),
    functions: Mapping[Signature, LogicFunction] = dict(),
) -> Union[Library, Pluggable]:
    if alias is None:
        return Library.of(primitives, clauses, operators, functions)
    else:
        return Library.of(alias, primitives, clauses, operators, functions)


def aliased(alias: str, library: Library) -> Library:
    return Library.of(alias, library)


def libraries(
        *libs: Union[Library, Iterable[Library]],
        **kwargs: Library
) -> Library:
    all_libraries = []
    queue = list(libs)
    while len(queue) > 0:
        current = queue.pop()
        if isinstance(current, Library):
            all_libraries.append(current)
        elif isinstance(current, Iterable):
            queue.extend(current)
        else:
            raise TypeError(f'Expected Library or Iterable[Library], got {type(current)}')
    for alias, library in kwargs.items():
        if isinstance(library, Library):
            all_libraries.append(aliased(alias, kwargs[alias]))
    return reduce(lambda a, b: a.plus(b), all_libraries, Library.of({}, [], operator_set(), {}))
