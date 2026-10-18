"""Pythonic methods for theory parsers and readers."""

from jpype import JImplementationFor

from tuprolog import logger
from tuprolog.jvmioutils import ensure_input_steam


@JImplementationFor("it.unibo.tuprolog.theory.parsing.ClausesParser")
class _KtClausesParser:
    def __jclass_init__(cls):
        pass

    @property
    def default_operator_set(self):
        """The operators known by default (a `tuprolog.core.operators.OperatorSet`)."""
        return self.getDefaultOperatorSet()

    def _parse(self, method, input, operators):
        if operators is None:
            return method(input)
        else:
            return method(input, operators)

    def parse_theory(self, input, operators=None):
        """Parses a string into a `tuprolog.theory.Theory`.

        Args:
            input: The Prolog source code.
            operators: The operators to use, instead of the default ones, if not None.

        Raises:
            ParsingError: If `input` is not valid Prolog.
        """
        return self._parse(self.parseTheory, input, operators)

    def parse_clauses_lazily(self, input, operators=None):
        """Parses a string into a lazy iterable of clauses, parsing each one when reached."""
        return self._parse(self.parseClausesLazily, input, operators)

    def parse_clauses(self, input, operators=None):
        """Parses a string into a list of clauses (see `parse_theory` for the arguments)."""
        return list(self.parse_clauses_lazily(input, operators))


@JImplementationFor("it.unibo.tuprolog.theory.parsing.ClausesReader")
class _KtClausesReader:
    def __jclass_init__(cls):
        pass

    @property
    def default_operator_set(self):
        """The operators known by default (a `tuprolog.core.operators.OperatorSet`)."""
        return self.getDefaultOperatorSet()

    def _read(self, method, input, operators):
        input_stream = ensure_input_steam(input)
        if operators is None:
            return method(input_stream)
        else:
            return method(input_stream, operators)

    def read_theory(self, input, operators=None):
        """Reads a `tuprolog.theory.Theory` from a file or stream.

        Args:
            input: A path, a Python stream, or a JVM input stream.
            operators: The operators to use, instead of the default ones, if not None.

        Raises:
            ParsingError: If the input is not valid Prolog.
        """
        return self._read(self.readTheory, input, operators)

    def read_clauses_lazily(self, input, operators=None):
        """Reads a lazy iterable of clauses from a file or stream, reading each one when reached."""
        return self._read(self.readClausesLazily, input, operators)

    def read_clauses(self, input, operators=None):
        """Reads a list of clauses from a file or stream (see `read_theory` for the arguments)."""
        return list(self.read_clauses_lazily(input, operators))


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.theory.parsing.*")
