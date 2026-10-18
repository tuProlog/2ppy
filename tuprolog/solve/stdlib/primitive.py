"""The primitives of the standard library, i.e. its predicates implemented in Kotlin.

Each constant is a primitive with a `signature` (its name and arity in Prolog, e.g.
`atom_length/2`), loaded by default in Prolog solvers; most are ISO Prolog's built-in predicates.
Their `implementation` is the `tuprolog.solve.primitive.Primitive` solving them.

`Atom`, `Clause`, `Integer` and `Var` are left out of `__all__`, as star-imports would shadow the
homonymous types of `tuprolog.core`: use them qualified (e.g. `primitive.Atom`).

Examples:
    >>> AtomLength.signature
    Signature(name=atom_length, arity=2, vararg=false)
"""

import it.unibo.tuprolog.solve.stdlib.primitive as _primitive  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

# Atom, Clause, Integer and Var are left out, as star-imports would shadow tuprolog.core's:
# use them qualified (e.g. primitive.Atom)
__all__ = [
    "Abolish",
    "Arg",
    "ArithmeticEqual",
    "ArithmeticGreaterThan",
    "ArithmeticGreaterThanOrEqualTo",
    "ArithmeticLowerThan",
    "ArithmeticLowerThanOrEqualTo",
    "ArithmeticNotEqual",
    "Assert",
    "AssertA",
    "AssertZ",
    "AtomChars",
    "AtomCodes",
    "AtomConcat",
    "AtomLength",
    "Atomic",
    "BagOf",
    "Between",
    "Callable",
    "CharCode",
    "Compound",
    "CopyTerm",
    "CurrentFlag",
    "CurrentOp",
    "EnsureExecutable",
    "FindAll",
    "Float",
    "Functor",
    "GetDurable",
    "GetEphemeral",
    "GetPersistent",
    "Ground",
    "Halt",
    "Halt1",
    "InternalHelp",
    "Is",
    "Natural",
    "NewLine",
    "NonVar",
    "NotUnifiableWith",
    "Number",
    "NumberChars",
    "NumberCodes",
    "Op",
    "Repeat",
    "Retract",
    "RetractAll",
    "Reverse",
    "SetDurable",
    "SetEphemeral",
    "SetFlag",
    "SetOf",
    "SetPersistent",
    "Sleep",
    "SubAtom",
    "TermGreaterThan",
    "TermGreaterThanOrEqualTo",
    "TermIdentical",
    "TermLowerThan",
    "TermLowerThanOrEqualTo",
    "TermNotIdentical",
    "TermNotSame",
    "TermSame",
    "UnifiesWith",
    "Univ",
    "Write",
]


Abolish: _primitive.Abolish = _primitive.Abolish.INSTANCE
"""The primitive `abolish/1`.

Removes all the clauses of a dynamic predicate, given its indicator.
"""


Arg: _primitive.Arg = _primitive.Arg.INSTANCE
"""The primitive `arg/3`: the `N`-th argument of a compound term."""


ArithmeticEqual: _primitive.ArithmeticEqual = _primitive.ArithmeticEqual.INSTANCE
"""The primitive `=:=/2`: two arithmetic expressions evaluate to equal numbers."""


ArithmeticGreaterThan: _primitive.ArithmeticGreaterThan = _primitive.ArithmeticGreaterThan.INSTANCE
"""The primitive `>/2`: an arithmetic expression evaluates to more than another."""


ArithmeticGreaterThanOrEqualTo: _primitive.ArithmeticGreaterThanOrEqualTo = (
    _primitive.ArithmeticGreaterThanOrEqualTo.INSTANCE
)
"""The primitive `>=/2`: an expression evaluates to at least another."""


ArithmeticLowerThan: _primitive.ArithmeticLowerThan = _primitive.ArithmeticLowerThan.INSTANCE
"""The primitive `</2`: an arithmetic expression evaluates to less than another."""


ArithmeticLowerThanOrEqualTo: _primitive.ArithmeticLowerThanOrEqualTo = (
    _primitive.ArithmeticLowerThanOrEqualTo.INSTANCE
)
"""The primitive `=</2`: an expression evaluates to at most another."""


ArithmeticNotEqual: _primitive.ArithmeticNotEqual = _primitive.ArithmeticNotEqual.INSTANCE
"""The primitive `=\\=/2`: two arithmetic expressions evaluate to different numbers."""


Assert: _primitive.Assert = _primitive.Assert.INSTANCE
"""The primitive `assert/1`: adds a clause at the end of the dynamic knowledge base."""


AssertA: _primitive.AssertA = _primitive.AssertA.INSTANCE
"""The primitive `asserta/1`: adds a clause at the beginning of the dynamic knowledge base."""


AssertZ: _primitive.AssertZ = _primitive.AssertZ.INSTANCE
"""The primitive `assertz/1`: adds a clause at the end of the dynamic knowledge base."""


Atom: _primitive.Atom = _primitive.Atom.INSTANCE
"""The primitive `atom/1`: a term is an atom."""


AtomChars: _primitive.AtomChars = _primitive.AtomChars.INSTANCE
"""The primitive `atom_chars/2`: relates an atom to the list of its characters."""


AtomCodes: _primitive.AtomCodes = _primitive.AtomCodes.INSTANCE
"""The primitive `atom_codes/2`: relates an atom to the list of its character codes."""


AtomConcat: _primitive.AtomConcat = _primitive.AtomConcat.INSTANCE
"""The primitive `atom_concat/3`: an atom is the concatenation of two others."""


AtomLength: _primitive.AtomLength = _primitive.AtomLength.INSTANCE
"""The primitive `atom_length/2`: the number of characters of an atom."""


Atomic: _primitive.Atomic = _primitive.Atomic.INSTANCE
"""The primitive `atomic/1`: a term is atomic, i.e. an atom or a number."""


BagOf: _primitive.BagOf = _primitive.BagOf.INSTANCE
"""The primitive `bagof/3`: the list of the instances of a template for the solutions of a goal."""


Between: _primitive.Between = _primitive.Between.INSTANCE
"""The primitive `between/3`: an integer is between two others, inclusive."""


Callable: _primitive.Callable = _primitive.Callable.INSTANCE
"""The primitive `callable/1`: a term is callable, i.e. an atom or a compound term."""


CharCode: _primitive.CharCode = _primitive.CharCode.INSTANCE
"""The primitive `char_code/2`: relates a character to its code."""


Clause: _primitive.Clause = _primitive.Clause.INSTANCE
"""The primitive `clause/2`: a clause of the knowledge base, by head and body."""


Compound: _primitive.Compound = _primitive.Compound.INSTANCE
"""The primitive `compound/1`: a term is a compound term."""


CopyTerm: _primitive.CopyTerm = _primitive.CopyTerm.INSTANCE
"""The primitive `copy_term/2`: a copy of a term, with fresh variables."""


CurrentFlag: _primitive.CurrentFlag = _primitive.CurrentFlag.INSTANCE
"""The primitive `current_flag/2`: a flag and its value."""


CurrentOp: _primitive.CurrentOp = _primitive.CurrentOp.INSTANCE
"""The primitive `current_op/3`: an operator, by priority, specifier and symbol."""


EnsureExecutable: _primitive.EnsureExecutable = _primitive.EnsureExecutable.INSTANCE
"""The primitive `ensure_executable/1`: raises an error unless a term is callable."""


FindAll: _primitive.FindAll = _primitive.FindAll.INSTANCE
"""The primitive `findall/3`.

The list of the instances of a template for all the solutions of a goal.
"""


Float: _primitive.Float = _primitive.Float.INSTANCE
"""The primitive `float/1`: a term is a floating-point number."""


Functor: _primitive.Functor = _primitive.Functor.INSTANCE
"""The primitive `functor/3`: relates a term to its name and arity."""


GetDurable: _primitive.GetDurable = _primitive.GetDurable.INSTANCE
"""The primitive `get_durable/2`: a value of the durable custom data, by key."""


GetEphemeral: _primitive.GetEphemeral = _primitive.GetEphemeral.INSTANCE
"""The primitive `get_ephemeral/2`: a value of the ephemeral custom data, by key."""


GetPersistent: _primitive.GetPersistent = _primitive.GetPersistent.INSTANCE
"""The primitive `get_persistent/2`: a value of the persistent custom data, by key."""


Ground: _primitive.Ground = _primitive.Ground.INSTANCE
"""The primitive `ground/1`: a term has no variables."""


Halt: _primitive.Halt = _primitive.Halt.INSTANCE
"""The primitive `halt/0`: stops the resolution."""


Halt1: _primitive.Halt1 = _primitive.Halt1.INSTANCE
"""The primitive `halt/1`: stops the resolution, with an exit code."""


Integer: _primitive.Integer = _primitive.Integer.INSTANCE
"""The primitive `integer/1`: a term is an integer."""


InternalHelp: _primitive.InternalHelp = _primitive.InternalHelp.INSTANCE
"""The primitive `__help__/2`: the help text of a subject, behind `help/2`."""


Is: _primitive.Is = _primitive.Is.INSTANCE
"""The primitive `is/2`: the value of an arithmetic expression."""


Natural: _primitive.Natural = _primitive.Natural.INSTANCE
"""The primitive `natural/1`: a term is a natural number, or generates them if a variable."""


NewLine: _primitive.NewLine = _primitive.NewLine.INSTANCE
"""The primitive `nl/0`: writes a new line on the current output."""


NonVar: _primitive.NonVar = _primitive.NonVar.INSTANCE
"""The primitive `nonvar/1`: a term is not a variable."""


NotUnifiableWith: _primitive.NotUnifiableWith = _primitive.NotUnifiableWith.INSTANCE
"""The primitive `\\=/2`: two terms do not unify."""


Number: _primitive.Number = _primitive.Number.INSTANCE
"""The primitive `number/1`: a term is a number."""


NumberChars: _primitive.NumberChars = _primitive.NumberChars.INSTANCE
"""The primitive `number_chars/2`: relates a number to the list of its characters."""


NumberCodes: _primitive.NumberCodes = _primitive.NumberCodes.INSTANCE
"""The primitive `number_codes/2`: relates a number to the list of its character codes."""


Op: _primitive.Op = _primitive.Op.INSTANCE
"""The primitive `op/3`: declares an operator, by priority, specifier and symbol."""


Repeat: _primitive.Repeat = _primitive.Repeat.INSTANCE
"""The primitive `repeat/0`: succeeds infinitely many times."""


Retract: _primitive.Retract = _primitive.Retract.INSTANCE
"""The primitive `retract/1`: removes a clause from the dynamic knowledge base."""


RetractAll: _primitive.RetractAll = _primitive.RetractAll.INSTANCE
"""The primitive `retractall/1`: removes the dynamic clauses whose head unifies with a term."""


Reverse: _primitive.Reverse = _primitive.Reverse.INSTANCE
"""The primitive `reverse/2`: a list in reverse order."""


SetDurable: _primitive.SetDurable = _primitive.SetDurable.INSTANCE
"""The primitive `set_durable/2`: sets a value of the durable custom data, by key."""


SetEphemeral: _primitive.SetEphemeral = _primitive.SetEphemeral.INSTANCE
"""The primitive `set_ephemeral/2`: sets a value of the ephemeral custom data, by key."""


SetFlag: _primitive.SetFlag = _primitive.SetFlag.INSTANCE
"""The primitive `set_flag/2`: sets the value of a flag."""


SetOf: _primitive.SetOf = _primitive.SetOf.INSTANCE
"""The primitive `setof/3`: the sorted list, without duplicates, of the instances of a template."""


SetPersistent: _primitive.SetPersistent = _primitive.SetPersistent.INSTANCE
"""The primitive `set_persistent/2`: sets a value of the persistent custom data, by key."""


Sleep: _primitive.Sleep = _primitive.Sleep.INSTANCE
"""The primitive `sleep/1`: waits for a number of milliseconds."""


SubAtom: _primitive.SubAtom = _primitive.SubAtom.INSTANCE
"""The primitive `sub_atom/5`: a sub-atom of an atom, by position and length."""


TermGreaterThan: _primitive.TermGreaterThan = _primitive.TermGreaterThan.INSTANCE
"""The primitive `@>/2`: a term follows another in the standard order of terms."""


TermGreaterThanOrEqualTo: _primitive.TermGreaterThanOrEqualTo = (
    _primitive.TermGreaterThanOrEqualTo.INSTANCE
)
"""The primitive `@>=/2`: a term does not precede another in the standard order."""


TermIdentical: _primitive.TermIdentical = _primitive.TermIdentical.INSTANCE
"""The primitive `==/2`: two terms are identical."""


TermLowerThan: _primitive.TermLowerThan = _primitive.TermLowerThan.INSTANCE
"""The primitive `@</2`: a term precedes another in the standard order of terms."""


TermLowerThanOrEqualTo: _primitive.TermLowerThanOrEqualTo = (
    _primitive.TermLowerThanOrEqualTo.INSTANCE
)
"""The primitive `@=</2`: a term does not follow another in the standard order."""


TermNotIdentical: _primitive.TermNotIdentical = _primitive.TermNotIdentical.INSTANCE
"""The primitive `\\==/2`: two terms are not identical."""


TermNotSame: _primitive.TermNotSame = _primitive.TermNotSame.INSTANCE
"""The primitive `\\=@=/2`: two terms are not variants of each other."""


TermSame: _primitive.TermSame = _primitive.TermSame.INSTANCE
"""The primitive `=@=/2`: two terms are variants, i.e. equal up to variable renaming."""


UnifiesWith: _primitive.UnifiesWith = _primitive.UnifiesWith.INSTANCE
"""The primitive `=/2`: unifies two terms."""


Univ: _primitive.Univ = _primitive.Univ.INSTANCE
"""The primitive `=../2`: relates a term to the list of its name and arguments."""


Var: _primitive.Var = _primitive.Var.INSTANCE
"""The primitive `var/1`: a term is a variable."""


Write: _primitive.Write = _primitive.Write.INSTANCE
"""The primitive `write/1`: writes a term on the current output."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.primitive.*")
