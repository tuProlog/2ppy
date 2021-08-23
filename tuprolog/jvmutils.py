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

# @jpype.JImplements("java.util.Iterator", deferred=True)
# class _IteratorAdapter(object):
#     def __init__(self, iterator):
#         assert isinstance(iterator, PyIterator)
#         self._iterator = iterator
#         self._queue = None

#     @jpype.JOverride
#     def hasNext(self):
#         if self._queue is None:
#             try:
#                 self._queue = [next(self._iterator)]
#                 return True
#             except StopIteration:
#                 return False
#         elif len(self._queue) > 0:
#             return True
#         else:
#             try:
#                 self._queue.append(next(self._iterator))
#                 return True
#             except StopIteration:
#                 return False

#     @jpype.JOverride
#     def next(self):
#         if self.hasNext():
#             return self._queue.pop(0)
#         else:
#             raise NoSuchElementException()


# @jpype.JImplements("java.lang.Iterable", deferred=True)
# class _IterableAdapter(object):
#     def __init__(self, iterable):
#         assert isinstance(iterable, PyIterable)
#         self._iterable = iterable

#     @jpype.JOverride
#     def iterator(self):
#         return _IteratorAdapter(iter(self._iterable))


# @jpype.JImplements("java.util.Map", deferred=True)
# class _DictAdapter(object):
#     def __init__(self, dictionary):
#         assert isinstance(dictionary, MutableMapping)
#         self._dictionary = dictionary

#     @jpype.JOverride
#     def iterator(self):
#         return _IteratorAdapter(iter(self._iterable))

#     @jpype.JOverride
#     def remove(self, key):
#         if key in self._dictionary:
#             del self._dictionary[key]
#             return True
#         else:
#             return False

#     @jpype.JOverride
#     def put(self, key, value):
#         if key in self._dictionary:
#             old = self._dictionary[key]
#             self._dictionary[key] = value
#             return old
#         else:
#             self._dictionary[key] = value
#             return None

#     @jpype.JOverride
#     def clear(self):
#         self._dictionary.clear()

#     @jpype.JOverride
#     def containsKey(self, key):
#         return key in self._dictionary

#     @jpype.JOverride
#     def containsValue(self, value):
#         return value in self._dictionary.values()

#     @jpype.JOverride
#     def entrySet(self):
#         ...

#     @jpype.JOverride
#     def equals(self, other):
#         ...

#     @jpype.JOverride
#     def get(self, key):
#         return self._dictionary[key]


# @jpype.JConversion("java.lang.Iterable", instanceof=PyIterable, excludes=str)
# def _JIterableConvert(jcls, obj):
#     return _IterableAdapter(obj)


def jiterable(iterable):
    assert isinstance(iterable, PyIterable)
    return jpype.JObject(iterable, Iterable)


def jiterator(iterator):
    assert isinstance(iterator, PyIterator)
    return jpype.JObject(iterator, Iterator)


def jmap(dictionary):
    assert isinstance(dictionary, Mapping)
    return jpype.JObject(dictionary, Map)


@jpype.JImplementationFor("kotlin.sequences.Sequence")
class _KtSequence:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return self.iterator()


logging.debug("Configure JVM-specific extensions")
