"""The functions of the standard library, evaluated in arithmetic expressions (e.g. by `is/2`).

Each constant is a `tuprolog.solve.function.LogicFunction` with a `signature` (its name and arity
in Prolog, e.g. `abs/1`), and is loaded by default in Prolog solvers. They are mostly ISO Prolog's
evaluable functors.

Examples:
    >>> AbsoluteValue.signature
    Signature(name=abs, arity=1, vararg=false)
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> prolog_solver().solve_once("X is abs(-3) + 7 mod 2")["X"]
    4
"""

import it.unibo.tuprolog.solve.stdlib.function as _function  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "AbsoluteValue",
    "Addition",
    "ArcTangent",
    "BitwiseAnd",
    "BitwiseComplement",
    "BitwiseLeftShift",
    "BitwiseOr",
    "BitwiseRightShift",
    "Ceiling",
    "Cosine",
    "Exponential",
    "Exponentiation",
    "FloatFractionalPart",
    "FloatIntegerPart",
    "FloatingPointDivision",
    "Floor",
    "IntegerDivision",
    "Modulo",
    "Multiplication",
    "NaturalLogarithm",
    "Remainder",
    "Round",
    "Sign",
    "SignReversal",
    "Sine",
    "SquareRoot",
    "Subtraction",
    "ToFloat",
    "Truncate",
]


AbsoluteValue = _function.AbsoluteValue.INSTANCE
"""The function `abs/1`: the absolute value of a number."""


Addition = _function.Addition.INSTANCE
"""The function `+/2`: the sum of two numbers."""


ArcTangent = _function.ArcTangent.INSTANCE
"""The function `atan/1`: the arc tangent of a number, in radians."""


BitwiseAnd = _function.BitwiseAnd.INSTANCE
"""The function `/\\/2`: the bitwise and of two integers."""


BitwiseComplement = _function.BitwiseComplement.INSTANCE
"""The function `\\/1`: the bitwise complement of an integer."""


BitwiseLeftShift = _function.BitwiseLeftShift.INSTANCE
"""The function `<</2`: an integer shifted left by a number of bits."""


BitwiseOr = _function.BitwiseOr.INSTANCE
"""The function `\\//2`: the bitwise or of two integers."""


BitwiseRightShift = _function.BitwiseRightShift.INSTANCE
"""The function `>>/2`: an integer shifted right by a number of bits."""


Ceiling = _function.Ceiling.INSTANCE
"""The function `ceiling/1`: the smallest integer not less than a number."""


Cosine = _function.Cosine.INSTANCE
"""The function `cos/1`: the cosine of an angle, in radians."""


Exponential = _function.Exponential.INSTANCE
"""The function `exp/1`: e raised to a number."""


Exponentiation = _function.Exponentiation.INSTANCE
"""The function `**/2`: a number raised to another, as a float."""


FloatFractionalPart = _function.FloatFractionalPart.INSTANCE
"""The function `float_fractional_part/1`: the fractional part of a number."""


FloatIntegerPart = _function.FloatIntegerPart.INSTANCE
"""The function `float_integer_part/1`: the integer part of a number, as a float."""


FloatingPointDivision = _function.FloatingPointDivision.INSTANCE
"""The function `//2`: the quotient of two numbers."""


Floor = _function.Floor.INSTANCE
"""The function `floor/1`: the largest integer not greater than a number."""


IntegerDivision = _function.IntegerDivision.INSTANCE
"""The function `///2`: the integer quotient of two integers, truncated towards zero."""


Modulo = _function.Modulo.INSTANCE
"""The function `mod/2`: the modulo of two integers, with the sign of the divisor."""


Multiplication = _function.Multiplication.INSTANCE
"""The function `*/2`: the product of two numbers."""


NaturalLogarithm = _function.NaturalLogarithm.INSTANCE
"""The function `log/1`: the natural logarithm of a number."""


Remainder = _function.Remainder.INSTANCE
"""The function `rem/2`: the remainder of two integers, with the sign of the dividend."""


Round = _function.Round.INSTANCE
"""The function `round/1`: the integer nearest to a number."""


Sign = _function.Sign.INSTANCE
"""The function `sign/1`: the sign of a number: -1, 0 or 1."""


SignReversal = _function.SignReversal.INSTANCE
"""The function `-/1`: the opposite of a number."""


Sine = _function.Sine.INSTANCE
"""The function `sin/1`: the sine of an angle, in radians."""


SquareRoot = _function.SquareRoot.INSTANCE
"""The function `sqrt/1`: the square root of a number."""


Subtraction = _function.Subtraction.INSTANCE
"""The function `-/2`: the difference of two numbers."""


ToFloat = _function.ToFloat.INSTANCE
"""The function `float/1`: a number converted to a float."""


Truncate = _function.Truncate.INSTANCE
"""The function `truncate/1`: the integer part of a number."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.function.*")
