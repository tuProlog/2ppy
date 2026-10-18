from jpype import JImplementationFor

from tuprolog import logger
from tuprolog.jvmioutils import ensure_input_stream


@JImplementationFor("it.unibo.tuprolog.core.parsing.TermParser")
class _KtTermParser:
    def __jclass_init__(cls):
        pass

    @property
    def default_operator_set(self):
        """The operators the parser uses when not given others."""
        return self.getDefaultOperatorSet()

    def _parse(self, method, input, operators):
        if operators is None:
            return method(input)
        else:
            return method(input, operators)

    def parse(self, input, operators=None):
        """Parses a term (an alias of `parse_term`).

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The term.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
        """
        return self.parse_term(input, operators)

    def parse_term(self, input, operators=None):
        """Parses a term.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The term.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
        """
        return self._parse(self.parseTerm, input, operators)

    def parse_struct(self, input, operators=None):
        """Parses a structure.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The structure.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseStruct, input, operators)

    def parse_constant(self, input, operators=None):
        """Parses a constant (an atom or a number).

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The constant.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseConstant, input, operators)

    def parse_var(self, input, operators=None):
        """Parses a variable.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The variable.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseVar, input, operators)

    def parse_atom(self, input, operators=None):
        """Parses an atom.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The atom.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseAtom, input, operators)

    def parse_numeric(self, input, operators=None):
        """Parses a number.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The number.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseNumeric, input, operators)

    def parse_integer(self, input, operators=None):
        """Parses an integer.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The integer.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseInteger, input, operators)

    def parse_real(self, input, operators=None):
        """Parses a real number.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The real.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseReal, input, operators)

    def parse_clause(self, input, operators=None):
        """Parses a clause: a rule or fact with an explicit `:-`, or a directive `:- goal`.

        Args:
            input: the text, in Prolog syntax, without the final `.`.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The clause.

        Raises:
            ParseException: if `input` is not valid Prolog syntax.
            InvalidTermTypeException: if `input` is valid, but represents another kind of term.
        """
        return self._parse(self.parseClause, input, operators)


@JImplementationFor("it.unibo.tuprolog.core.parsing.TermReader")
class _KtTermReader:
    def __jclass_init__(cls):
        pass

    @property
    def default_operator_set(self):
        """The operators the reader uses when not given others."""
        return self.getDefaultOperatorSet()

    def _read(self, method, input, operators):
        input_stream = ensure_input_stream(input)
        if operators is None:
            return method(input_stream)
        else:
            return method(input_stream, operators)

    def read(self, input, operators=None):
        """Reads the first term (an alias of `read_term`).

        Args:
            input: a Python stream (binary or text), a JVM `InputStream`, or a file path. It is
                closed once read.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The first term, or `None` if there is none.

        Raises:
            ParseException: if the text is not valid Prolog syntax.
        """
        return self.read_term(input, operators)

    def read_term(self, input, operators=None):
        """Reads the first term, ending with `.`.

        Args:
            input: a Python stream (binary or text), a JVM `InputStream`, or a file path. It is
                closed once read.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The first term, or `None` if there is none.

        Raises:
            ParseException: if the text is not valid Prolog syntax.
        """
        return self._read(self.readTerm, input, operators)

    def read_all(self, input, operators=None):
        """Reads all the terms, lazily (an alias of `read_terms`).

        Args:
            input: a Python stream (binary or text), a JVM `InputStream`, or a file path. It is
                closed once read.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The terms, as a lazy iterable, to consume once.

        Raises:
            ParseException: if the text is not valid Prolog syntax (while iterating).
        """
        return self.read_terms(input, operators)

    def read_terms(self, input, operators=None):
        """Reads all the terms, each ending with `.`, lazily.

        Args:
            input: a Python stream (binary or text), a JVM `InputStream`, or a file path. It is
                closed once read.
            operators: the operators to parse with, replacing the parser's default ones (so pass
                e.g. `DEFAULT_OPERATORS + custom` to add operators). If `None`, the parser's default
                ones.

        Returns:
            The terms, as a lazy iterable, to consume once.

        Raises:
            ParseException: if the text is not valid Prolog syntax (while iterating).
        """
        return self._read(self.readTerms, input, operators)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.parsing.*")
