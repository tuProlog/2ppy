from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.stdlib.primitive as _primitive


Abolish = _primitive.Abolish.INSTANCE

Arg = _primitive.Arg.INSTANCE

ArithmeticEqual = _primitive.ArithmeticEqual.INSTANCE

ArithmeticGreaterThan = _primitive.ArithmeticGreaterThan.INSTANCE

ArithmeticGreaterThanOrEqualTo = _primitive.ArithmeticGreaterThanOrEqualTo.INSTANCE

ArithmeticLowerThan = _primitive.ArithmeticLowerThan.INSTANCE

ArithmeticLowerThanOrEqualTo = _primitive.ArithmeticLowerThanOrEqualTo.INSTANCE

ArithmeticNotEqual = _primitive.ArithmeticNotEqual.INSTANCE

Assert = _primitive.Assert.INSTANCE

AssertA = _primitive.AssertA.INSTANCE

AssertZ = _primitive.AssertZ.INSTANCE

Atom = _primitive.Atom.INSTANCE

AtomChars = _primitive.AtomChars.INSTANCE

AtomCodes = _primitive.AtomCodes.INSTANCE

AtomConcat = _primitive.AtomConcat.INSTANCE

AtomLength = _primitive.AtomLength.INSTANCE

Atomic = _primitive.Atomic.INSTANCE

BagOf = _primitive.BagOf.INSTANCE

Between = _primitive.Between.INSTANCE

Callable = _primitive.Callable.INSTANCE

CharCode = _primitive.CharCode.INSTANCE

Clause = _primitive.Clause.INSTANCE

Compound = _primitive.Compound.INSTANCE

CopyTerm = _primitive.CopyTerm.INSTANCE

CurrentFlag = _primitive.CurrentFlag.INSTANCE

CurrentOp = _primitive.CurrentOp.INSTANCE

EnsureExecutable = _primitive.EnsureExecutable.INSTANCE

FindAll = _primitive.FindAll.INSTANCE

Float = _primitive.Float.INSTANCE

Functor = _primitive.Functor.INSTANCE

GetDurable = _primitive.GetDurable.INSTANCE

GetEphemeral = _primitive.GetEphemeral.INSTANCE

GetPersistent = _primitive.GetPersistent.INSTANCE

Ground = _primitive.Ground.INSTANCE

Halt = _primitive.Halt.INSTANCE

Halt1 = _primitive.Halt1.INSTANCE

Integer = _primitive.Integer.INSTANCE

Is = _primitive.Is.INSTANCE

Natural = _primitive.Natural.INSTANCE

NewLine = _primitive.NewLine.INSTANCE

NonVar = _primitive.NonVar.INSTANCE

NotUnifiableWith = _primitive.NotUnifiableWith.INSTANCE

Number = _primitive.Number.INSTANCE

NumberChars = _primitive.NumberChars.INSTANCE

NumberCodes = _primitive.NumberCodes.INSTANCE

Op = _primitive.Op.INSTANCE

Repeat = _primitive.Repeat.INSTANCE

Retract = _primitive.Retract.INSTANCE

RetractAll = _primitive.RetractAll.INSTANCE

Reverse = _primitive.Reverse.INSTANCE

SetDurable = _primitive.SetDurable.INSTANCE

SetEphemeral = _primitive.SetEphemeral.INSTANCE

SetFlag = _primitive.SetFlag.INSTANCE

SetOf = _primitive.SetOf.INSTANCE

SetPersistent = _primitive.SetPersistent.INSTANCE

Sleep = _primitive.Sleep.INSTANCE

SubAtom = _primitive.SubAtom.INSTANCE

TermGreaterThan = _primitive.TermGreaterThan.INSTANCE

TermGreaterThanOrEqualTo = _primitive.TermGreaterThanOrEqualTo.INSTANCE

TermIdentical = _primitive.TermIdentical.INSTANCE

TermLowerThan = _primitive.TermLowerThan.INSTANCE

TermLowerThanOrEqualTo = _primitive.TermLowerThanOrEqualTo.INSTANCE

TermNotIdentical = _primitive.TermNotIdentical.INSTANCE

TermNotSame = _primitive.TermNotSame.INSTANCE

TermSame = _primitive.TermSame.INSTANCE

UnifiesWith = _primitive.UnifiesWith.INSTANCE

Univ = _primitive.Univ.INSTANCE

Var = _primitive.Var.INSTANCE

Write = _primitive.Write.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.primitive.*")
