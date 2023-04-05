from tuprolog import logger
import jpype

from tuprolog.jvmioutils import ensure_input_steam


@jpype.JImplementationFor("it.unibo.tuprolog.theory.parsing.ClausesParser")
class _KtClausesParser:
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

    def parse_theory(self, input, operators):
        return self._parse(self.parseTheory, input, operators)

    def parse_clauses_lazily(self, input, operators):
        return self._parse(self.parseClausesLazily, input, operators)

    def parse_clauses(self, input, operators):
        return list(self.parse_clauses_lazily(input, operators))



@jpype.JImplementationFor("it.unibo.tuprolog.theory.parsing.ClausesReader")
class _KtClausesReader:
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

    def read_theory(self, input, operators):
        return self._read(self.readTheory, input, operators)

    def read_clauses_lazily(self, input, operators):
        return self._read(self.readClausesLazily, input, operators)

    def read_clauses(self, input, operators):
        return list(self.read_clauses_lazily(input, operators))


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.theory.parsing.*")
