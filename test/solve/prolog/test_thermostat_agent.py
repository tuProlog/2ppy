import unittest
from typing import Iterable
from pathlib import Path
from tuprolog.core import atom, integer
from tuprolog.unify import mgu
from tuprolog.theory.parsing import parse_theory
from tuprolog.solve import signature
from tuprolog.solve.library import library, Library
from tuprolog.solve.primitive import primitive, Primitive, SolveRequest, SolveResponse, ensuring_argument_is_variable, ensuring_all_arguments_are_instantiated, ensuring_argument_is_atom
from tuprolog.solve.flags import TrackVariables
from tuprolog.solve.channel import output_channel
from tuprolog.solve.prolog import PROLOG_SOLVER_FACTORY


class ThermostatAgent:
    def __init__(self, name: str, cold_threshold: int, hot_threshold: int, initial_temperature: int):
        self.name = name
        self.cold_threshold = cold_threshold
        self.hot_threshold = hot_threshold
        self.initial_temperature = initial_temperature
        self._temperature = initial_temperature

    @property
    def temperature(self) -> int:
        return self._temperature

    def get_temp(self, request: SolveRequest) -> Iterable[SolveResponse]:
        ensuring_argument_is_variable(request, 0)
        sub = mgu(request.arguments[0], integer(self.temperature))
        return [request.reply_with(sub)]

    def push(self, request: SolveRequest) -> SolveResponse:
        ensuring_all_arguments_are_instantiated(request)
        ensuring_argument_is_atom(request, 0)
        arg = request.arguments[0].cast_to_atom().value
        if arg == "hot":
            self._temperature += 1
        elif arg == "cold":
            self._temperature -= 1
        else:
            return request.reply_fail()
        return [request.reply_success()]

    @property
    def library(self) -> Library:
        get_temp = primitive(self.get_temp)
        push = primitive(self.push)
        return library(
            alias="libs.agency.thermostat",
            primitives={
                signature("get_temp", arity=1): get_temp,
                signature("push", arity=1): push
            }
        )

    def program(self) -> str:
        with open(Path(__file__).parent / "thermostat.pl", "r") as f:
            return f.read() \
                .replace("__COLD_THRESHOLD__", str(self.cold_threshold)) \
                .replace("__HOT_THRESHOLD__", str(self.hot_threshold))


class ThermostatAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.thermostat_agent = ThermostatAgent("thermostat", 20, 24, 15)
        self.prints: list[str] = []

    def print_output(self, message):
        message = str(message)
        if len(self.prints) == 0:
            self.prints.append(message)
        elif self.prints[-1].endswith('\n'):
            self.prints.append(message)
        else:
            self.prints[-1] += message

    def test_program(self):
        theory = parse_theory(self.thermostat_agent.program())
        solver_builder = PROLOG_SOLVER_FACTORY.new_builder() \
            .static_kb(theory) \
            .flag(TrackVariables, TrackVariables.ON) \
            .standard_output(output_channel(self.print_output))
        solver_builder = solver_builder.runtime(solver_builder.get_runtime() + self.thermostat_agent.library.to_runtime())
        solver = solver_builder.build()
        solution = solver.solve_once(atom("start"))
        self.assertTrue(solution.is_yes)
        self.assertSequenceEqual(
            self.prints,
            [
                "Temperature is 15.\n", 
                "Pushing hot air.\n", 
                "Temperature is 16.\n", 
                "Pushing hot air.\n", 
                "Temperature is 17.\n", 
                "Pushing hot air.\n", 
                "Temperature is 18.\n", 
                "Pushing hot air.\n", 
                "Temperature is 19.\n", 
                "Pushing hot air.\n", 
                "Temperature is 20.\n", 
                "Pushing hot air.\n", 
                "Temperature is 21.\n", 
                "I'm done.\n"]
        )
