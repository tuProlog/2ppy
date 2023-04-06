from functools import reduce
from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
from tuprolog.core.operators import OperatorSet, operator_set
from tuprolog.theory import Theory, theory
from tuprolog.solve import Signature
from tuprolog.solve.primitive import Primitive
from tuprolog.solve.function import LogicFunction
from tuprolog.jvmutils import jiterable
from typing import Union, Mapping, Iterable
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.library as _library


Library = _library.Library

Pluggable = _library.Pluggable

Runtime = _library.Runtime


def library(
    alias: str = None,
    primitives: Mapping[Signature, Primitive] = dict(),
    theory: Theory = theory(),
    operators: OperatorSet = operator_set(),
    functions: Mapping[Signature, LogicFunction] = dict(),
) -> Union[Library, Pluggable]:
    if alias is None:
        return Library.of(primitives, theory.clauses, operators, functions)
    else:
        return Library.of(alias, primitives, theory.clauses, operators, functions)


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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.*")