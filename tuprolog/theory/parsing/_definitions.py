from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.theory.parsing as _parsing  # type: ignore


ClausesParser = _parsing.ClausesParser


ClausesReader = _parsing.ClausesReader


DEFAULT_CLAUSES_PARSER = ClausesParser.withDefaultOperators()


DEFAULT_CLAUSES_READER = ClausesReader.withDefaultOperators()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.theory.parsing.*")
