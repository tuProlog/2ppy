# Use Python objects from Prolog

OOPLib (`tuprolog.solve.libs.OOPLib`) lets Prolog code create Python objects, call their methods,
and read or assign their attributes. This guide shows the common tasks; the
[OOPLib reference](../reference/ooplib.md) lists all its predicates and operators.

## Load the library

Pass `OOPLib` to the solver (combine it with other libraries via
`tuprolog.solve.library.libraries`):

```pycon
>>> from tuprolog.solve.libs import OOPLib
>>> from tuprolog.solve.prolog import prolog_solver
>>> solver = prolog_solver(libraries=OOPLib)

```

## Call functions and methods

`Result := Receiver.method(Args)` calls a method and binds its result. `$name` denotes a well-known
object, such as a safe standard module (`$math`, `$json`, `$re`, ...), a built-in type (`$list`,
`$dict`, `$str`, ...), or `$builtins`:

```pycon
>>> list(solver.query("X := $math.sqrt(16)"))
[{'X': 4.0}]
>>> list(solver.query("X := $builtins.len([a, b, c])"))
[{'X': 3}]
>>> list(solver.query("X := hello.upper"))  # any term is a receiver; no-argument calls need no ()
[{'X': 'HELLO'}]
>>> list(solver.query("X := $json.dumps([1, 2], indent = 0)"))  # keyword arguments as Key = Value
[{'X': '[\n1,\n2\n]'}]

```

Arguments are converted from terms into Python values (atoms become strings, lists lists, ...).
Results that are numbers, booleans or strings become terms.

## Create objects and keep references

Other results become *references*: atoms denoting the objects, which later calls accept in their
place. `new_object(Type, Args, Object)` creates an object; `Receiver.method(Args)` alone calls a
method, discarding its result:

```pycon
>>> goal = "new_object($list, [[c, a, b]], L), L.sort, L.append(d), list_items(L, Items)"
>>> list(solver.query(goal))
[{'L': '<object:list#...>', 'Items': ['a', 'b', 'c', 'd']}]
>>> list(solver.query("new_object($dict, [], D), D.update(a = 1), X := D.get(a)"))
[{'D': '<object:dict#...>', 'X': 1}]

```

`list_items/2`, `set_items/2` and `array_items/2` turn collections into Prolog lists.

## Read and assign attributes

```pycon
>>> list(solver.query("type('fractions.Fraction', F), new_object(F, [1, 3], X), D := X.denominator"))
[{'F': '<type:fractions.Fraction>', 'X': '<object:Fraction#...>', 'D': 3}]

```

`Receiver.attribute := Value` assigns an attribute (see the next section for an example).

## Convert values

`Result := (Expression) as Type` converts a value by calling a type:

```pycon
>>> list(solver.query("X := ('42') as $int"))
[{'X': 42}]

```

## Expose your own objects

`oop_lib(aliases={...})` builds an OOPLib instance where your objects and types have aliases:

```pycon
>>> from tuprolog.solve.libs import oop_lib
>>> class Point:
...     def __init__(self, x, y):
...         self.x, self.y = x, y
...
...     def norm(self):
...         return (self.x**2 + self.y**2) ** 0.5
>>> solver = prolog_solver(libraries=oop_lib(aliases={"point": Point}))
>>> list(solver.query("new_object($point, [3, 4], P), N := P.norm, P.x := 6, X := P.x"))
[{'P': '<object:Point#...>', 'N': 5.0, 'X': 6}]

```

Prolog code can also register aliases with `register(Object, Alias)`:

```pycon
>>> list(solver.query("new_object($point, [1, 1], P), register(P, origin), X := $origin.x"))
[{'P': '<object:Point#...>', 'X': 1}]

```

## Lift the safety limits

By default only side-effect free standard modules can be imported (by `type/2` or as aliases),
built-ins giving access to code execution or files (`eval`, `open`, ...) are unavailable, and
private attributes (`_name`) are not accessible:

```pycon
>>> solver = prolog_solver(libraries=OOPLib)
>>> solver.solve_once("type('os', T)").exception.type
existence_error(oop_alias, os)
>>> solver.solve_once("X := hello.'__len__'").exception.type
permission_error(access, oop_method, '__len__')

```

`oop_lib(allow_all_imports=True, allow_private=True)` lifts these limits:

```pycon
>>> solver = prolog_solver(libraries=oop_lib(allow_all_imports=True, allow_private=True))
>>> list(solver.query("type('os.path', P), X := P.basename('/tmp/kb.pl')"))
[{'P': '<module:...path>', 'X': 'kb.pl'}]
>>> list(solver.query("X := hello.'__len__'"))
[{'X': 5}]

```

!!! warning
    These limits restrict what Prolog code can reach, but they are not a sandbox: do not run
    untrusted Prolog code with OOPLib.

## See also

- [OOPLib reference](../reference/ooplib.md).
- API: `tuprolog.solve.libs` ([reference](../api/tuprolog/solve/libs.md)).
