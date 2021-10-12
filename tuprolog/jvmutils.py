from functools import cache

from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyProtectedMember
from _jpype import _JObject as JObjectClass
# noinspection PyUnresolvedReferences
import java.util as _jutils
# noinspection PyUnresolvedReferences
import java.lang as _jlang
# noinspection PyUnresolvedReferences
import kotlin as _kotlin
# noinspection PyUnresolvedReferences
import kotlin.sequences as _ksequences
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.utils as _tuprolog_utils

from typing import Iterable as PyIterable
from typing import Iterator as PyIterator
from typing import Mapping, MutableMapping, Callable, Any

from .jvmioutils import *
import re


Arrays = _jutils.Arrays

ArrayList = _jutils.ArrayList

Iterator = _jutils.Iterator

Map = _jutils.Map

NoSuchElementException = _jutils.NoSuchElementException

Iterable = _jlang.Iterable

JavaSystem = _jlang.System

Object = _jlang.Object

Pair = _kotlin.Pair

Triple = _kotlin.Triple

Sequence = _ksequences.Sequence

SequencesKt = _ksequences.SequencesKt

PyUtils = _tuprolog_utils.PyUtils

class JvmProperty:

    @staticmethod
    def pythonize_name(name: str, boolean: bool = False):
        name = name[2:] if boolean else name[3:]
        words = re.findall('([A-Z]+[a-z]*)|[0-9]+', name)
        if len(words) == 0:
            return name
        snake_case = "_".join(map(str.lower, words))
        if boolean:
            return "is_" + snake_case
        else:
            return snake_case

    def __init__(self, getter_name: str = None, getter = None, setter_name: str = None, setter = None):
        assert (getter_name is not None and getter is not None) or (setter_name is not None and setter is not None)
        self._getter_name = getter_name
        self._getter = getter
        self._setter_name = setter_name
        self._setter = setter

    @property
    def is_readonly(self):
        return self._setter is None

    @property
    def is_writeonly(self):
        return self._getter is None

    @property
    def is_boolean(self):
        return not self.is_writeonly and self._getter_name.startswith('is')

    @property
    @cache
    def python_name(self):
        if self.is_readonly:
            return JvmProperty.pythonize_name(self._getter_name, self.is_boolean)
        else:
            return JvmProperty.pythonize_name(self._setter_name, self.is_boolean)

    @property
    def property(self):
        if self.is_readonly:
            return property(fget=self._getter)
        elif self.is_writeonly:
            return property(fset=self._setter)
        else:
            return property(fget=self._getter, fset=self._setter)

    def set_getter(self, name, method):
        return JvmProperty(name, method, self._setter_name, self._setter)

    def set_setter(self, name, method):
        return JvmProperty(self._getter_name, self._getter, name, method)

    def merge(self, other):
        if self.is_readonly:
            return self.set_setter(other._setter_name, other._setter)
        elif self.is_writeonly:
            return self.set_getter(other._getter_name, other._getter)
        else:
            return self

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, JvmProperty):
            return False
        return self._getter_name == other._getter_name \
            and self._setter_name == other._setter_name \
            and self._getter == other._getter \
            and self._setter == other._setter

    def __hash__(self):
        return hash((self._getter_name, self._getter, self._setter, self._setter_name))

    def __repr__(self):
        return f"JvmProperty({self.python_name}, {self._getter_name or '<no getter>'}" + \
               f", {self._setter_name or '<no setter>'})"

    def __str__(self):
        return repr(self)

    @staticmethod
    def from_class(cls):
        def is_getter_or_setter(method):
            return is_getter(method) or is_setter(method)

        def is_getter(method):
            return method != 'getClass' and method.startswith('get') or method.startswith('is')

        def is_setter(method):
            return method.startswith('set')

        def setter_from_getter(method):
            return 'set' + method[2 if method.startswith('is') else 3]

        def is_zero_args_method(cls, method):
            try:
                cls.class_.getMethod(method, [])
                return True
            except:
                return False

        properties = dict()

        for method in cls.__dict__:
            if is_getter_or_setter(method) and is_zero_args_method(cls, method):
                if is_getter(method):
                    property = JvmProperty(getter_name=method, getter=cls.__dict__[method])
                elif is_setter(method):
                    property = JvmProperty(setter_name=method, setter=cls.__dict__[method])
                else:
                    continue
                if property.python_name in properties:
                    properties[property.python_name] = properties[property.python_name].merge(property)
                else:
                    properties[property.python_name] = property

        return properties.values()


def pythonize_properties(cls):
    properties = JvmProperty.from_class(cls)
    for p in properties:
        cls[p.python_name] = p.property


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


def kpair(items: PyIterable) -> Pair:
    if isinstance(items, Pair):
        return items
    i = iter(items)
    first = next(i)
    second = next(i)
    return Pair(first, second)


@jpype.JConversion("kotlin.Pair", instanceof=PyIterable, excludes=str)
def _kt_pair_covert(jcls, obj):
    return kpair(obj)


def ktriple(items: PyIterable) -> Triple:
    if isinstance(items, Triple):
        return items
    i = iter(items)
    first = next(i)
    second = next(i)
    third = next(i)
    return Triple(first, second, third)


@jpype.JConversion("kotlin.Triple", instanceof=PyIterable, excludes=str)
def _kt_triple_covert(jcls, obj):
    return ktriple(obj)


def jlist(iterable: PyIterable) -> Iterable:
    assert isinstance(iterable, PyIterable)
    if isinstance(iterable, list):
        return Arrays.asList(iterable)
    lst = ArrayList()
    for item in iterable:
        lst.add(item)
    return lst


def jiterable(iterable: PyIterable) -> Iterable:
    assert isinstance(iterable, PyIterable)
    return _IterableAdapter(iterable)


@jpype.JConversion("java.lang.Iterable", instanceof=PyIterable, excludes=str)
def _java_iterable_convert(jcls, obj):
    return jiterable(obj)


def jarray(type, rank: int = 1):
    return jpype.JArray(type, rank)


def jiterator(iterator: PyIterator) -> Iterator:
    assert isinstance(iterator, PyIterator)
    return _IteratorAdapter(iterator)


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


def ksequence(iterable: PyIterable) -> Sequence:
    return SequencesKt.asSequence(jiterable(iterable))


@jpype.JConversion("kotlin.sequences.Sequence", instanceof=PyIterable, excludes=str)
def _kt_sequence_convert(jcls, obj):
    return ksequence(obj)


@jpype.JImplementationFor("java.util.stream.Stream")
class _JvmStream:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return self.iterator()


@jpype.JImplementationFor("java.lang.Comparable")
class _JvmComparable:
    def __jclass_init__(self):
        pass

    def __lt__(self, other):
        return self.compareTo(other) < 0

    def __gt__(self, other):
        return self.compareTo(other) > 0

    def __le__(self, other):
        return self.compareTo(other) <= 0

    def __ge__(self, other):
        return self.compareTo(other) >= 0


class _KtFunction(Callable):
    def __init__(self, arity: int, function: Callable):
        self._function = function
        self._arity = arity

    def invoke(self, *args):
        assert len(args) == self._arity
        return self._function(*args)

    def __call__(self, *args):
        return self.invoke(*args)


_kt_function_classes: MutableMapping[int, Any] = dict()


def kfunction(arity: int):
    if arity not in _kt_function_classes:
        @jpype.JImplements("kotlin.jvm.functions.Function" + str(arity), deferred=True)
        class _KtFunctionN(_KtFunction):
            def __init__(self, f):
                super().__init__(arity, f)

            @jpype.JOverride
            def invoke(self, *args):
                return super().invoke(*args)

        _kt_function_classes[arity] = _KtFunctionN
    return _kt_function_classes[arity]


logger.debug("Configure JVM-specific extensions")
