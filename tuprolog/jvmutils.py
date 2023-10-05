from tuprolog import logger
from typing import Iterable as PyIterable, Iterator as PyIterator, Mapping, MutableMapping, Callable, Any
import jpype
import jpype.imports
from _jpype import _JObject as JObjectClass, _JMethod as JMethodClass # type: ignore
import java.util as _jutils # type: ignore
import java.lang as _jlang # type: ignore
import kotlin as _kotlin # type: ignore
import kotlin.sequences as _ksequences # type: ignore
import it.unibo.tuprolog.utils as _tuprolog_utils # type: ignore
from .jvmioutils import *


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


def protect_iterable(iterable: Iterable) -> Iterable:
    return PyUtils.iterable(iterable)


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
        return protect_iterable(self).iterator()


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


def to_snake_case(camel_str: str) -> str:
    return "".join("_" + x.lower() if x.isupper() and camel_str[i + 1:i + 2].islower() else x for i, x in enumerate(camel_str)).lstrip("_")


@jpype.JImplementationFor("java.lang.Object")
class _KtObjectWithSmartPythonicAccessors:
    """
    This class provides every Java imported type with Pythonic versions of its methods and properties,
    unless pythonic versions would conflict with existing members.
    """
    def __jclass_init__(self):
        members = dir(self)
        members_set = set(members)
        for name in members:
            member = getattr(self, name, None)
            if member is None:
                continue
            elif name.startswith("_") or '$' in name or name == 'getClass':
                continue
            elif isinstance(member, JMethodClass):
                if len(name) > 3:
                    snake_case = to_snake_case(name)
                    method_has_0_args = member.__annotations__.keys() == {"return"}
                    add_property = None
                    add_method = (snake_case, member)
                    # Shorten method name and promote to property if it's a getter
                    if method_has_0_args and snake_case.startswith("get_"):
                        property_name = snake_case[4:]
                        if member._isBeanAccessor():
                            getter = member
                            # Attempt to find paired bean setter
                            setter_name = "set" + name.removeprefix("get")
                            setter = getattr(self, setter_name, None)
                            if setter is not None and isinstance(setter, JMethodClass) and setter._isBeanMutator():
                                add_property = (property_name, property(fget=getter, fset=setter))
                            else:
                                add_property = (property_name, property(fget=getter))
                        else:
                            add_property = (property_name, property(fget=member))
                    # Promote method to property if it's a boolean getter
                    elif method_has_0_args and snake_case.startswith("is_"):
                        add_property = (snake_case, property(fget=member))
                        # Do not add method with the same name
                        add_method = None
                    # Add method and property
                    for to_add in (add_property, add_method):
                        if to_add is not None:
                            # Avoid conflicts with existing members
                            if to_add[0] not in members_set or not hasattr(self, to_add[0]):
                                self._customize(*to_add)
                                members_set.add(to_add[0])


@jpype.JImplementationFor("java.lang.Throwable")
class _JvmThrowable:
    def __jclass_init__(self):
        pass

    @property
    def message(self):
        return self.getMessage()


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
