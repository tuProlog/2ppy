from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyProtectedMember
from _jpype import _JObject as JObjectClass

# noinspection PyUnresolvedReferences
from java.util import NoSuchElementException
# noinspection PyUnresolvedReferences
from java.util import Map
# noinspection PyUnresolvedReferences
from java.util import Iterator
# noinspection PyUnresolvedReferences
from java.lang import Iterable
# noinspection PyUnresolvedReferences
from java.lang import Object

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.utils import PyUtils

from collections.abc import Iterable as PyIterable
from collections.abc import Iterator as PyIterator
from collections.abc import Mapping

from .jvmioutils import *


def jiterable(iterable: PyIterable) -> Iterable:
    assert isinstance(iterable, PyIterable)
    return Iterable@iterable


def jiterator(iterator: PyIterator) -> Iterator:
    assert isinstance(iterator, PyIterator)
    return Iterator@iterator


def jmap(dictionary: Mapping) -> Map:
    assert isinstance(dictionary, Mapping)
    return Map@dictionary


def _java_obj_repr(java_object: Object) -> str:
    return str(java_object.toString())


# replaces the default __repr__ implementation for java objects, making them use _java_obj_repr
JObjectClass.__repr__ = _java_obj_repr


@jpype.JImplementationFor("kotlin.sequences.Sequence")
class _KtSequence:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return PyUtils.iterable(self).iterator()


@jpype.JImplementationFor("java.util.stream.Stream")
class _JvmStream:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return self.iterator()


logger.debug("Configure JVM-specific extensions")
