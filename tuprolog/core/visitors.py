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
        return TermVisitor.DefaultImpls.visitTerm(self, term)

    @jpype.JOverride
    def visitVar(self, term):
        return TermVisitor.DefaultImpls.visitVar(self, term)

    @jpype.JOverride
    def visitConstant(self, term):
        return TermVisitor.DefaultImpls.visitConstant(self, term)

    @jpype.JOverride
    def visitStruct(self, term):
        return TermVisitor.DefaultImpls.visitStruct(self, term)

    @jpype.JOverride
    def visitCollection(self, term):
        return TermVisitor.DefaultImpls.visitCollection(self, term)

    @jpype.JOverride
    def visitAtom(self, term):
        return TermVisitor.DefaultImpls.visitAtom(self, term)

    @jpype.JOverride
    def visitTruth(self, term):
        return TermVisitor.DefaultImpls.visitTruth(self, term)

    @jpype.JOverride
    def visitNumeric(self, term):
        return TermVisitor.DefaultImpls.visitNumeric(self, term)

    @jpype.JOverride
    def visitInteger(self, term):
        return TermVisitor.DefaultImpls.visitInteger(self, term)

    @jpype.JOverride
    def visitReal(self, term):
        return TermVisitor.DefaultImpls.visitReal(self, term)

    @jpype.JOverride
    def visitBlock(self, term):
        return TermVisitor.DefaultImpls.visitBlock(self, term)

    @jpype.JOverride
    def visitEmpty(self, term):
        return TermVisitor.DefaultImpls.visitEmpty(self, term)

    @jpype.JOverride
    def visitEmptyBlock(self, term):
        return TermVisitor.DefaultImpls.visitEmptyBlock(self, term)

    @jpype.JOverride
    def visitList(self, term):
        return TermVisitor.DefaultImpls.visitList(self, term)

    @jpype.JOverride
    def visitCons(self, term):
        return TermVisitor.DefaultImpls.visitCons(self, term)

    @jpype.JOverride
    def visitEmptyList(self, term):
        return TermVisitor.DefaultImpls.visitEmptyList(self, term)

    @jpype.JOverride
    def visitTuple(self, term):
        return TermVisitor.DefaultImpls.visitTuple(self, term)

    @jpype.JOverride
    def visitIndicator(self, term):
        return TermVisitor.DefaultImpls.visitIndicator(self, term)

    @jpype.JOverride
    def visitClause(self, term):
        return TermVisitor.DefaultImpls.visitClause(self, term)

    @jpype.JOverride
    def visitRule(self, term):
        return TermVisitor.DefaultImpls.visitRule(self, term)

    @jpype.JOverride
    def visitFact(self, term):
        return TermVisitor.DefaultImpls.visitFact(self, term)

    @jpype.JOverride
    def visitDirective(self, term):
        return TermVisitor.DefaultImpls.visitDirective(self, term)


logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermVisitor.class_.getName()))
