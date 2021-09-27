from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype
import jpype.imports
from tuprolog.core import Formatter, TermFormatter
from tuprolog.core.visitors import AbstractTermVisitor


@jpype.JImplements(Formatter)
class AbstractFormatter(object):
    @jpype.JOverride
    def format(self, term):
        raise NotImplementedError()


@jpype.JImplements(TermFormatter)
class AbstractTermFormatter(AbstractFormatter, AbstractTermVisitor):
    @jpype.JOverride
    def format(self, term):
        return term.accept(self)

    @jpype.JOverride
    def defaultValue(self, term):
        return super(AbstractTermVisitor).defaultValue(self, term)

    @jpype.JOverride
    def visitTerm(self, term):
        return super(AbstractTermVisitor, self).visitTerm(term)

    @jpype.JOverride
    def visitVar(self, term):
        return super(AbstractTermVisitor, self).visitVar(term)

    @jpype.JOverride
    def visitConstant(self, term):
        return super(AbstractTermVisitor, self).visitConstant(term)

    @jpype.JOverride
    def visitStruct(self, term):
        return super(AbstractTermVisitor, self).visitStruct(term)

    @jpype.JOverride
    def visitCollection(self, term):
        return super(AbstractTermVisitor, self).visitCollection(term)

    @jpype.JOverride
    def visitAtom(self, term):
        return super(AbstractTermVisitor, self).visitAtom(term)

    @jpype.JOverride
    def visitTruth(self, term):
        return super(AbstractTermVisitor, self).visitTruth(term)

    @jpype.JOverride
    def visitNumeric(self, term):
        return super(AbstractTermVisitor, self).visitNumeric(term)

    @jpype.JOverride
    def visitInteger(self, term):
        return super(AbstractTermVisitor, self).visitInteger(term)

    @jpype.JOverride
    def visitReal(self, term):
        return super(AbstractTermVisitor, self).visitReal(term)

    @jpype.JOverride
    def visitBlock(self, term):
        return super(AbstractTermVisitor, self).visitBlock(term)

    @jpype.JOverride
    def visitEmpty(self, term):
        return super(AbstractTermVisitor, self).visitEmpty(term)

    @jpype.JOverride
    def visitEmptyBlock(self, term):
        return super(AbstractTermVisitor, self).visitEmptyBlock(term)

    @jpype.JOverride
    def visitList(self, term):
        return super(AbstractTermVisitor, self).visitList(term)

    @jpype.JOverride
    def visitCons(self, term):
        return super(AbstractTermVisitor, self).visitCons(term)

    @jpype.JOverride
    def visitEmptyList(self, term):
        return super(AbstractTermVisitor, self).visitEmptyList(term)

    @jpype.JOverride
    def visitTuple(self, term):
        return super(AbstractTermVisitor, self).visitTuple(term)

    @jpype.JOverride
    def visitIndicator(self, term):
        return super(AbstractTermVisitor, self).visitIndicator(term)

    @jpype.JOverride
    def visitClause(self, term):
        return super(AbstractTermVisitor, self).visitClause(term)

    @jpype.JOverride
    def visitRule(self, term):
        return super(AbstractTermVisitor, self).visitRule(term)

    @jpype.JOverride
    def visitFact(self, term):
        return super(AbstractTermVisitor, self).visitFact(term)

    @jpype.JOverride
    def visitDirective(self, term):
        return super(AbstractTermVisitor, self).visitDirective(term)


logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermFormatter.class_.getName()))
