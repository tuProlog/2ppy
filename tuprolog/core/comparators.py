import logging
import jpype
import jpype.imports

# from tuprolog.pyutils import iterable_or_varargs
# from tuprolog.jvmutils import jiterable, jmap

from tuprolog.core import TermComparator

logging.debug("Loaded compatibility layer for JVM subtypes of " + str(TermComparator.class_.getName()))


@jpype.JImplements(TermComparator)
class AbstractTermComparator(object):
    @jpype.JOverride
    def equals(self, other):
        return self is other

    @jpype.JOverride
    def compare(self, first, second):
        raise NotImplementedError()
