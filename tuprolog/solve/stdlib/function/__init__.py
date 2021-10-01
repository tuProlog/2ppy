from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.stdlib.function as _function


AbsoluteValue = _function.AbsoluteValue.INSTANCE

Addition = _function.Addition.INSTANCE

ArcTangent = _function.ArcTangent.INSTANCE

BitwiseAnd = _function.BitwiseAnd.INSTANCE

BitwiseComplement = _function.BitwiseComplement.INSTANCE

BitwiseLeftShift = _function.BitwiseLeftShift.INSTANCE

BitwiseOr = _function.BitwiseOr.INSTANCE

BitwiseRightShift = _function.BitwiseRightShift.INSTANCE

Ceiling = _function.Ceiling.INSTANCE

Cosine = _function.Cosine.INSTANCE

Exponential = _function.Exponential.INSTANCE

Exponentiation = _function.Exponentiation.INSTANCE

FloatFractionalPart = _function.FloatFractionalPart.INSTANCE

FloatIntegerPart = _function.FloatIntegerPart.INSTANCE

FloatingPointDivision = _function.FloatingPointDivision.INSTANCE

Floor = _function.Floor.INSTANCE

IntegerDivision = _function.IntegerDivision.INSTANCE

Modulo = _function.Modulo.INSTANCE

Multiplication = _function.Multiplication.INSTANCE

NaturalLogarithm = _function.NaturalLogarithm.INSTANCE

Remainder = _function.Remainder.INSTANCE

Round = _function.Round.INSTANCE

Sign = _function.Sign.INSTANCE

SignReversal = _function.SignReversal.INSTANCE

Sine = _function.Sine.INSTANCE

SquareRoot = _function.SquareRoot.INSTANCE

Subtraction = _function.Subtraction.INSTANCE

ToFloat = _function.ToFloat.INSTANCE

Truncate = _function.Truncate.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.function.*")
