from tuprolog import logger
import jpype

from tuprolog.jvmioutils import ensure_input_steam


@jpype.JImplementationFor("it.unibo.tuprolog.core.parsing.TermParser")
class _KtTermParser:
    def __jclass_init__(cls):
        pass

    @property
    def default_operator_set(self):
        return self.getDefaultOperatorSet()

    def _parse(self, method, input, operators):
        if operators is None:
            return method(input)
        else:
            return method(input, operators)

    def parse(self, input, operators=None):
        return self.parse_term(input, operators)

    def parse_term(self, input, operators=None):
        return self._parse(self.parseTerm, input, operators)

    def parse_struct(self, input, operators=None):
        return self._parse(self.parseStruct, input, operators)

    def parse_constant(self, input, operators=None):
        return self._parse(self.parseConstant, input, operators)

    def parse_var(self, input, operators=None):
        return self._parse(self.parseVar, input, operators)

    def parse_atom(self, input, operators=None):
        return self._parse(self.parseAtom, input, operators)

    def parse_numeric(self, input, operators=None):
        return self._parse(self.parseNumeric, input, operators)

    def parse_integer(self, input, operators=None):
        return self._parse(self.parseInteger, input, operators)

    def parse_real(self, input, operators=None):
        return self._parse(self.parseReal, input, operators)

    def parse_clause(self, input, operators=None):
        return self._parse(self.parseClause, input, operators)


@jpype.JImplementationFor("it.unibo.tuprolog.core.parsing.TermReader")
class _KtTermReader:
    def __jclass_init__(cls):
        pass

    @property
    def default_operator_set(self):
        return self.getDefaultOperatorSet()

    def _read(self, method, input, operators):
        input_stream = ensure_input_steam(input)
        if operators is None:
            return method(input_stream)
        else:
            return method(input_stream, operators)

    def read(self, input, operators=None):
        return self.read_term(input, operators)

    def read_term(self, input, operators=None):
        return self._read(self.readTerm, input, operators)

    def read_all(self, input, operators=None):
        return self.read_terms(input, operators)

    def read_terms(self, input, operators=None):
        return self._read(self.readTerms, input, operators)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.parsing.*")
