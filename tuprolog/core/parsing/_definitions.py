import it.unibo.tuprolog.core.parsing as _parsing  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "DEFAULT_TERM_PARSER",
    "DEFAULT_TERM_READER",
    "InvalidTermTypeException",
    "ParseException",
    "TermParser",
    "TermReader",
]


TermParser = _parsing.TermParser


TermReader = _parsing.TermReader


ParseException = _parsing.ParseException


InvalidTermTypeException = _parsing.InvalidTermTypeException


DEFAULT_TERM_PARSER = TermParser.withDefaultOperators()


DEFAULT_TERM_READER = TermReader.withDefaultOperators()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.parsing.*")
