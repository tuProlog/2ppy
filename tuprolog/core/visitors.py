from tuprolog import logger
import jpype
from tuprolog.core import TermVisitor


@jpype.JImplements(TermVisitor)
class AbstractTermVisitor(object):

    @jpype.JOverride
    def defaultValue(self, term):
        raise NotImplementedError()

    @jpype.JOverride
    def visitTerm(self, term):
        return TermVisitor.visitTerm(self, term)

    @jpype.JOverride
    def visitVar(self, term):
        return TermVisitor.visitVar(self, term)

    @jpype.JOverride
    def visitConstant(self, term):
        return TermVisitor.visitConstant(self, term)

    @jpype.JOverride
    def visitStruct(self, term):
        return TermVisitor.visitStruct(self, term)

    @jpype.JOverride
    def visitCollection(self, term):
        return TermVisitor.visitCollection(self, term)

    @jpype.JOverride
    def visitAtom(self, term):
        return TermVisitor.visitAtom(self, term)

    @jpype.JOverride
    def visitTruth(self, term):
        return TermVisitor.visitTruth(self, term)

    @jpype.JOverride
    def visitNumeric(self, term):
        return TermVisitor.visitNumeric(self, term)

    @jpype.JOverride
    def visitInteger(self, term):
        return TermVisitor.visitInteger(self, term)

    @jpype.JOverride
    def visitReal(self, term):
        return TermVisitor.visitReal(self, term)

    @jpype.JOverride
    def visitBlock(self, term):
        return TermVisitor.visitBlock(self, term)

    @jpype.JOverride
    def visitEmpty(self, term):
        return TermVisitor.visitEmpty(self, term)

    @jpype.JOverride
    def visitEmptyBlock(self, term):
        return TermVisitor.visitEmptyBlock(self, term)

    @jpype.JOverride
    def visitList(self, term):
        return TermVisitor.visitList(self, term)

    @jpype.JOverride
    def visitCons(self, term):
        return TermVisitor.visitCons(self, term)

    @jpype.JOverride
    def visitEmptyList(self, term):
        return TermVisitor.visitEmptyList(self, term)

    @jpype.JOverride
    def visitTuple(self, term):
        return TermVisitor.visitTuple(self, term)

    @jpype.JOverride
    def visitIndicator(self, term):
        return TermVisitor.visitIndicator(self, term)

    @jpype.JOverride
    def visitClause(self, term):
        return TermVisitor.visitClause(self, term)

    @jpype.JOverride
    def visitRule(self, term):
        return TermVisitor.visitRule(self, term)

    @jpype.JOverride
    def visitFact(self, term):
        return TermVisitor.visitFact(self, term)

    @jpype.JOverride
    def visitDirective(self, term):
        return TermVisitor.visitDirective(self, term)


logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermVisitor.class_.getName()))
