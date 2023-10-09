from jpype import JImplements, JOverride
from tuprolog import logger
from tuprolog.core import TermComparator

@JImplements(TermComparator)
class AbstractTermComparator(object):
    @JOverride
    def equals(self, other):
        return self is other

    @JOverride
    def compare(self, first, second):
        raise NotImplementedError()


logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermComparator.class_.getName()))
