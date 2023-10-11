from tuprolog import logger
from tuprolog.jvmutils import Pair
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.flags as _flags  # type: ignore


DoubleQuotes = _flags.DoubleQuotes


FlagStore = _flags.FlagStore


LastCallOptimization = _flags.LastCallOptimization


MaxArity = _flags.MaxArity


NotableFlag = _flags.NotableFlag


TrackVariables = _flags.TrackVariables


Unknown = _flags.Unknown


Flag = Pair


EMPTY_FLAG_STORE: FlagStore = FlagStore.EMPTY


DEFAULT_FLAG_STORE: FlagStore = FlagStore.DEFAULT


DoubleQuotes: NotableFlag = DoubleQuotes.INSTANCE


LastCallOptimization: NotableFlag = LastCallOptimization.INSTANCE


MaxArity: NotableFlag = MaxArity.INSTANCE


TrackVariables: NotableFlag = TrackVariables.INSTANCE


Unknown: NotableFlag = Unknown.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.flags.*")
