import logging
import jpype
import jpype.imports

from it.unibo.tuprolog.core import Atom
from it.unibo.tuprolog.core import Block
from it.unibo.tuprolog.core import Clause
from it.unibo.tuprolog.core import Cons
from it.unibo.tuprolog.core import Constant
from it.unibo.tuprolog.core import Directive
from it.unibo.tuprolog.core import Empty
from it.unibo.tuprolog.core import EmptyBlock
from it.unibo.tuprolog.core import EmptyList
from it.unibo.tuprolog.core import Fact
from it.unibo.tuprolog.core import Formatter
from it.unibo.tuprolog.core import Indicator
from it.unibo.tuprolog.core import Integer
from it.unibo.tuprolog.core import List
from it.unibo.tuprolog.core import Numeric
from it.unibo.tuprolog.core import Real
from it.unibo.tuprolog.core import Recursive
from it.unibo.tuprolog.core import Rule
from it.unibo.tuprolog.core import Scope
from it.unibo.tuprolog.core import Struct
from it.unibo.tuprolog.core import Substitution
from it.unibo.tuprolog.core import Term
from it.unibo.tuprolog.core import TermComparator
from it.unibo.tuprolog.core import TermConvertible
from it.unibo.tuprolog.core import TermFormatter
from it.unibo.tuprolog.core import Terms
from it.unibo.tuprolog.core import TermVisitor
from it.unibo.tuprolog.core import Truth
from it.unibo.tuprolog.core import Tuple
from it.unibo.tuprolog.core import Var

logging.debug("Loaded JVM classes from it.unibo.tuprolog.core.*")


@jpype.JImplements(Formatter)
class AbstractFormatter(object):
    @jpype.JOverride
    def format(self, term):
        raise NotImplementedError()

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

@jpype.JImplements(TermComparator)
class AbstractTermComparator(object):
    @jpype.JOverride
    def equals(self, other):
        return self is other

    @jpype.JOverride
    def compare(self, first, second):
        raise NotImplementedError()

@jpype.JImplements(TermConvertible)
class AbstractTermConvertible(object):
    @jpype.JOverride
    def toTerm(self):
        raise NotImplementedError()

# def atom(string) -> Atom:
#     Atom.of(string)

# def block(terms):
#     list

# def clause():
#     pass

# def cons(head, tail=):
#     pass

# def directive():
#     pass

# def empty_block():
#     pass

# def empty_logic_list():
#     pass

# def fact():
#     pass

# def indicator():
#     pass

# def integer():
#     pass

# def logic_list():
#     pass

# def numeric():
#     pass

# def real():
#     pass

# def rule():
#     pass

# def struct():
#     pass

# def truth():
#     pass

# def logic_tuple():
#     pass

# def var():
#     pass
