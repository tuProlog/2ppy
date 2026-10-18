# Python–term conversions

Logic programs manipulate **terms** (see [Terms and variables](../explanation/terms-and-variables.md));
Python programs manipulate Python values. 2PPy converts between the two with
[`tuprolog.core.to_term`](../api/tuprolog/core.md) and [`tuprolog.core.to_python`](../api/tuprolog/core.md),
and applies them automatically at most places where the two worlds meet.

## From Python to terms: `to_term`

| Python value | Term | Example |
|---|---|---|
| a term | the term itself | `to_term(atom("a"))` is `a` |
| `str` | atom | `"bart"` → `bart`, `"Hello World"` → `'Hello World'` |
| `bool` | truth | `True` → `true`, `False` → `false` |
| `int` (any size) | integer | `42` → `42`, `10**30` → `1000000000000000000000000000000` |
| `float` | real, from the float's shortest representation | `0.1` → `0.1` |
| `decimal.Decimal` | real, without trailing zeros | `Decimal("1.50")` → `1.5` |
| `list` | logic list, items converted | `[1, "a"]` → `[1, a]` |
| `tuple` of 2+ items | logic tuple (conjunction), items converted | `(1, "a")` → `(1, a)` |
| 1-tuple | its item, converted | `("a",)` → `a` |

Anything else (`None`, dicts, sets, the empty tuple, arbitrary objects) raises `TypeError`.
Note that strings always become atoms: to get a variable, create one with `var("X")` (or parse
text with `tuprolog.core.parsing.parse_term`).

```pycon
>>> from decimal import Decimal
>>> from tuprolog.core import atom, to_term
>>> to_term("bart"), to_term("Hello World"), to_term(True), to_term(42), to_term(0.1)
(bart, 'Hello World', true, 42, 0.1)
>>> to_term(Decimal("1.50")), to_term(10**30)
(1.5, 1000000000000000000000000000000)
>>> to_term([1, "a", (2, 3)]), to_term(("a",))
([1, a, (2, 3)], a)
>>> to_term(None)
Traceback (most recent call last):
    ...
TypeError: Cannot convert NoneType into a term: None

```

## From terms to Python: `to_python`

| Term | Python value | Example |
|---|---|---|
| truth (`true`, `false`, `fail`) | `bool` | `true` → `True`, `fail` → `False` |
| integer | `int` | `42` → `42` |
| real | `float` (possibly losing precision) | `2.5` → `2.5` |
| well-formed list (incl. `[]`) | `list`, items converted | `[1, a]` → `[1, 'a']`, `[]` → `[]` |
| tuple | `tuple`, items converted | `(1, a)` → `(1, 'a')` |
| other atom | `str` | `bart` → `'bart'` |
| anything else (variables, compound terms, partial lists like `[1 \| T]`) | the term itself | `f(a)` → `f(a)` |

```pycon
>>> from tuprolog.core import to_python
>>> from tuprolog.core.parsing import parse_term
>>> to_python(parse_term("[1, 2.5, a, true, (b, c)]"))
[1, 2.5, 'a', True, ('b', 'c')]
>>> to_python(parse_term("fail")), to_python(parse_term("[]"))
(False, [])
>>> to_python(parse_term("f(a)")), to_python(parse_term("[1 | T]"))
(f(a), [1 | T_...])

```

`to_python(to_term(v)) == v` holds for strings, booleans, ints, lists and tuples of them; floats
round-trip through their shortest representation, and `Decimal`s become `float`s.

## Where conversions happen automatically

| Where | Direction | What is converted |
|---|---|---|
| Term factories `struct`, `logic_list`, `logic_list_from`, `logic_tuple` (`tuprolog.core`) | Python → term | their arguments/items, e.g. `struct("f", "a", 1)` is `f(a, 1)` |
| Flags: `flag`, `flag_store`, `store + {...}` (`tuprolog.solve.flags`) | Python → term | flag values, e.g. `flag_store(unknown="fail")` |
| `Solver.query` and `Solution.to_dict` (`tuprolog.solve`) | term → Python | the bindings of the query's variables, e.g. `{'X': 1}` |
| `predicate` (`tuprolog.solve.primitive`) | both | the goal's arguments are passed through `to_python`; returned tuples of values are converted by `to_term` and unified with the arguments |
| `function` (`tuprolog.solve.function`) | both | the evaluated arguments through `to_python`, the result through `to_term` |
| [OOPLib](ooplib.md) | both | call arguments through `to_python` (references and `$aliases` stand for their objects, `Key = Value` gives keyword arguments); numbers, booleans and strings returned by Python become terms, other objects references (atoms like `'<object:list#...>'`) |

```pycon
>>> from tuprolog.core import struct
>>> from tuprolog.solve.prolog import prolog_solver
>>> struct("point", 1, 2.5, "origin")
point(1, 2.5, origin)
>>> list(prolog_solver().query("X = [1, a], Y = f(b), Z = (c, d)"))
[{'X': [1, 'a'], 'Y': f(b), 'Z': ('c', 'd')}]

```

`Solution.bindings` (and `solution[name]`) give the bound terms instead, unconverted.

Other factories take terms (or plain Python values only where documented, e.g. `atom` takes a
string, `integer` an `int`): check their docstrings in the [API reference](../api/tuprolog/core.md).
Methods of JVM objects that have no Pythonic counterpart take and return JVM values: JPype
converts Python `str`, `int`, `float` and `bool` to their JVM counterparts, and may return
`java.lang.String`s where 2P-Kt returns strings (use `str(...)` to get Python strings).
