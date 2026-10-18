"""2PPy: tuProlog in Python, a logic-programming ecosystem for symbolic AI.

2PPy lets Python programs represent logic knowledge, reason over it, and extend the reasoners with
Python code. It wraps [2P-Kt](https://github.com/tuProlog/2p-kt), a Kotlin implementation of
tuProlog, running it on a Java Virtual Machine (JVM) started when `tuprolog` is first imported:
no separate Java installation is needed, as the JVM comes with the `jdk4py` dependency.

Logic programming in a nutshell: data are *terms* (e.g. the atom `bart`, the variable `X`, or the
compound term `parent(homer, bart)`); knowledge is a *theory*, i.e. a sequence of *clauses*, as
the fact `parent(homer, bart).` or the rule `grandparent(X, Z) :- parent(X, Y), parent(Y, Z).`;
reasoning means *solving* a query (e.g. `grandparent(abe, Who)`) against a theory, finding the
values of the query variables making it true, by *unification* and *resolution*.

The package is organized in sub-packages, mirroring 2P-Kt's modules:

- `tuprolog.core`: terms (atoms, numbers, variables, structures, lists, clauses), substitutions,
  and their formatting; `tuprolog.core.operators` and `tuprolog.core.parsing` deal with operators
  and with parsing terms from text.
- `tuprolog.unify`: unification of terms.
- `tuprolog.theory` (and `tuprolog.theory.parsing`): theories, i.e. indexed clause databases.
- `tuprolog.collections`: other indexed collections of clauses (queues and multi-sets).
- `tuprolog.solve`: the solver API (queries, solutions, libraries, primitives, flags, errors),
  with `tuprolog.solve.prolog` (ISO Prolog solvers) and `tuprolog.solve.problog` (probabilistic
  ProbLog solvers).
- `tuprolog.errors`: Python exception classes classifying 2P-Kt's exceptions.
- `tuprolog.repl`: interactive read-eval-print loops (`python -m tuprolog.repl.prolog`).
- `tuprolog.math`: arbitrary-precision numbers, as used by numeric terms.

Python values are converted to terms (and back) where convenient, and JVM methods are also callable
with Python-style names (see `tuprolog.jvmutils`).

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> from tuprolog.theory.parsing import parse_theory
    >>> solver = prolog_solver(static_kb=parse_theory("parent(abe, homer). parent(homer, bart)."))
    >>> list(solver.query("parent(X, bart)"))
    [{'X': 'homer'}]

See Also:
    2P-Kt's documentation: <https://tuprolog.github.io/2p-kt/>.
"""

import logging
from importlib.metadata import version

import jpype

from .libs import CLASSPATH, find_jvm

__version__ = version("2ppy")  # pyproject.toml is the only source
"""The version of 2PPy, e.g. `"1.5.0"`."""

logger = logging.getLogger("tuprolog")
"""The logger of 2PPy (named `"tuprolog"`), reporting e.g. the JVM startup and the classpath."""

jars = [str(j.resolve()) for j in CLASSPATH.glob("*.jar")]
"""The absolute paths of the JARs (2P-Kt and its dependencies) on the JVM's classpath."""

if not jpype.isJVMStarted():
    jpype.startJVM("--enable-native-access=ALL-UNNAMED", classpath=jars, jvmpath=str(find_jvm()))

import jpype.imports
from it.unibo import tuprolog as _tuprolog  # type: ignore

Info = _tuprolog.Info
"""Information about the running 2P-Kt, e.g. `Info.VERSION`, the version of 2P-Kt.

Note:
    The JVM class `it.unibo.tuprolog.Info` of 2P-Kt.
"""

JVM_VERSION = ".".join(map(str, jpype.getJVMVersion()))
"""The version of the JVM 2PPy runs on, e.g. `"21.0.8"`."""

logger.info("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

logger.info("Using 2P-Kt v" + str(Info.VERSION))

from . import errors
