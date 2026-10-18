import re
from collections.abc import Callable, Mapping, MutableMapping
from collections.abc import Iterable as PyIterable
from collections.abc import Iterator as PyIterator
from copy import copy as _copy
from itertools import tee as _tee
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

__all__ = [
    "ArrayList",
    "Arrays",
    "Iterable",
    "Iterator",
    "JavaSystem",
    "Map",
    "NoSuchElementException",
    "Object",
    "Pair",
    "PyUtils",
    "Sequence",
    "SequencesKt",
    "Triple",
    "customize_derived",
    "jarray",
    "jiterable",
    "jiterator",
    "jlist",
    "jmap",
    "jvm_method",
    "kfunction",
    "kpair",
    "ksequence",
    "ktriple",
    "protect_iterable",
    "to_snake_case",
]


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


_ITERABLE_ITERATOR = Iterable.class_.getMethod("iterator")

_ITERATOR_HAS_NEXT = Iterator.class_.getMethod("hasNext")

_ITERATOR_NEXT = Iterator.class_.getMethod("next")


def _is_anonymous(obj: Any) -> bool:
    # JPype wraps instances of non-public JVM classes (e.g. Kotlin's synthetic Iterable
    # implementations) as java.lang.Object$Anonymous, hiding their interfaces
    return type(obj).__name__ == "java.lang.Object$Anonymous"


def _iterate_reflectively(iterable: Any) -> PyIterator:
    # interface methods are still callable via reflection on anonymous instances
    iterator = _ITERABLE_ITERATOR.invoke(iterable)
    while _ITERATOR_HAS_NEXT.invoke(iterator):
        yield _ITERATOR_NEXT.invoke(iterator)


def protect_iterable(iterable: Any) -> Any:
    if _is_anonymous(iterable):
        return iterable  # Python-iterable, see _KtObjectWithSmartPythonicAccessors
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
    first, second = items
    return Pair(first, second)


@JConversion("kotlin.Pair", instanceof=PyIterable, excludes=str)
def _kt_pair_covert(jcls, obj):
    return kpair(obj)


def ktriple(items: PyIterable) -> Triple:
    if isinstance(items, Triple):
        return items
    first, second, third = items
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


_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def to_snake_case(camel_str: str) -> str:
    """E.g. getHTTPCode -> get_http_code, toURI -> to_uri, assertA -> assert_a."""
    return _CAMEL_BOUNDARY.sub("_", camel_str).lower()


def _virtual_getter(name: str) -> Callable:
    # invoking an unbound JMethod (e.g. as a property fget) is a non-virtual call in JPype,
    # which would ignore overrides in subclasses: look the method up on the instance instead
    return lambda obj: getattr(obj, name)()


def _virtual_setter(name: str) -> Callable:
    return lambda obj, value: getattr(obj, name)(value)


def _is_defined(cls, name: str) -> bool:
    # hasattr() is unreliable here, as properties may fail when accessed on JVM classes
    return any(name in base.__dict__ for base in cls.__mro__)


def _dispatch_overloads(methods: list) -> Callable:
    if len(methods) == 1:
        return methods[0]

    def dispatch(self, *args, **kwargs):
        # binding before calling keeps JVM calls virtual
        for method in methods[:-1]:
            try:
                return method.__get__(self)(*args, **kwargs)
            except TypeError as e:
                if not str(e).startswith("No matching overloads"):
                    raise
        return methods[-1].__get__(self)(*args, **kwargs)

    return dispatch


def _jvm_methods(cls, name: str, *aliases: str) -> list:
    methods = []
    for base in cls.__mro__:
        for key in (name,) + aliases:
            method = base.__dict__.get(key)
            if isinstance(method, JMethodClass) and method not in methods:
                methods.append(method)
    return methods


def jvm_method(obj: Any, name: str) -> Callable:
    """The JVM method `name` of `obj`, with all the overloads declared along its class hierarchy,
    even when Python members (e.g. customizers, or auto-generated snake_case properties) shadow it."""
    return _dispatch_overloads(_jvm_methods(type(obj), name, "_jvm_" + name, "_" + name)).__get__(
        obj
    )


def customize_derived(*names: str) -> Callable:
    """
    Class decorator for customizers (to be put below `@JImplementationFor`): applies the members
    `names` of the customizer to every class deriving from the customized one, too.

    JPype copies a customizer's members onto the customized class only: a derived class (re)declaring
    a JVM method with the same name would shadow them. Here the JVM methods are kept as `_<name>`, as
    `@JOverride` does on the customized class itself. As JPype splits overloads among the classes
    declaring them (e.g. MutableTheory.equals(Object) vs AbstractTheory.equals(Theory, Boolean)),
    `_<name>` tries all the JVM methods named `name` along the MRO.
    """

    def decorator(proto):
        init = proto.__dict__.get("__jclass_init__")

        def __jclass_init__(cls):
            if init is not None:
                init(cls)
            for name in names:
                member = proto.__dict__[name]
                own = cls.__dict__.get(name)
                if isinstance(own, JMethodClass):  # keeps it for derived classes
                    cls._customize("_jvm_" + name, own)
                methods = _jvm_methods(cls, name, "_jvm_" + name, "_" + name)
                if methods:
                    cls._customize("_" + name, _dispatch_overloads(methods))
                if getattr(cls, name, None) is not member:
                    cls._customize(name, member)

        proto.__jclass_init__ = __jclass_init__
        return proto

    return decorator


def _anonymous_iter(self):
    if not Iterable.class_.isInstance(self):
        raise TypeError(f"'{type(self).__name__}' object is not iterable")
    return _iterate_reflectively(self)


@JImplementationFor("java.lang.Object")
class _KtObjectWithSmartPythonicAccessors:
    """
    This class provides every Java imported type with Pythonic versions of its methods and properties,
    unless pythonic versions would conflict with existing members.
    """

    def __jclass_init__(self):
        if self.__name__ == "java.lang.Object$Anonymous":
            self._customize("__iter__", _anonymous_iter)
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
        message = self.getMessage()
        return None if message is None else str(message)


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
