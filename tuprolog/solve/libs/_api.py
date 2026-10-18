"""2P-Kt's OOPLib Prolog API, over Python objects instead of JVM ones.

Objects are referred to by atoms (`'<object:list#7f...>'`, `'<type:collections.Counter>'`,
`'<module:math>'`, `'<null>'`) and aliases (`$math`); calls take Python values converted from
terms, and give back terms for numbers, booleans and strings, references for any other object.
"""

import builtins
import decimal
import importlib
import inspect
import math
import sys
import types
from collections.abc import Callable, Iterable, Iterator, Mapping
from typing import Any

from tuprolog.core import Atom, Struct, Term, Var, atom, logic_list, struct, to_python, to_term
from tuprolog.core.operators import DEFAULT_OPERATORS, FX, XFX, XFY, operator, operator_set
from tuprolog.solve import signature
from tuprolog.solve.exception.error.existence import existence_error, object_type
from tuprolog.solve.exception.error.instantiation import instantiation_error_for_argument
from tuprolog.solve.exception.error.permission import operation, permission_error, permission_type
from tuprolog.solve.exception.error.type import expected_type, type_error_for_argument
from tuprolog.solve.library import Library, library
from tuprolog.solve.primitive import Primitive, SolveRequest, SolveResponse, primitive
from tuprolog.theory.parsing import ClausesParser

__all__ = ["NULL_REF", "SAFE_MODULES", "OOPLib", "oop_lib"]

NULL_REF = atom("<null>")
"""The reference (the atom `'<null>'`) standing for Python's `None` in OOPLib calls.

Results that are `None` become this atom, and this atom in arguments becomes `None`; `null_ref/1`
gives it to Prolog code.
"""

# importable by default (by `type/2` or as `$name`): side-effect free standard modules
SAFE_MODULES = frozenset(
    {
        "bisect",
        "calendar",
        "cmath",
        "collections",
        "copy",
        "datetime",
        "decimal",
        "difflib",
        "enum",
        "fractions",
        "functools",
        "heapq",
        "itertools",
        "json",
        "math",
        "random",
        "re",
        "statistics",
        "string",
        "textwrap",
        "time",
        "unicodedata",
        "uuid",
    }
)
"""The names of the standard modules OOPLib can import by default (a frozen set).

Side-effect free modules of the standard library (e.g. `math`, `json`, `re`, `collections`,
`datetime`): Prolog code can refer to them as aliases (e.g. `$math`) and to their types by
`type/2` (e.g. `type('collections.Counter', T)`). Other modules are importable only with
`oop_lib(allow_all_imports=True)`.

Examples:
    >>> "math" in SAFE_MODULES, "os" in SAFE_MODULES
    (True, False)
"""

# built-ins giving access to code execution, files, or arbitrary attributes
_UNSAFE_BUILTINS = frozenset(
    {
        "__import__",
        "breakpoint",
        "compile",
        "delattr",
        "eval",
        "exec",
        "exit",
        "getattr",
        "globals",
        "help",
        "input",
        "locals",
        "open",
        "quit",
        "setattr",
        "vars",
    }
)

# 2P-Kt's OOPLib aliases, mapped onto Python types, and Python's own names
_TYPE_ALIASES: dict[str, Any] = {
    "string": str,
    "array": tuple,
    "list": list,
    "arraylist": list,
    "map": dict,
    "hashmap": dict,
    "int": int,
    "integer": int,
    "double": float,
    "float": float,
    "long": int,
    "short": int,
    "byte": int,
    "char": str,
    "bool": bool,
    "boolean": bool,
    "any": object,
    "nothing": type(None),
    "big_integer": int,
    "big_decimal": decimal.Decimal,
    "str": str,
    "tuple": tuple,
    "dict": dict,
    "set": set,
    "frozenset": frozenset,
    "range": range,
    "complex": complex,
    "bytes": bytes,
    "object": object,
}

# resolved when used, as Python's current standard streams may be replaced
_STREAM_ALIASES: dict[str, Callable[[], Any]] = {
    "stdin": lambda: sys.stdin,
    "stdout": lambda: sys.stdout,
    "stderr": lambda: sys.stderr,
}

OPERATORS = operator_set(
    operator(".", XFY, 800),
    operator("as", XFX, 200),
    operator(":=", XFX, 850),
    operator("$", FX, 100),
)
"""The operators OOPLib adds: `.`, `:=`, `as`, and `$`.

That is, `.` (`xfy`, 800), `:=` (`xfx`, 850), `as` (`xfx`, 200), and `$` (`fx`, 100).

See `tuprolog.solve.libs` for the syntax they enable.
"""

# the same rules as 2P-Kt's OOPLib, for fluent calls (`Obj.method(...)`) and assignments (`:=`)
CLAUSES = """
R := as(X, T) :- var(R), !, fluent_reduce(X, Y), cast(Y, T, R).
R := M :- var(R), !, fluent_reduce(M, R).
C := V :- property_reduce(C, R, P), assign(R, P, V).
[Ref | Method] :- fluent_reduce([Ref | Method], _).
fluent_reduce([P, M | X], R) :- !, invoke_method(P, M, P1), fluent_reduce([P1 | X], R).
fluent_reduce([P | M], R) :- !, invoke_method(P, M, R).
fluent_reduce(R, R) :- !.
new_object(Type, Instance) :- new_object(Type, [], Instance).
property_reduce([A, B | C], O, P) :- !, invoke_method(A, B, B1), property_reduce([B1 | C], O, P).
property_reduce([A | B], A, B) :- !.
"""
"""The Prolog source of the rules OOPLib defines on top of its primitives (as 2P-Kt's OOPLib).

They implement fluent calls (`Receiver.method(Args)`), evaluations and assignments (`:=`), and
`new_object/2`.
"""


class _Failure(Exception):
    """A logic error to reply with, built once the request is known."""

    def __init__(self, error: Callable[[SolveRequest], Any]):
        self.error = error


def _type_error(index: int, expected: str, culprit: Term) -> _Failure:
    return _Failure(
        lambda r: type_error_for_argument(
            r.context, r.signature, expected_type(expected), culprit, index
        )
    )


def _existence_error(kind: str, culprit: Term, message: str) -> _Failure:
    return _Failure(lambda r: existence_error(r.context, object_type(kind), culprit, message))


class _PythonObjects:
    def __init__(
        self, allow_all_imports: bool, allow_private: bool, aliases: Mapping[str, Any] | None
    ):
        self.allow_all_imports = allow_all_imports
        self.allow_private = allow_private
        self.references: dict[str, Any] = {}
        self.names: dict[int, str] = {}
        safe_builtins = types.SimpleNamespace(
            **{
                name: value
                for name, value in vars(builtins).items()
                if not name.startswith("_") and (allow_all_imports or name not in _UNSAFE_BUILTINS)
            }
        )
        # OOPLib's type aliases win over modules' names (i.e. $string is str, not the string module)
        self.preset: dict[str, Any] = {name: importlib.import_module(name) for name in SAFE_MODULES}
        self.preset.update(_TYPE_ALIASES, builtins=safe_builtins)
        if allow_all_imports:
            self.preset.update(builtins=builtins, system=sys, sys=sys)
        self.preset.update(aliases or {})
        self.registered: dict[str, Any] = {}

    # --- references ---------------------------------------------------------------------------

    def reference(self, value: Any) -> Atom:
        if value is None:
            return NULL_REF
        name = self.names.get(id(value))
        if name is None or self.references.get(name) is not value:
            if isinstance(value, type):
                name = f"<type:{value.__module__}.{value.__qualname__}>"
            elif isinstance(value, types.ModuleType):
                name = f"<module:{value.__name__}>"
            else:
                name = f"<object:{type(value).__qualname__}#{id(value):x}>"
            if name in self.references and self.references[name] is not value:
                name = f"{name[:-1]}#{id(value):x}>"
            self.references[name] = value
            self.names[id(value)] = name
        return atom(name)

    def is_reference(self, term: Term) -> bool:
        return isinstance(term, Atom) and (term == NULL_REF or str(term.value) in self.references)

    def referenced(self, term: Term) -> Any:
        return None if term == NULL_REF else self.references[str(term.value)]

    # --- conversions --------------------------------------------------------------------------

    def alias(self, name: str) -> Any:
        if name in self.registered:
            return self.registered[name]
        if name in _STREAM_ALIASES:
            return _STREAM_ALIASES[name]()
        return self.preset[name]

    def aliases(self) -> Iterator[tuple[str, Any]]:
        for name in {**self.preset, **_STREAM_ALIASES, **self.registered}:
            yield name, self.alias(name)

    def value(self, term: Term, index: int) -> Any:
        """The Python value of a term: references and aliases are dereferenced, inside
        collections too, other terms are converted (see `to_python`)."""
        if isinstance(term, Var):
            raise _Failure(
                lambda r: instantiation_error_for_argument(r.context, r.signature, term, index)
            )
        if self.is_reference(term):
            return self.referenced(term)
        if isinstance(term, Struct) and str(term.functor) == "$" and term.arity == 1:
            name = term[0]
            if not isinstance(name, Atom):
                raise _type_error(index, "dealiasing_expression", term)
            try:
                return self.alias(str(name.value))
            except KeyError:
                raise _existence_error("OOP_ALIAS", name, f"There is no alias `{name}`") from None
        converted = to_python(term)
        if isinstance(converted, list):
            return [self.value(item, index) for item in term]
        if isinstance(converted, tuple):
            return tuple(self.value(item, index) for item in term.unfolded)
        return converted

    def arguments(self, terms: Iterable[Term], index: int) -> tuple[list, dict]:
        """Positional and keyword (`Key = Value`) arguments of a call."""
        args, kwargs = [], {}
        for term in terms:
            if _is_keyword_argument(term):
                kwargs[str(term[0].value)] = self.value(term[1], index)
                continue
            args.append(self.value(term, index))
        return args, kwargs

    def term(self, value: Any) -> Term:
        """Numbers, booleans and strings become terms, any other object a reference."""
        if isinstance(value, (bool, int, float, decimal.Decimal, str)):
            if isinstance(value, float) and not math.isfinite(value):
                return self.reference(value)
            return to_term(value)
        return self.reference(value)

    # --- operations ---------------------------------------------------------------------------

    def resolve_type(self, name: str) -> Any:
        if name in self.preset or name in self.registered:
            return self.alias(name)
        if "." not in name:
            if hasattr(builtins, name) and (self.allow_all_imports or name not in _UNSAFE_BUILTINS):
                return getattr(builtins, name)
            raise _existence_error("OOP_ALIAS", atom(name), f"There is no type named `{name}`")
        module_name, _, attribute = name.rpartition(".")
        for candidate in (name, module_name):
            if self.allow_all_imports or candidate.split(".")[0] in SAFE_MODULES:
                try:
                    module = importlib.import_module(candidate)
                except ImportError:
                    continue
                return module if candidate == name else self.attribute(module, attribute, 0)
        raise _existence_error("OOP_ALIAS", atom(name), f"There is no importable type `{name}`")

    def type_value(self, term: Term, index: int) -> Any:
        if isinstance(term, Atom) and not self.is_reference(term):
            return self.resolve_type(str(term.value))
        return self.value(term, index)

    def attribute(self, receiver: Any, name: str, index: int) -> Any:
        if name.startswith("_") and not self.allow_private:
            raise _Failure(
                lambda r: permission_error(
                    r.context,
                    r.signature,
                    operation("access"),
                    permission_type("oop_method"),
                    atom(name),
                )
            )
        try:
            return getattr(receiver, name)
        except AttributeError:
            message = f"There is no attribute `{name}` on {type(receiver).__qualname__} objects"
            raise _existence_error("OOP_METHOD", atom(name), message) from None

    def invoke(self, receiver: Any, method: Term, index: int) -> Any:
        if isinstance(method, Atom):
            found = self.attribute(receiver, str(method.value), index)
            return found() if inspect.isroutine(found) else found
        if isinstance(method, Struct):
            args, kwargs = self.arguments(method.args, index)
            return self.attribute(receiver, str(method.functor), index)(*args, **kwargs)
        raise _type_error(index, "callable", method)


def _is_keyword_argument(term: Term) -> bool:
    return (
        isinstance(term, Struct)
        and str(term.functor) == "="
        and term.arity == 2
        and isinstance(term[0], Atom)
    )


def _unify(request: SolveRequest, *pairs: tuple[Term, Term]) -> SolveResponse:
    goal = struct("pairs", [a for a, _ in pairs])
    values = struct("pairs", [b for _, b in pairs])
    mgu = request.context.unificator.mgu(goal, values)
    return request.reply_fail() if mgu.isFailed() else request.reply_success(mgu)


def _primitive(
    function: Callable[[SolveRequest, list[Term]], Iterable[SolveResponse]],
) -> Primitive:
    def solve(request: SolveRequest) -> Iterator[SolveResponse]:
        try:
            yield from function(request, list(request.arguments))
        except _Failure as failure:
            yield request.reply_exception(failure.error(request))

    return primitive(solve)


def oop_lib(
    allow_all_imports: bool = False,
    allow_private: bool = False,
    aliases: Mapping[str, Any] | None = None,
) -> Library:
    """Creates an OOPLib library, letting Prolog code use Python objects.

    It offers 2P-Kt's OOPLib Prolog API over Python objects: the predicates `type/2`,
    `new_object/2,3`, `invoke_method/3`, `assign/3`, `cast/3`, `register/2`, `unregister/1`,
    `alias/2`, `ref/1`, `object_ref/1`, `type_ref/1`, `null_ref/1`, `list_items/2`, `set_items/2`
    and `array_items/2`, and the fluent syntax (`X := $math.sqrt(2)`, `Obj.method(Args)`,
    `Obj.attribute := Value`, `X := (V) as T`). See `tuprolog.solve.libs` for a guide.

    Unlike 2P-Kt's OOPLib, any term is a valid receiver (e.g. `X := hello.upper`), atom methods call
    routines and read other attributes, and calls take keyword arguments as `Key = Value`. As Python
    dispatches calls by value, there is no overload selection (`invoke_strict/3` is missing), and
    `as` converts values by calling types (e.g. `X := ('42') as $int`).

    Args:
        allow_all_imports: whether any module can be imported (by `type/2`, as `$sys` and
            `$system`), and all built-ins be used (e.g. `eval`, `open`); by default, only the
            modules in `SAFE_MODULES`, and the built-ins giving no access to code execution, files,
            or arbitrary attributes.
        allow_private: whether private attributes (whose names start with `_`) are accessible.
        aliases: further aliases, from names to objects (e.g. `{"point": Point}` makes `$point`
            denote `Point`), overriding the default ones.

    Returns:
        The library, aliased `prolog.oop.python`.

    Note:
        `allow_all_imports` and `allow_private` limit what Prolog code can reach, without
        sandboxing it: do not run untrusted Prolog code with this library.

    Examples:
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> solver = prolog_solver(libraries=oop_lib(aliases={"answer": 42}))
        >>> list(solver.query("alias(answer, A), B := A.bit_length"))
        [{'A': 42, 'B': 6}]
        >>> solver.solve_once("catch(type(os, T), error(E, _), true)")["E"]
        existence_error(oop_alias, os)
        >>> solver = prolog_solver(libraries=oop_lib(allow_all_imports=True))
        >>> list(solver.query("type('os.path', P), X := P.basename('/a/b.txt')"))
        [{'P': '<module:...>', 'X': 'b.txt'}]
    """
    objects = _PythonObjects(allow_all_imports, allow_private, aliases)

    def type_(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        name, result = args
        if not isinstance(name, Atom):
            raise _type_error(0, "atom", name)
        yield _unify(request, (result, objects.reference(objects.resolve_type(str(name.value)))))

    def new_object(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        type_term, arguments, result = args
        constructor = objects.type_value(type_term, 0)
        if not callable(constructor):
            raise _type_error(0, "type_reference", type_term)
        values, kwargs = objects.arguments(_items(arguments, 1), 1)
        yield _unify(request, (result, objects.term(constructor(*values, **kwargs))))

    def invoke_method(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        receiver, method, result = args
        value = objects.invoke(objects.value(receiver, 0), method, 1)
        yield _unify(request, (result, objects.term(value)))

    def assign(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        receiver, name, value = args
        if not isinstance(name, Atom):
            raise _type_error(1, "atom", name)
        target = objects.value(receiver, 0)
        objects.attribute(target, str(name.value), 1)  # checks permissions
        setattr(target, str(name.value), objects.value(value, 2))
        yield request.reply_success()

    def cast(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        value, type_term, result = args
        target = objects.type_value(type_term, 1)
        if not isinstance(target, type):
            raise _type_error(1, "type_reference", type_term)
        yield _unify(request, (result, objects.term(target(objects.value(value, 0)))))

    def register(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        value, alias = args
        if not isinstance(alias, Atom):
            raise _type_error(1, "atom", alias)
        if str(alias.value) in objects.registered:
            raise _Failure(
                lambda r: permission_error(
                    r.context, r.signature, operation("add_alias"), permission_type("flag"), alias
                )
            )
        objects.registered[str(alias.value)] = objects.value(value, 0)
        yield request.reply_success()

    def unregister(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        [alias] = args
        if not isinstance(alias, Atom):
            raise _type_error(0, "atom", alias)
        removed = objects.registered.pop(str(alias.value), _MISSING) is not _MISSING
        yield request.reply_success() if removed else request.reply_fail()

    def alias(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        name, reference = args
        for alias_name, value in objects.aliases():
            response = _unify(request, (name, atom(alias_name)), (reference, objects.term(value)))
            if response.solution.is_yes:
                yield response

    def checking(test: Callable[[Term], bool]) -> Callable:
        def check(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
            yield request.reply_success() if test(args[0]) else request.reply_fail()

        return check

    def is_type(term: Term) -> bool:
        return objects.is_reference(term) and isinstance(objects.referenced(term), type)

    def null_ref(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        yield _unify(request, (args[0], NULL_REF))

    def items(request: SolveRequest, args: list[Term]) -> Iterator[SolveResponse]:
        collection, result = args
        values = objects.value(collection, 0)
        if not isinstance(values, Iterable) or isinstance(values, (str, bytes)):
            raise _type_error(0, "object_reference", collection)
        yield _unify(request, (result, logic_list([objects.term(v) for v in values])))

    primitives = {
        "type/2": type_,
        "new_object/3": new_object,
        "invoke_method/3": invoke_method,
        "assign/3": assign,
        "cast/3": cast,
        "register/2": register,
        "unregister/1": unregister,
        "alias/2": alias,
        "ref/1": checking(objects.is_reference),
        "object_ref/1": checking(
            lambda t: objects.is_reference(t) and t != NULL_REF and not is_type(t)
        ),
        "type_ref/1": checking(is_type),
        "null_ref/1": null_ref,
        "list_items/2": items,
        "set_items/2": items,
        "array_items/2": items,
    }
    return library(
        "prolog.oop.python",
        primitives={signature(key): _primitive(value) for key, value in primitives.items()},
        clauses=ClausesParser.withOperators(DEFAULT_OPERATORS + OPERATORS).parse_clauses(CLAUSES),
        operators=OPERATORS,
    )


_MISSING = object()


def _items(term: Term, index: int) -> list[Term]:
    if isinstance(term, Var):
        raise _Failure(
            lambda r: instantiation_error_for_argument(r.context, r.signature, term, index)
        )
    converted = to_python(term)
    if not isinstance(converted, list):
        raise _type_error(index, "list", term)
    return list(term)


OOPLib: Library = oop_lib()
"""The default instance of OOPLib, i.e. `oop_lib()` (alias `prolog.oop.python`).

Restricted to `SAFE_MODULES` and public attributes; see `tuprolog.solve.libs` for a guide to its
use from Prolog, and `oop_lib` to customize it.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> list(prolog_solver(libraries=OOPLib).query("X := 'a,b'.split(','), list_items(X, I)"))
    [{'X': '<object:list#...>', 'I': ['a', 'b']}]
"""
