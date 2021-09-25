from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Append
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Arrow
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import CurrentPrologFlag
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Member
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Not
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Once
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Semicolon
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import SetPrologFlag


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.rule.*")
