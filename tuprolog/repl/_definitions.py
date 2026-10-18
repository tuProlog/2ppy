from __future__ import annotations

from cmd import Cmd
from typing import IO

from jpype import JException

from tuprolog.core import pretty_expressions_formatter
from tuprolog.core.parsing import ParseException, TermParser
from tuprolog.solve import SolutionFormatter, Solver, solution_formatter, solve_options
from tuprolog.solve.exception import HaltException
from tuprolog.solve.plp import probability
from tuprolog.theory.parsing import ClausesParser

__all__ = ["PrologREPL"]


_PROBLOG_PACKAGE = "it.unibo.tuprolog.solve.problog."


def _is_command(line: str) -> bool:
    return line.startswith(":") and not line.startswith(":-")


class PrologREPL(Cmd):
    use_rawinput = False

    def __init__(
        self,
        solver: Solver,
        name: str,
        completekey: str = "tab",
        stdin: IO[str] | None = None,
        stdout: IO[str] | None = None,
        probabilistic: bool | None = None,
    ):
        """`probabilistic` queries show their probability; by default, it holds for ProbLog solvers."""
        super().__init__(completekey, stdin, stdout)
        self.intro = f"""
Welcome to the {name.title()} REPL.
    Usage
        Assert a clause by typing it in.
        Query the theory by typing ?- followed by a query.
        Clauses and queries must end with a period, otherwise they will be
            considered incomplete and you will be prompted for more input.
        Run a directive by typing :- followed by a goal.
        Type ":help" for more information, including the list of available
            commands that can be used by prefixing a colon ":".
        Type ":exit" to exit.
"""
        self.solver = solver
        self.name = name
        self.multi_line_command = ""
        if probabilistic is None:
            probabilistic = str(solver.getClass().getName()).startswith(_PROBLOG_PACKAGE)
        self.probabilistic = probabilistic

    # parsers and formatter follow the solver's current operators, e.g. after ?- op(...).
    @property
    def clauses_parser(self) -> ClausesParser:
        return ClausesParser.withOperators(self.solver.operators)

    @property
    def query_parser(self) -> TermParser:
        return TermParser.withOperators(self.solver.operators)

    @property
    def solution_formatter(self) -> SolutionFormatter:
        return solution_formatter(pretty_expressions_formatter(operators=self.solver.operators))

    @property  # Cmd reads the prompt as an attribute: a property computes it
    def prompt(self) -> str:  # type: ignore[override]
        return "...>" if self.multi_line_command else f"{self.name}>"

    def emptyline(self) -> bool:
        return False  # never repeat the last command, as Cmd does by default

    def precmd(self, line: str) -> str:
        if line == "EOF":
            return ":exit"
        if not line.strip() and not self.multi_line_command:
            return ""
        if _is_command(line):
            return line
        if line.rstrip().endswith("."):
            command = self.multi_line_command + line
            self.multi_line_command = ""
            return command
        self.multi_line_command += line + "\n"
        return ""

    def do_exit(self, arg: str) -> bool:
        """Exit the REPL."""
        return True

    def parseline(self, line: str) -> tuple[str | None, str | None, str]:
        line = line.strip()
        if _is_command(line):
            return super().parseline(line[1:])
        if line.startswith("?-"):
            return "query", line[2:].strip(), line
        if line.startswith(":-"):
            return "directive", line[2:].strip(), line
        return "assert", line, line

    def do_query(self, arg: str) -> bool:
        """Query the theory."""
        try:
            query = self.query_parser.parse_struct(arg)
            options = solve_options(probabilistic=self.probabilistic)
            for solution in self.solver.solve(query, options):
                if solution.is_halt and isinstance(solution.getException(), HaltException):
                    self.stdout.write("# goodbye.\n")  # like 2P-Kt's REPL, halt/0,1 exit
                    return True
                formatted = str(self.solution_formatter.format(solution))
                self.stdout.write(formatted)
                if self.probabilistic and solution.is_yes:
                    self.stdout.write(f"\n    probability: {probability(solution)}")
                self.stdout.write("\n")
        except ParseException as e:
            self.on_parsing_error(e)
        return False

    def do_directive(self, arg: str) -> bool:
        """Runs a directive (:- goal.), reporting only its failures."""
        try:
            goal = self.query_parser.parse_struct(arg)
            solution = self.solver.solve_once(goal)
            if solution.is_halt and isinstance(solution.getException(), HaltException):
                self.stdout.write("# goodbye.\n")
                return True
            if not solution.is_yes:
                self.stdout.write(str(self.solution_formatter.format(solution)))
                self.stdout.write("\n")
        except ParseException as e:
            self.on_parsing_error(e)
        return False

    def do_assert(self, arg: str) -> bool:
        """Asserts a clause, appending to the theory."""
        try:
            clauses = self.clauses_parser.parseClauses(arg)
            for clause in clauses:
                self.solver.assertZ(clause)
        except ParseException as e:
            self.on_parsing_error(e)
        except JException as e:  # e.g. clauses the knowledge base rejects
            self.stdout.write(f"Error: {e.getMessage()}\n")
        return False

    def on_parsing_error(self, err: ParseException) -> None:
        self.stdout.write(f"Error: {err.message}\n")
