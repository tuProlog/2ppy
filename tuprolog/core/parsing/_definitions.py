from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.core.parsing as _parsing  # type: ignore

TermParser = _parsing.TermParser


TermReader = _parsing.TermReader


ParseException = _parsing.ParseException


InvalidTermTypeException = _parsing.InvalidTermTypeException


DEFAULT_TERM_PARSER = TermParser.withDefaultOperators()


DEFAULT_TERM_READER = TermReader.withDefaultOperators()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.parsing.*")
