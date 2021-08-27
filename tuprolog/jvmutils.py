import logging
import jpype
import jpype.imports

from java.util import NoSuchElementException 
from java.util import Map
from java.util import Iterator
from java.lang import Iterable

from collections.abc import Iterable as PyIterable
from collections.abc import Iterator as PyIterator
from collections.abc import Mapping


def jiterable(iterable):
    assert isinstance(iterable, PyIterable)
    return Iterable@iterable


def jiterator(iterator):
    assert isinstance(iterator, PyIterator)
    return Iterator@iterator


def jmap(dictionary):
    assert isinstance(dictionary, Mapping)
    return Map@dictionary


@jpype.JImplementationFor("kotlin.sequences.Sequence")
class _KtSequence:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return self.iterator()


logging.debug("Configure JVM-specific extensions")
