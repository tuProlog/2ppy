import logging
import jpype
import jpype.imports

from java.util import NoSuchElementException 

from collections.abc import Iterable as PyIterable
from collections.abc import Iterator as PyIterator

@jpype.JImplements("java.util.Iterator", deferred=True)
class _IteratorAdapter(object):
    def __init__(self, iterator):
        assert isinstance(iterator, PyIterator)
        self._iterator = iterator
        self._queue = None

    @jpype.JOverride
    def hasNext(self):
        if self._queue is None:
            try:
                self._queue = [next(self._iterator)]
                return True
            except StopIteration:
                return False
        elif len(self._queue) > 0:
            return True
        else:
            try:
                self._queue.append(next(self._iterator))
                return True
            except StopIteration:
                return False

    @jpype.JOverride
    def next(self):
        if self.hasNext():
            return self._queue.pop(0)
        else:
            raise NoSuchElementException()


@jpype.JImplements("java.lang.Iterable", deferred=True)
class _IterableAdapter(object):
    def __init__(self, iterable):
        assert isinstance(iterable, PyIterable)
        self._iterable = iterable

    @jpype.JOverride
    def iterator(self):
        return _IteratorAdapter(iter(self._iterable))


@jpype.JConversion("java.lang.Iterable", instanceof=PyIterable, excludes=str)
def _JIterableConvert(jcls, obj):
    return _IterableAdapter(obj)


def jiterable(iterable):
    return _IterableAdapter(iterable)


def jiterator(iterator):
    return IteratorAdapter(iterator)


@jpype.JImplementationFor("kotlin.sequences.Sequence")
class _KtSequence:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return self.iterator()


logging.debug("Configure JVM-specific extensions")
