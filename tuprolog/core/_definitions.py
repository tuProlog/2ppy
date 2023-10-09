from jpype import JImplements, JOverride
from tuprolog import logger
import jpype.imports
import it.unibo.tuprolog.core as _core # type: ignore


Applicable = _core.Applicable


Atom = _core.Atom


Block = _core.Block


Clause = _core.Clause


Cons = _core.Cons


Constant = _core.Constant


Directive = _core.Directive


Empty = _core.Empty


EmptyBlock = _core.EmptyBlock


EmptyList = _core.EmptyList


Fact = _core.Fact


Formatter = _core.Formatter


Indicator = _core.Indicator


Integer = _core.Integer


List = _core.List


Numeric = _core.Numeric


Real = _core.Real


Recursive = _core.Recursive


Rule = _core.Rule


Scope = _core.Scope


Struct = _core.Struct


Substitution = _core.Substitution


Term = _core.Term


TermComparator = _core.TermComparator


TermConvertible = _core.TermConvertible


TermFormatter = _core.TermFormatter


Terms = _core.Terms


TermVisitor = _core.TermVisitor


Truth = _core.Truth


Tuple = _core.Tuple


Var = _core.Var


Variabled = _core.Variabled


TRUE = Truth.TRUE


FALSE = Truth.FALSE


FAIL = Truth.FAIL


@JImplements(TermComparator)
class AbstractTermComparator(object):
    @JOverride
    def equals(self, other):
        return self is other

    @JOverride
    def compare(self, first, second):
        raise NotImplementedError()


@JImplements(TermConvertible)
class AbstractTermConvertible(object):
    @JOverride
    def toTerm(self):
        raise NotImplementedError()


@JImplements(TermVisitor)
class AbstractTermVisitor(object):

    @JOverride
    def defaultValue(self, term):
        raise NotImplementedError()

    @JOverride
    def visitTerm(self, term):
        return TermVisitor.visitTerm(self, term)

    @JOverride
    def visitVar(self, term):
        return TermVisitor.visitVar(self, term)

    @JOverride
    def visitConstant(self, term):
        return TermVisitor.visitConstant(self, term)

    @JOverride
    def visitStruct(self, term):
        return TermVisitor.visitStruct(self, term)

    @JOverride
    def visitCollection(self, term):
        return TermVisitor.visitCollection(self, term)

    @JOverride
    def visitAtom(self, term):
        return TermVisitor.visitAtom(self, term)

    @JOverride
    def visitTruth(self, term):
        return TermVisitor.visitTruth(self, term)

    @JOverride
    def visitNumeric(self, term):
        return TermVisitor.visitNumeric(self, term)

    @JOverride
    def visitInteger(self, term):
        return TermVisitor.visitInteger(self, term)

    @JOverride
    def visitReal(self, term):
        return TermVisitor.visitReal(self, term)

    @JOverride
    def visitBlock(self, term):
        return TermVisitor.visitBlock(self, term)

    @JOverride
    def visitEmpty(self, term):
        return TermVisitor.visitEmpty(self, term)

    @JOverride
    def visitEmptyBlock(self, term):
        return TermVisitor.visitEmptyBlock(self, term)

    @JOverride
    def visitList(self, term):
        return TermVisitor.visitList(self, term)

    @JOverride
    def visitCons(self, term):
        return TermVisitor.visitCons(self, term)

    @JOverride
    def visitEmptyList(self, term):
        return TermVisitor.visitEmptyList(self, term)

    @JOverride
    def visitTuple(self, term):
        return TermVisitor.visitTuple(self, term)

    @JOverride
    def visitIndicator(self, term):
        return TermVisitor.visitIndicator(self, term)

    @JOverride
    def visitClause(self, term):
        return TermVisitor.visitClause(self, term)

    @JOverride
    def visitRule(self, term):
        return TermVisitor.visitRule(self, term)

    @JOverride
    def visitFact(self, term):
        return TermVisitor.visitFact(self, term)

    @JOverride
    def visitDirective(self, term):
        return TermVisitor.visitDirective(self, term)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.*")
