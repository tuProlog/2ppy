# Architecture

2PPy is a Python wrapper of [2P-Kt](https://github.com/tuProlog/2p-kt), the Kotlin implementation
of tuProlog. This page explains how the two are connected, and why 2PPy is built that way.

```text
 your Python code
        │   Pythonic API: snake_case factories, Python protocols, conversions, exceptions
        ▼
 tuprolog (2PPy)  ──────────── Python
        │   JPype: calls between Python and JVM objects, in the same process
        ▼
 2P-Kt JARs + 2PPy's adapters ── JVM (bundled by jdk4py)
```

## Write once, wrap elsewhere

The logic engine (terms, unification, parsing, theories, solvers, libraries) is written once, in
Kotlin, as 2P-Kt, and 2PPy wraps it. 2PPy re-implements nothing that 2P-Kt already provides: it
exposes 2P-Kt's objects to Python, and makes them comfortable to use from Python. This keeps the
behaviour of 2PPy identical to 2P-Kt's (and to tuProlog's other front ends), and lets 2PPy benefit
from every improvement of the engine. When 2P-Kt's API is awkward from Python, the fix goes either
in 2P-Kt itself, when it belongs there, or in a Kotlin adapter of 2PPy: the `jvm/` directory of the
repository is a Gradle project declaring 2P-Kt's artifacts, and compiling the adapters 2PPy needs on
top of them (e.g. the facade `tuprolog.gui` wraps, hiding Kotlin coroutines behind callbacks and
futures), without changing 2P-Kt.

The price is a dependency on the Java virtual machine (JVM), which 2PPy makes invisible:

- the wheel ships 2P-Kt's JARs and 2PPy's adapters (in `tuprolog/libs/`);
- the [`jdk4py`](https://pypi.org/project/jdk4py/) dependency ships a Java runtime, so no Java
  installation is needed;
- [JPype](https://jpype.readthedocs.io) runs the JVM *inside* the Python process, so Python and
  JVM objects call each other directly, with no serialization or inter-process communication.

## The JVM lifecycle

Importing `tuprolog` (or any of its sub-packages) starts the JVM, with 2P-Kt's JARs on its class
path. This takes a second or two, once per process. JPype can start the JVM only once per
process, and it cannot be restarted after shutting down: all `tuprolog` objects in a process
share the same JVM.

```pycon
>>> import tuprolog
>>> str(tuprolog.Info.VERSION).split(".")[0], isinstance(tuprolog.JVM_VERSION, str)
('3', True)

```

`tuprolog.__version__` is 2PPy's version, `tuprolog.Info.VERSION` the version of 2P-Kt it wraps,
and `tuprolog.JVM_VERSION` the version of the JVM.

## JVM objects in Python

Terms, theories, solvers and solutions are JVM objects: JPype gives each JVM class a Python
proxy class, so they can be used as Python objects, with their JVM methods. 2PPy then makes them
Pythonic in four ways.

**Pythonic names.** Each sub-package re-exports the JVM types of a 2P-Kt module under their
Kotlin names (e.g. `tuprolog.core.Struct` is `it.unibo.tuprolog.core.Struct`), and adds factory
functions in `snake_case`, with default arguments and conversions of Python values (e.g.
`struct("f", "a", 1)` for 2P-Kt's `Struct.of("f", Atom.of("a"), Integer.of(1))`). Every JVM method
also gets a `snake_case` alias, and getters become properties: `getArity()` is also `arity`, and
`isGround()` is `is_ground`.

```pycon
>>> from tuprolog.core import struct
>>> term = struct("f", "a", 1)
>>> term.getArity(), term.arity, term.isGround(), term.is_ground
(2, 2, True, True)

```

**Python protocols.** 2PPy adds Python's protocols to the JVM types where they make sense:
iteration (lists, tuples, theories, sequences of solutions), `len`, indexing (`term[0]` for
arguments, `solution["X"]` for bindings), `in`, truthiness (`bool(solution)`), and operators
(`theory + clause`, `flags + {...}`, `runtime - alias`).

```pycon
>>> from tuprolog.core import logic_list
>>> items = logic_list(1, 2, 3)
>>> len(items), list(items), items[0]
(3, [1, 2, 3], 1)

```

**Conversions at the boundary.** Where Python code hands values to the engine, or gets values
back, 2PPy converts between Python values and terms (`to_term`, `to_python`): see
[Python–term conversions](../reference/python-term-conversions.md). Python streams
(`io.IOBase`) are adapted wherever 2P-Kt reads or writes, and Python functions can implement JVM
interfaces (e.g. a predicate written in Python is a 2P-Kt `Primitive`).

**Exceptions.** 2P-Kt's exceptions are JVM exceptions, raised in Python as they are; 2PPy makes
each of them also an instance of a class of `tuprolog.errors` and of a Python built-in exception
(e.g. a Prolog type error is a `TypeError`): see [Exceptions](../reference/exceptions.md).

Methods without a Pythonic counterpart remain available, as JVM methods: they may take or return
JVM types (e.g. `java.lang.String`, Kotlin sequences), which JPype converts where it can.

## Code layout

Each `tuprolog` sub-package corresponds to a 2P-Kt module (see
[Relationship with 2P-Kt](relationship-with-2p-kt.md)) and is split in three private modules,
re-exported by the package:

| Module | Content |
|---|---|
| `_definitions.py` | the JVM types and constants, re-exported under Pythonic names, each with a docstring |
| `_api.py` | the Pythonic factory functions (`snake_case`, defaults, varargs, conversions) |
| `_adapters.py` | the *customizers* (JPype's `@JImplementationFor`) adding Python members and protocols to JVM classes |

Cross-cutting bridges live in `tuprolog.jvmutils` (collections, iterables, functions, the
`snake_case` aliases) and `tuprolog.jvmioutils` (streams). Contributor notes are in
[`AGENTS.md`](https://github.com/tuProlog/2ppy/blob/master/AGENTS.md).

## Consequences

- Behaviour, including bugs and limitations, follows 2P-Kt's: the documentation points out the
  2P-Kt issues users may meet (e.g. missing predicates).
- Terms printed by Python are formatted by 2P-Kt, in Prolog syntax: `repr(term)` and `str(term)`
  both give Prolog text, with operators in canonical form except `:-` and `,` (e.g. `'+'(1, 2)`).
- Calls crossing the Python–JVM boundary have a cost: many small calls from Python (e.g. building
  large terms item by item) are slower than letting the engine do the work (e.g. parsing text, or
  solving in Prolog).
- The JVM's memory is managed separately from Python's: JPype keeps JVM objects alive while
  Python refers to them.
