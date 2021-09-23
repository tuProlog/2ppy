from functools import reduce

from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.library import Library
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.library import Libraries
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.library import LibraryGroup
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.library import AliasedLibrary

# noinspection PyUnresolvedReferences
from tuprolog.core.operators import OperatorSet, operator_set
# noinspection PyUnresolvedReferences
from tuprolog.theory import Theory, theory
# noinspection PyUnresolvedReferences
from tuprolog.solve import Signature
# noinspection PyUnresolvedReferences
from tuprolog.solve.primitive import Primitive
# noinspection PyUnresolvedReferences
from tuprolog.solve.function import LogicFunction
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable

from typing import Union, Mapping, Iterable


def library(
        alias: str = None,
        primitives: Mapping[Signature, Primitive] = dict(),
        theory: Theory = theory(),
        operators: OperatorSet = operator_set(),
        functions: Mapping[Signature, LogicFunction] = dict(),
) -> Union[Library, AliasedLibrary]:
    if alias is None:
        return Library.unaliased(primitives, theory, operators, functions)
    else:
        return Library.aliased(alias, primitives, theory, operators, functions)


def aliased(alias: str, library: Library) -> AliasedLibrary:
    return Library.of(alias, library)


def libraries(
        *libs: Union[Libraries, AliasedLibrary, Iterable[Union[Libraries, AliasedLibrary]]],
        **kwargs: Library
) -> Libraries:
    all_libraries = []
    aliased_libs = []
    queue = list(libs)
    while len(queue) > 0:
        current = queue.pop()
        if isinstance(current, Libraries):
            all_libraries.append(current)
        elif isinstance(current, AliasedLibrary):
            aliased_libs.append(current)
        else:
            queue.extend(current)
    for alias in kwargs:
        aliased_libs.append(aliased(alias, kwargs[alias]))
    first = Libraries.of(jiterable(aliased_libs))
    return reduce(lambda a, b: a.plus(b), all_libraries, first)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.library.*")