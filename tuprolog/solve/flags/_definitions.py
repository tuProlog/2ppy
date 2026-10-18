import it.unibo.tuprolog.solve.flags as _flags  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger
from tuprolog.jvmutils import Pair

FlagStore = _flags.FlagStore


NotableFlag = _flags.NotableFlag


Flag = Pair


EMPTY_FLAG_STORE: FlagStore = FlagStore.EMPTY


DEFAULT_FLAG_STORE: FlagStore = FlagStore.DEFAULT


DoubleQuotes: NotableFlag = _flags.DoubleQuotes.INSTANCE


GroundQueriesHaveBooleanSolution: NotableFlag = _flags.GroundQueriesHaveBooleanSolution.INSTANCE


LastCallOptimization: NotableFlag = _flags.LastCallOptimization.INSTANCE


MaxArity: NotableFlag = _flags.MaxArity.INSTANCE


ShowWildCardVariablesInSolutions: NotableFlag = _flags.ShowWildCardVariablesInSolutions.INSTANCE


TrackVariables: NotableFlag = _flags.TrackVariables.INSTANCE


UniqueSolutions: NotableFlag = _flags.UniqueSolutions.INSTANCE


Unknown: NotableFlag = _flags.Unknown.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.flags.*")
