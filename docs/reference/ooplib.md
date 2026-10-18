# OOPLib

`OOPLib` ([`tuprolog.solve.libs`](../api/tuprolog/solve/libs.md), alias `prolog.oop.python`) lets
Prolog code create Python objects, call their methods, and read or assign their attributes. It
offers the Prolog API of 2P-Kt's OOPLib, over Python objects instead of JVM ones. Solvers do not
load it by default: pass `OOPLib` (or a customized instance, built by `oop_lib`) to the solver
factory.

```pycon
>>> from tuprolog.solve.libs import OOPLib
>>> from tuprolog.solve.prolog import prolog_solver
>>> solver = prolog_solver(libraries=OOPLib)
>>> list(solver.query("X := $math.sqrt(16)"))
[{'X': 4.0}]
>>> list(solver.query("new_object($list, [], L), L.append(a), L.append(b), list_items(L, Items)"))
[{'L': '<object:list#...>', 'Items': ['a', 'b']}]

```

## Values and references

- **Arguments** of calls are converted from terms to Python values (see
  [Python–term conversions](python-term-conversions.md)): atoms become strings, numbers numbers,
  lists lists, and so on. References and aliases (below) stand for their objects, also inside
  lists. An argument `Key = Value` is a keyword argument.
- **Results** that are numbers, booleans or strings become terms; any other object becomes a
  **reference**: an atom denoting the object, e.g. `'<object:list#7f...>'`,
  `'<type:builtins.int>'`, `'<module:math>'`. `None` becomes `'<null>'` (`NULL_REF`), and
  `'<null>'` in arguments becomes `None`.

The library keeps the objects it has given references to alive, for as long as the library
exists.

## Operators

| Operator | Type, priority | Use |
|---|---|---|
| `.` | `xfy`, 800 | `Receiver.method(Args)`, `Receiver.attribute`: calls and attribute access |
| `:=` | `xfx`, 850 | `Result := Expression`: evaluation; `Receiver.attribute := Value`: assignment |
| `as` | `xfx`, 200 | `(Expression) as Type`: conversion, by calling the type |
| `$` | `fx`, 100 | `$Name`: an alias |

| Goal | Meaning |
|---|---|
| `Result := Receiver.method(Args)` | call a method, binding its result |
| `Result := Receiver.attribute` | read an attribute (calling it, if it is a method taking no arguments) |
| `Result := Receiver.m1(A).m2(B)` | chained calls |
| `Receiver.method(Args)` | call a method, discarding its result |
| `Receiver.attribute := Value` | assign an attribute |
| `Result := (Expression) as Type` | convert a value, e.g. `X := ('42') as $int` |

Any term is a valid receiver: e.g. `X := hello.upper` calls `"hello".upper()`.
Parenthesize calls on the left of `as`, which binds tighter than `.`.

```pycon
>>> list(solver.query("X := hello.upper, Y := ('42') as $int, Z := $json.dumps([1, 2], indent = 0)"))
[{'X': 'HELLO', 'Y': 42, 'Z': '[\n1,\n2\n]'}]

```

`X := $alias` alone does not resolve the alias (`X` is bound to the term `$alias`): use
`alias/2`, or call something on it. `$name(Args)` is not a call either: use
`$builtins.name(Args)`, or `new_object/3` for types.

## Aliases

`$Name` denotes a well-known object:

| Aliases | Objects |
|---|---|
| `$str`, `$int`, `$float`, `$bool`, `$list`, `$tuple`, `$dict`, `$set`, `$frozenset`, `$range`, `$complex`, `$bytes`, `$object` | Python's built-in types |
| `$string`, `$char`, `$integer`, `$long`, `$short`, `$byte`, `$double`, `$boolean`, `$array`, `$arraylist`, `$map`, `$hashmap`, `$any`, `$nothing`, `$big_integer`, `$big_decimal` | the same types (or `decimal.Decimal`, `NoneType`), under 2P-Kt's OOPLib names |
| `$builtins` | Python's built-in functions, e.g. `$builtins.len(L)` |
| `$stdin`, `$stdout`, `$stderr` | Python's current standard streams |
| `$math`, `$json`, `$re`, ... | the standard modules in `SAFE_MODULES`: `bisect`, `calendar`, `cmath`, `collections`, `copy`, `datetime`, `decimal`, `difflib`, `enum`, `fractions`, `functools`, `heapq`, `itertools`, `json`, `math`, `random`, `re`, `statistics`, `string`, `textwrap`, `time`, `unicodedata`, `uuid` |
| others | objects registered by `register/2`, and those given to `oop_lib(aliases=...)` |

## Predicates

| Predicate | Meaning |
|---|---|
| `type(Name, Type)` | the type named `Name`, e.g. `type('collections.Counter', T)` |
| `new_object(Type, Args, Object)`, `new_object(Type, Object)` | create an object, calling a type with arguments (or none) |
| `invoke_method(Receiver, Method, Result)` | call `Method` (an atom, e.g. `upper`, or a compound term, e.g. `append(a)`) on `Receiver` |
| `assign(Receiver, Attribute, Value)` | assign an attribute |
| `cast(Value, Type, Result)` | convert a value by calling a type |
| `register(Object, Alias)`, `unregister(Alias)` | add and remove aliases |
| `alias(Name, Object)` | the object of an alias, or enumerate aliases |
| `ref(Term)`, `object_ref(Term)`, `type_ref(Term)` | check that a term is a reference, to an object, to a type |
| `null_ref(Ref)` | the reference to `None` |
| `list_items(Collection, Items)`, `set_items(...)`, `array_items(...)` | the items of a collection, as a Prolog list |

```pycon
>>> goal = "type('fractions.Fraction', F), new_object(F, [1, 3], X), D := X.denominator"
>>> list(solver.query(goal))
[{'F': '<type:fractions.Fraction>', 'X': '<object:Fraction#...>', 'D': 3}]

```

Unlike 2P-Kt's OOPLib, there is no overload selection (`invoke_strict/3`): Python dispatches calls
by value.

## Errors

| Situation | Error |
|---|---|
| unknown alias or type | `existence_error(oop_alias, Name)` |
| missing attribute or method | `existence_error(oop_method, Name)` |
| private attribute (`_name`), unless allowed | `permission_error(access, oop_method, Name)` |
| unbound argument where a value is needed | `instantiation_error` |
| exception raised by Python code | `system_error` |

## Customization and safety

`oop_lib(allow_all_imports=False, allow_private=False, aliases=None)` builds a customized library:

| Option | Default behaviour | When enabled |
|---|---|---|
| `allow_all_imports` | only the modules in `SAFE_MODULES` are importable (by `type/2` or as aliases), and built-ins giving access to code execution, files or arbitrary attributes (`eval`, `exec`, `compile`, `open`, `getattr`, `setattr`, `__import__`, ...) are unavailable | any module (also as `$sys` and `$system`), and every built-in |
| `allow_private` | attributes whose names start with `_` are not accessible | they are |
| `aliases` | — | further aliases, from names to objects, e.g. `{"point": Point}` makes `$point` denote `Point` |

```pycon
>>> from tuprolog.solve.libs import oop_lib
>>> class Point:
...     def __init__(self, x, y):
...         self.x, self.y = x, y
>>> solver = prolog_solver(libraries=oop_lib(aliases={"point": Point}))
>>> list(solver.query("new_object($point, [3, 4], P), P.x := 6, X := P.x"))
[{'P': '<object:Point#...>', 'X': 6}]

```

!!! warning
    These limits restrict what Prolog code can reach, but they are not a sandbox: do not run
    untrusted Prolog code with OOPLib.

## See also

- [Use Python objects from Prolog](../how-to/use-python-objects-from-prolog.md), a practical guide.
- 2P-Kt's [libraries](https://tuprolog.github.io/2p-kt/reference/libraries/) reference.
