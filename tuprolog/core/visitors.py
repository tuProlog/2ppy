from jpype import JImplements, JOverride
from tuprolog import logger
import jpype.imports
import it.unibo.tuprolog.core as _core # type: ignore

TermVisitor = _core.TermVisitor

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


logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermVisitor.class_.getName()))
