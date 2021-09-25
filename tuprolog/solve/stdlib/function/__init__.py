from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import AbsoluteValue
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Addition
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import ArcTangent
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import BitwiseAnd
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import BitwiseComplement
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import BitwiseLeftShift
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import BitwiseOr
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import BitwiseRightShift
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Ceiling
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Cosine
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Exponential
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Exponentiation
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import FloatFractionalPart
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import FloatIntegerPart
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import FloatingPointDivision
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Floor
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import IntegerDivision
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Modulo
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Multiplication
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import NaturalLogarithm
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Remainder
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Round
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Sign
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import SignReversal
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Sine
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import SquareRoot
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Subtraction
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import ToFloat
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.function import Truncate


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.function.*")
