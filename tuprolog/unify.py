import logging
import jpype
import jpype.imports

from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap




logging.debug("Loaded JVM classes from it.unibo.tuprolog.unify.*")