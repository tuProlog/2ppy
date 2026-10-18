"""Ready-made libraries for Prolog code: streams and I/O (`IOLib`), and Python objects (`OOPLib`).

Libraries add predicates to solvers (see `tuprolog.solve.library`): pass them to the solver
factories, e.g. `prolog_solver(libraries=OOPLib)`, or several at once with
`tuprolog.solve.library.libraries(IOLib, OOPLib)`.

## IOLib: streams and I/O

`IOLib` (alias `prolog.io`) is 2P-Kt's library of ISO Prolog stream predicates. A **stream** is a
source of characters to read or a sink to write characters to, denoted by a term
(`'$stream'(...)`) or by an alias atom; the *current* input and output streams are the solver's
standard input and output (`user_input`, `user_output`), which are Python's `sys.stdin` and
`sys.stdout` unless given to the solver factory (`std_in=`, `std_out=`, e.g. `io.StringIO`s).

- streams: `open/3,4` (`open(Source, Mode, Stream)`, with `Mode` `read`, `write` or `append`,
  `Source` a file path or URL, and options such as `alias(A)`), `close/1`, `current_input/1`,
  `current_output/1`, `set_input/1`, `set_output/1`, `stream_property/2`, `at_end_of_stream/0,1`,
  `flush_output/1`;
- characters: `get_char/1,2`, `get_code/1,2` (reading `end_of_file` / `-1` at the end),
  `peek_char/1,2`, `peek_code/1,2` (without consuming), `put_char/1,2`, `put_code/1,2`, `nl/1`;
- terms: `read/1,2` (failing, rather than reading `end_of_file`, at the end of the stream),
  `read_term/2,3`, `write/2`, `writeq/1,2` (quoting atoms where needed), `write_canonical/1,2`
  (quoting, and ignoring operators), `write_term/2,3` (with options `quoted(B)`, `ignore_ops(B)`,
  `numbervars(B)`);
- theories: `consult/1` (loading the clauses of a file or URL), `set_theory/1` (replacing the
  knowledge base with the clauses in an atom).

Binary streams are not supported: `get_byte/1,2`, `put_byte/1,2`, `peek_byte/1,2`, `close/2`,
`char_conversion/2` and `current_char_conversion/2` raise a `system_error`. Writing is only
possible on local files.

## OOPLib: Python objects from Prolog

`OOPLib` (alias `prolog.oop.python`) lets Prolog code create Python objects, call their methods,
and read or change their attributes, as 2P-Kt's OOPLib does with JVM objects. Build a
customized instance with `oop_lib`.

**Values.** Arguments of calls are converted from terms to Python values (see
`tuprolog.core.to_python`: e.g. atoms become strings, lists lists, `Key = Value` arguments
keyword arguments); results that are numbers, booleans or strings become terms, any other object
a **reference**: an atom denoting the object, e.g. `'<object:list#7f...>'`, `'<type:builtins.int>'`,
`'<module:math>'`, or `'<null>'` (`NULL_REF`) for `None`. References in arguments, even inside
lists, stand for their objects.

**Aliases.** `$Name` denotes a well-known object: Python built-in types (also by OOPLib's names,
e.g. `$string`, `$arraylist`, `$hashmap`, `$double`), `$builtins` (the built-in functions, e.g.
`$builtins.len(L)`), `$stdin`, `$stdout`, `$stderr`, the standard modules in `SAFE_MODULES` (e.g.
`$math`, `$json`, `$re`), objects registered by `register/2`, and those given to `oop_lib`.

**Syntax.** The library adds the operators `.` (`xfy`, 800: calls), `:=` (`xfx`, 850:
evaluation and assignment), `as` (`xfx`, 200: conversion), and `$` (`fx`, 100: aliases):

- `Result := Receiver.method(Args)` calls a method, `Result := Receiver.attribute` reads an
  attribute (calling it, if it is a method taking no arguments); calls can be chained, e.g.
  `X := $math.sqrt(16).is_integer`; any term is a valid receiver, e.g. `X := hello.upper`;
- `Receiver.method(Args)` alone calls a method, discarding its result;
- `Receiver.attribute := Value` assigns an attribute;
- `Result := (Expression) as Type` converts the result by calling the type, e.g.
  `X := ('42') as $int` (parenthesize calls, as `as` binds tighter than `.`).

`X := $alias` alone does not resolve the alias (`X` is bound to the term `$alias`): use
`alias/2`, or call something on it. `$name(Args)` is not a call either: use
`$builtins.name(Args)`, or `new_object/3` for types.

**Predicates.** `type(Name, Type)` (a type by name, e.g. `'collections.Counter'`),
`new_object(Type, Args, Object)` and `new_object(Type, Object)`, `invoke_method(Receiver,
Method, Result)`, `assign(Receiver, Attribute, Value)`, `cast(Value, Type, Result)`,
`register(Object, Alias)` and `unregister(Alias)`, `alias(Name, Object)` (enumerating aliases),
`ref/1`, `object_ref/1`, `type_ref/1` (checking references), `null_ref(Ref)`, and
`list_items/2`, `set_items/2`, `array_items/2` (the items of a collection, as a Prolog list).
Unlike 2P-Kt's, there is no overload selection (`invoke_strict/3`), as Python dispatches calls
by value.

**Errors.** Unknown aliases or types raise `existence_error(oop_alias, Name)`, missing attributes
`existence_error(oop_method, Name)`, private attributes `permission_error(access, oop_method,
Name)`, and exceptions raised by Python code a `system_error` (see
`tuprolog.solve.exception.error`).

**Safety.** By default only the modules in `SAFE_MODULES` can be imported (by `type/2` or as
aliases), built-ins giving access to code execution or files (e.g. `eval`, `open`, `getattr`)
are not available, and private attributes (`_name`) are not accessible: `oop_lib`'s
`allow_all_imports` and `allow_private` lift these limits. They limit what Prolog code can reach,
but are not a sandbox: do not run untrusted Prolog code with this library.

Examples:
    Reading and writing terms on in-memory streams with `IOLib`:

    >>> import io
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> output = io.StringIO()
    >>> solver = prolog_solver(
    ...     libraries=IOLib, std_in=io.StringIO("foo(bar). 'hello world'."), std_out=output
    ... )
    >>> list(solver.query("read(X), read(Y), current_output(S), write(S, X), nl(S), writeq(S, Y)"))
    [{'X': foo(bar), 'Y': 'hello world', 'S': '$stream'(out, ...)}]
    >>> print(output.getvalue())
    foo(bar)
    'hello world'

    Using Python objects with `OOPLib`:

    >>> solver = prolog_solver(libraries=OOPLib)
    >>> list(solver.query("X := $math.sqrt(16)"))
    [{'X': 4.0}]
    >>> list(solver.query("X := $json.dumps([1, 2], indent = 0)"))
    [{'X': '[\\n1,\\n2\\n]'}]
    >>> list(solver.query("new_object($list, [], L), L.append(a), L.append(b), list_items(L, I)"))
    [{'L': '<object:list#...>', 'I': ['a', 'b']}]
    >>> goal = "type('fractions.Fraction', F), new_object(F, [1, 3], X), D := X.denominator"
    >>> list(solver.query(goal))
    [{'F': '<type:fractions.Fraction>', 'X': '<object:Fraction#...>', 'D': 3}]
    >>> list(solver.query("X := ('42') as $int"))
    [{'X': 42}]

    Exposing Python objects of your own, as aliases:

    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    ...     def norm(self):
    ...         return (self.x**2 + self.y**2) ** 0.5
    >>> solver = prolog_solver(libraries=oop_lib(aliases={"point": Point}))
    >>> list(solver.query("new_object($point, [3, 4], P), N := P.norm, P.x := 6, X := P.x"))
    [{'P': '<object:Point#...>', 'N': 5.0, 'X': 6}]

See Also:
    `tuprolog.solve.library`, to combine libraries and write new ones;
    `tuprolog.solve.primitive`, to write predicates in Python;
    2P-Kt's [I/O library](https://tuprolog.github.io/2p-kt/reference/io-lib/) and
    [libraries](https://tuprolog.github.io/2p-kt/reference/libraries/).
"""

from ._api import *
from ._definitions import *

__all__ = ["NULL_REF", "SAFE_MODULES", "IOLib", "OOPLib", "oop_lib"]
