from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Abolish
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Arg
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import ArithmeticEqual
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import ArithmeticGreaterThan
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import ArithmeticGreaterThanOrEqualTo
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import ArithmeticLowerThan
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import ArithmeticLowerThanOrEqualTo
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import ArithmeticNotEqual
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Assert
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import AssertA
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import AssertZ
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Atom
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import AtomChars
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import AtomCodes
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import AtomConcat
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import AtomLength
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Atomic
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import BagOf
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Between
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Callable
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import CharCode
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Clause
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Compound
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import CopyTerm
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import CurrentFlag
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import CurrentOp
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import EnsureExecutable
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import FindAll
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Float
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Functor
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import GetDurable
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import GetEphemeral
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import GetPersistent
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Ground
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Halt
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Halt1
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Integer
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Is
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Natural
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import NewLine
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import NonVar
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import NotUnifiableWith
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Number
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import NumberChars
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import NumberCodes
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Op
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Repeat
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Retract
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import RetractAll
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Reverse
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import SetDurable
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import SetEphemeral
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import SetFlag
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import SetOf
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import SetPersistent
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Sleep
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import SubAtom
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermGreaterThan
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermGreaterThanOrEqualTo
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermIdentical
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermLowerThan
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermLowerThanOrEqualTo
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermNotIdentical
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermNotSame
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import TermSame
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import UnifiesWith
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Univ
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Var
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.primitive import Write

Abolish = Abolish.INSTANCE

Arg = Arg.INSTANCE

ArithmeticEqual = ArithmeticEqual.INSTANCE

ArithmeticGreaterThan = ArithmeticGreaterThan.INSTANCE

ArithmeticGreaterThanOrEqualTo = ArithmeticGreaterThanOrEqualTo.INSTANCE

ArithmeticLowerThan = ArithmeticLowerThan.INSTANCE

ArithmeticLowerThanOrEqualTo = ArithmeticLowerThanOrEqualTo.INSTANCE

ArithmeticNotEqual = ArithmeticNotEqual.INSTANCE

Assert = Assert.INSTANCE

AssertA = AssertA.INSTANCE

AssertZ = AssertZ.INSTANCE

Atom = Atom.INSTANCE

AtomChars = AtomChars.INSTANCE

AtomCodes = AtomCodes.INSTANCE

AtomConcat = AtomConcat.INSTANCE

AtomLength = AtomLength.INSTANCE

Atomic = Atomic.INSTANCE

BagOf = BagOf.INSTANCE

Between = Between.INSTANCE

Callable = Callable.INSTANCE

CharCode = CharCode.INSTANCE

Clause = Clause.INSTANCE

Compound = Compound.INSTANCE

CopyTerm = CopyTerm.INSTANCE

CurrentFlag = CurrentFlag.INSTANCE

CurrentOp = CurrentOp.INSTANCE

EnsureExecutable = EnsureExecutable.INSTANCE

FindAll = FindAll.INSTANCE

Float = Float.INSTANCE

Functor = Functor.INSTANCE

GetDurable = GetDurable.INSTANCE

GetEphemeral = GetEphemeral.INSTANCE

GetPersistent = GetPersistent.INSTANCE

Ground = Ground.INSTANCE

Halt = Halt.INSTANCE

Halt1 = Halt1.INSTANCE

Integer = Integer.INSTANCE

Is = Is.INSTANCE

Natural = Natural.INSTANCE

NewLine = NewLine.INSTANCE

NonVar = NonVar.INSTANCE

NotUnifiableWith = NotUnifiableWith.INSTANCE

Number = Number.INSTANCE

NumberChars = NumberChars.INSTANCE

NumberCodes = NumberCodes.INSTANCE

Op = Op.INSTANCE

Repeat = Repeat.INSTANCE

Retract = Retract.INSTANCE

RetractAll = RetractAll.INSTANCE

Reverse = Reverse.INSTANCE

SetDurable = SetDurable.INSTANCE

SetEphemeral = SetEphemeral.INSTANCE

SetFlag = SetFlag.INSTANCE

SetOf = SetOf.INSTANCE

SetPersistent = SetPersistent.INSTANCE

Sleep = Sleep.INSTANCE

SubAtom = SubAtom.INSTANCE

TermGreaterThan = TermGreaterThan.INSTANCE

TermGreaterThanOrEqualTo = TermGreaterThanOrEqualTo.INSTANCE

TermIdentical = TermIdentical.INSTANCE

TermLowerThan = TermLowerThan.INSTANCE

TermLowerThanOrEqualTo = TermLowerThanOrEqualTo.INSTANCE

TermNotIdentical = TermNotIdentical.INSTANCE

TermNotSame = TermNotSame.INSTANCE

TermSame = TermSame.INSTANCE

UnifiesWith = UnifiesWith.INSTANCE

Univ = Univ.INSTANCE

Var = Var.INSTANCE

Write = Write.INSTANCE



logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.primitive.*")
