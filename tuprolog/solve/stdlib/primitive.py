from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.stdlib.primitive as _primitive  # type: ignore


Abolish: _primitive.Abolish = _primitive.Abolish.INSTANCE


Arg: _primitive.Arg = _primitive.Arg.INSTANCE


ArithmeticEqual: _primitive.ArithmeticEqual = _primitive.ArithmeticEqual.INSTANCE


ArithmeticGreaterThan: _primitive.ArithmeticGreaterThan = _primitive.ArithmeticGreaterThan.INSTANCE


ArithmeticGreaterThanOrEqualTo: _primitive.ArithmeticGreaterThanOrEqualTo = _primitive.ArithmeticGreaterThanOrEqualTo.INSTANCE


ArithmeticLowerThan: _primitive.ArithmeticLowerThan = _primitive.ArithmeticLowerThan.INSTANCE


ArithmeticLowerThanOrEqualTo: _primitive.ArithmeticLowerThanOrEqualTo = _primitive.ArithmeticLowerThanOrEqualTo.INSTANCE


ArithmeticNotEqual: _primitive.ArithmeticNotEqual = _primitive.ArithmeticNotEqual.INSTANCE


Assert: _primitive.Assert = _primitive.Assert.INSTANCE


AssertA: _primitive.AssertA = _primitive.AssertA.INSTANCE


AssertZ: _primitive.AssertZ = _primitive.AssertZ.INSTANCE


Atom: _primitive.Atom = _primitive.Atom.INSTANCE


AtomChars: _primitive.AtomChars = _primitive.AtomChars.INSTANCE


AtomCodes: _primitive.AtomCodes = _primitive.AtomCodes.INSTANCE


AtomConcat: _primitive.AtomConcat = _primitive.AtomConcat.INSTANCE


AtomLength: _primitive.AtomLength = _primitive.AtomLength.INSTANCE


Atomic: _primitive.Atomic = _primitive.Atomic.INSTANCE


BagOf: _primitive.BagOf = _primitive.BagOf.INSTANCE


Between: _primitive.Between = _primitive.Between.INSTANCE


Callable: _primitive.Callable = _primitive.Callable.INSTANCE


CharCode: _primitive.CharCode = _primitive.CharCode.INSTANCE


Clause: _primitive.Clause = _primitive.Clause.INSTANCE


Compound: _primitive.Compound = _primitive.Compound.INSTANCE


CopyTerm: _primitive.CopyTerm = _primitive.CopyTerm.INSTANCE


CurrentFlag: _primitive.CurrentFlag = _primitive.CurrentFlag.INSTANCE


CurrentOp: _primitive.CurrentOp = _primitive.CurrentOp.INSTANCE


EnsureExecutable: _primitive.EnsureExecutable = _primitive.EnsureExecutable.INSTANCE


FindAll: _primitive.FindAll = _primitive.FindAll.INSTANCE


Float: _primitive.Float = _primitive.Float.INSTANCE


Functor: _primitive.Functor = _primitive.Functor.INSTANCE


GetDurable: _primitive.GetDurable = _primitive.GetDurable.INSTANCE


GetEphemeral: _primitive.GetEphemeral = _primitive.GetEphemeral.INSTANCE


GetPersistent: _primitive.GetPersistent = _primitive.GetPersistent.INSTANCE


Ground: _primitive.Ground = _primitive.Ground.INSTANCE


Halt: _primitive.Halt = _primitive.Halt.INSTANCE


Halt1: _primitive.Halt1 = _primitive.Halt1.INSTANCE


Integer: _primitive.Integer = _primitive.Integer.INSTANCE


Is: _primitive.Is = _primitive.Is.INSTANCE


Natural: _primitive.Natural = _primitive.Natural.INSTANCE


NewLine: _primitive.NewLine = _primitive.NewLine.INSTANCE


NonVar: _primitive.NonVar = _primitive.NonVar.INSTANCE


NotUnifiableWith: _primitive.NotUnifiableWith = _primitive.NotUnifiableWith.INSTANCE


Number: _primitive.Number = _primitive.Number.INSTANCE


NumberChars: _primitive.NumberChars = _primitive.NumberChars.INSTANCE


NumberCodes: _primitive.NumberCodes = _primitive.NumberCodes.INSTANCE


Op: _primitive.Op = _primitive.Op.INSTANCE


Repeat: _primitive.Repeat = _primitive.Repeat.INSTANCE


Retract: _primitive.Retract = _primitive.Retract.INSTANCE


RetractAll: _primitive.RetractAll = _primitive.RetractAll.INSTANCE


Reverse: _primitive.Reverse = _primitive.Reverse.INSTANCE


SetDurable: _primitive.SetDurable = _primitive.SetDurable.INSTANCE


SetEphemeral: _primitive.SetEphemeral = _primitive.SetEphemeral.INSTANCE


SetFlag: _primitive.SetFlag = _primitive.SetFlag.INSTANCE


SetOf: _primitive.SetOf = _primitive.SetOf.INSTANCE


SetPersistent: _primitive.SetPersistent = _primitive.SetPersistent.INSTANCE


Sleep: _primitive.Sleep = _primitive.Sleep.INSTANCE


SubAtom: _primitive.SubAtom = _primitive.SubAtom.INSTANCE


TermGreaterThan: _primitive.TermGreaterThan = _primitive.TermGreaterThan.INSTANCE


TermGreaterThanOrEqualTo: _primitive.TermGreaterThanOrEqualTo = _primitive.TermGreaterThanOrEqualTo.INSTANCE


TermIdentical: _primitive.TermIdentical = _primitive.TermIdentical.INSTANCE


TermLowerThan: _primitive.TermLowerThan = _primitive.TermLowerThan.INSTANCE


TermLowerThanOrEqualTo: _primitive.TermLowerThanOrEqualTo = _primitive.TermLowerThanOrEqualTo.INSTANCE


TermNotIdentical: _primitive.TermNotIdentical = _primitive.TermNotIdentical.INSTANCE


TermNotSame: _primitive.TermNotSame = _primitive.TermNotSame.INSTANCE


TermSame: _primitive.TermSame = _primitive.TermSame.INSTANCE


UnifiesWith: _primitive.UnifiesWith = _primitive.UnifiesWith.INSTANCE


Univ: _primitive.Univ = _primitive.Univ.INSTANCE


Var: _primitive.Var = _primitive.Var.INSTANCE


Write: _primitive.Write = _primitive.Write.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.primitive.*")
