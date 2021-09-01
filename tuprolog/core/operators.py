import logging
import jpype
import jpype.imports

from it.unibo.tuprolog.core.operators import Operator
from it.unibo.tuprolog.core.operators import OperatorSet
from it.unibo.tuprolog.core.operators import Specifier

from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import jiterable, jmap

logging.debug("Loaded JVM classes from it.unibo.tuprolog.core.operators.*")
    