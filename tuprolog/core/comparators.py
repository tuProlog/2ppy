from tuprolog import logger

import jpype

from tuprolog.core import TermComparator


@jpype.JImplements(TermComparator)
class AbstractTermComparator(object):
    @jpype.JOverride
    def equals(self, other):
        return self is other

    @jpype.JOverride
    def compare(self, first, second):
        raise NotImplementedError()


logger.debug("Loaded compatibility layer for JVM subtypes of " + str(TermComparator.class_.getName()))
