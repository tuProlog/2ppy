from collections.abc import Callable, Mapping, MutableMapping
from copy import copy as _copy
from itertools import tee as _tee
from collections.abc import Iterable as PyIterable
from collections.abc import Iterator as PyIterator
from typing import Any

import it.unibo.tuprolog.utils as _tuprolog_utils  # type: ignore
import java.lang as _jlang  # type: ignore
import java.util as _jutils  # type: ignore
import jpype.imports  # noqa: F401
import kotlin as _kotlin  # type: ignore
import kotlin.sequences as _ksequences  # type: ignore
from _jpype import _JMethod as JMethodClass
from _jpype import _JObject as JObjectClass  # type: ignore
from jpype import JArray, JConversion, JImplementationFor, JImplements, JOverride

from tuprolog import logger

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


def protect_iterable(iterable: Any) -> Any:
    return PyUtils.iterable(iterable)


@JImplements("java.util.Iterator", deferred=True)
class _IteratorAdapter:
    def __init__(self, iterator):
        assert isinstance(iterator, PyIterator)
        self._iterator = iterator
        self._queue = None

    @JOverride
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

    @JOverride
    def next(self):
        if self.hasNext():
            return self._queue.pop(0)
        else:
            raise NoSuchElementException()


@JImplements("java.lang.Iterable", deferred=True)
class _IterableAdapter:
    def __init__(self, iterable):
        assert isinstance(iterable, PyIterable)
        if isinstance(iterable, PyIterator):
            # one-shot iterators (e.g. generators) are buffered lazily, as JVM code may iterate
            # an Iterable more than once
            iterable = _tee(iterable, 1)[0]
        self._iterable = iterable

    @JOverride
    def iterator(self):
        if isinstance(self._iterable, PyIterator):
            return _IteratorAdapter(_copy(self._iterable))
        return _IteratorAdapter(iter(self._iterable))


def kpair(items: PyIterable) -> Pair:
    if isinstance(items, Pair):
        return items
    i = iter(items)
    first = next(i)
    second = next(i)
    return Pair(first, second)


@JConversion("kotlin.Pair", instanceof=PyIterable, excludes=str)
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


@JConversion("kotlin.Triple", instanceof=PyIterable, excludes=str)
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


def jiterable(iterable: PyIterable) -> Any:
    assert isinstance(iterable, PyIterable)
    return _IterableAdapter(iterable)


@JConversion("java.lang.Iterable", instanceof=PyIterable, excludes=str)
def _java_iterable_convert(jcls, obj):
    return jiterable(obj)


def jarray(type, rank: int = 1):
    return JArray(type, rank)


def jiterator(iterator: PyIterator) -> Iterator:
    assert isinstance(iterator, PyIterator)
    return _IteratorAdapter(iterator)


def jmap(dictionary: Mapping) -> Map:
    assert isinstance(dictionary, Mapping)
    return Map @ dictionary


def _java_obj_repr(java_object: Any) -> str:
    return str(java_object.toString())


# replaces the default __repr__ implementation for java objects, making them use _java_obj_repr
JObjectClass.__repr__ = _java_obj_repr


@JImplementationFor("kotlin.sequences.Sequence")
class _KtSequence:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return protect_iterable(self).iterator()


def ksequence(iterable: PyIterable) -> Sequence:
    return SequencesKt.asSequence(jiterable(iterable).iterator())


@JConversion("kotlin.sequences.Sequence", instanceof=PyIterable, excludes=str)
def _kt_sequence_convert(jcls, obj):
    return ksequence(obj)


@JImplementationFor("java.util.stream.Stream")
class _JvmStream:
    def __jclass_init__(self):
        PyIterable.register(self)

    def __iter__(self):
        return self.iterator()


@JImplementationFor("java.lang.Comparable")
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
    return "".join(
        "_" + x.lower() if x.isupper() and camel_str[i + 1 : i + 2].islower() else x
        for i, x in enumerate(camel_str)
    ).lstrip("_")


def _virtual_getter(name: str) -> Callable:
    # invoking an unbound JMethod (e.g. as a property fget) is a non-virtual call in JPype,
    # which would ignore overrides in subclasses: look the method up on the instance instead
    return lambda obj: getattr(obj, name)()


def _virtual_setter(name: str) -> Callable:
    return lambda obj, value: getattr(obj, name)(value)


def _is_defined(cls, name: str) -> bool:
    # hasattr() is unreliable here, as properties may fail when accessed on JVM classes
    return any(name in base.__dict__ for base in cls.__mro__)


@JImplementationFor("java.lang.Object")
class _KtObjectWithSmartPythonicAccessors:
    """
    This class provides every Java imported type with Pythonic versions of its methods and properties,
    unless pythonic versions would conflict with existing members.
    """

    def __jclass_init__(self):
        members = dir(self)
        for name in members:
            member = getattr(self, name, None)
            if member is None or name.startswith("_") or "$" in name or name == "getClass":
                continue
            elif isinstance(member, JMethodClass) and len(name) > 3:
                snake_case = to_snake_case(name)
                method_has_0_args = member.__annotations__.keys() == {"return"}
                add_property = None
                add_method = (snake_case, member)
                # Shorten method name and promote to property if it's a getter
                if method_has_0_args and snake_case.startswith("get_"):
                    property_name = snake_case[4:]
                    getter = _virtual_getter(name)
                    if member._isBeanAccessor():
                        # Attempt to find paired bean setter
                        setter_name = "set" + name.removeprefix("get")
                        setter = getattr(self, setter_name, None)
                        if (
                            setter is not None
                            and isinstance(setter, JMethodClass)
                            and setter._isBeanMutator()
                        ):
                            setter = _virtual_setter(setter_name)
                            add_property = (property_name, property(fget=getter, fset=setter))
                        else:
                            add_property = (property_name, property(fget=getter))
                    else:
                        add_property = (property_name, property(fget=getter))
                # Promote method to property if it's a boolean getter
                elif method_has_0_args and snake_case.startswith("is_"):
                    add_property = (snake_case, property(fget=_virtual_getter(name)))
                    # Do not add method with the same name
                    add_method = None
                # Add method and property
                for to_add in (add_property, add_method):
                    # Avoid conflicts with existing members (e.g. those defined by customizers)
                    if to_add is not None and not _is_defined(self, to_add[0]):
                        self._customize(*to_add)


@JImplementationFor("java.lang.Throwable")
class _JvmThrowable:
    def __jclass_init__(self):
        pass

    @property
    def message(self):
        return self.getMessage()


class _KtFunction:
    def __init__(self, arity: int, function: Callable):
        self._function = function
        self._arity = arity

    def invoke(self, *args):
        assert len(args) == self._arity
        return self._function(*args)

    def __call__(self, *args):
        return self.invoke(*args)


_kt_function_classes: MutableMapping[int, Any] = {}


def kfunction(arity: int):
    if arity not in _kt_function_classes:

        @JImplements("kotlin.jvm.functions.Function" + str(arity), deferred=True)
        class _KtFunctionN(_KtFunction):
            def __init__(self, f):
                super().__init__(arity, f)

            @JOverride
            def invoke(self, *args):
                return super().invoke(*args)

        _kt_function_classes[arity] = _KtFunctionN
    return _kt_function_classes[arity]


logger.debug("Configure JVM-specific extensions")
