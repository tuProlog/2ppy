"""The Prolog REPL, built on Python's `cmd` module."""

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
    r"""A read-eval-print loop (REPL) for a logic solver.

    It is a `cmd.Cmd` shell: `cmdloop()` runs it, reading lines from its input until `:exit`, the
    end of the input, or a query halting the solver (e.g. `halt.`). Each input is:

    - a query, if it starts with `?-`: all its solutions are printed (see `do_query`);
    - a directive, if it starts with `:-`: it is run, printing its outcome only if it does not
      succeed (see `do_directive`);
    - a command, if it starts with `:` (e.g. `:help`, `:exit`);
    - a sequence of clauses, otherwise: they are added to the end of the solver's dynamic
      knowledge base (see `do_assert`).

    Queries, directives and clauses end with a full stop: until one is typed, lines are
    accumulated, and the prompt becomes `...>`. Parsing follows the solver's current operators,
    so operators defined by directives (e.g. `:- op(700, xfx, likes).`) are recognized afterward.

    Attributes:
        solver: The solver answering queries; it should have a mutable knowledge base, for
            clauses to be added.
        name: The name of the language, shown in the prompt (e.g. `prolog>`) and introduction.
        probabilistic: Whether queries are solved probabilistically, showing the probability of
            each successful solution.
        multi_line_command: The input accumulated so far, while waiting for a full stop.

    Examples:
        >>> import io
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> user_input = io.StringIO("p(1). p(2).\n?- p(\n  X).\n")
        >>> output = io.StringIO()
        >>> solver = prolog_solver(mutable=True)
        >>> repl = PrologREPL(solver, "prolog", stdin=user_input, stdout=output)
        >>> repl.cmdloop(intro="")
        >>> print(output.getvalue())
        prolog>prolog>...>yes: p(1)
            X = 1
        yes: p(2)
            X = 2
        prolog>
    """

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
        """Creates a REPL for a solver.

        Args:
            solver: The solver answering queries (see `tuprolog.solve`), preferably with a mutable
                knowledge base.
            name: The name of the language, shown in the prompt and introduction.
            completekey: The key completing commands (see `cmd.Cmd`).
            stdin: The input to read from (`sys.stdin`, unless given).
            stdout: The output to write to (`sys.stdout`, unless given).
            probabilistic: Whether queries show the probability of their solutions; if None (the
                default), they do for ProbLog solvers (see `tuprolog.solve.problog`).
        """
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
        """The parser of clauses, knowing the solver's current operators."""
        return ClausesParser.withOperators(self.solver.operators)

    @property
    def query_parser(self) -> TermParser:
        """The parser of queries and directives, knowing the solver's current operators."""
        return TermParser.withOperators(self.solver.operators)

    @property
    def solution_formatter(self) -> SolutionFormatter:
        """The formatter of solutions, writing terms with the solver's current operators."""
        return solution_formatter(pretty_expressions_formatter(operators=self.solver.operators))

    @property  # Cmd reads the prompt as an attribute: a property computes it
    def prompt(self) -> str:  # type: ignore[override]
        """The prompt: the language name (e.g. `prolog>`), or `...>` while input is incomplete."""
        return "...>" if self.multi_line_command else f"{self.name}>"

    def emptyline(self) -> bool:
        """Does nothing on empty lines (`cmd.Cmd` would repeat the last command)."""
        return False  # never repeat the last command, as Cmd does by default

    def precmd(self, line: str) -> str:
        """Accumulates lines until a full stop ends the input.

        Args:
            line: The line read.

        Returns:
            The whole input, once it ends with a full stop, or the line itself, if it is a
            command; an empty string while input is incomplete. The end of the input becomes
            `:exit`.
        """
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
        """Splits the input into the command to run (`query`, `directive`, `assert`, or the one
        following `:`), its argument, and the input itself."""
        line = line.strip()
        if _is_command(line):
            return super().parseline(line[1:])
        if line.startswith("?-"):
            return "query", line[2:].strip(), line
        if line.startswith(":-"):
            return "directive", line[2:].strip(), line
        return "assert", line, line

    def do_query(self, arg: str) -> bool:
        """Query the theory.

        Prints every solution of the query, with its variable bindings (and probability, if
        `probabilistic`), or `no.` if there is none; type `?- query.` to run it.

        Returns:
            True (ending the REPL) if the query halted the solver, False otherwise.
        """
        try:
            query = self.query_parser.parse_struct(arg)
            options = solve_options(probabilistic=self.probabilistic)
            for solution in self.solver.solve(query, options):
                if solution.is_halt and isinstance(solution.getException(), HaltException):
                    self.stdout.write("# goodbye.\n")  # like 2P-Kt's REPL, halt/0,1 exit
                    return True
                # 2P-Kt's formatter leaves an indented empty line when there are no bindings
                formatted = str(self.solution_formatter.format(solution)).rstrip()
                self.stdout.write(formatted)
                if self.probabilistic and solution.is_yes:
                    self.stdout.write(f"\n    probability: {probability(solution)}")
                self.stdout.write("\n")
        except ParseException as e:
            self.on_parsing_error(e)
        return False

    def do_directive(self, arg: str) -> bool:
        """Runs a directive (:- goal.), reporting only its failures.

        Returns:
            True (ending the REPL) if the directive halted the solver, False otherwise.
        """
        try:
            goal = self.query_parser.parse_struct(arg)
            solution = self.solver.solve_once(goal)
            if solution.is_halt and isinstance(solution.getException(), HaltException):
                self.stdout.write("# goodbye.\n")
                return True
            if not solution.is_yes:
                self.stdout.write(str(self.solution_formatter.format(solution)).rstrip())
                self.stdout.write("\n")
        except ParseException as e:
            self.on_parsing_error(e)
        return False

    def do_assert(self, arg: str) -> bool:
        """Asserts a clause, appending to the theory.

        All the clauses in the input are added to the end of the solver's dynamic knowledge base;
        clauses which cannot be parsed or added are reported as errors.

        Returns:
            False, as asserting never ends the REPL.
        """
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
        """Reports input which is not valid Prolog, writing the parser's message."""
        self.stdout.write(f"Error: {err.message}\n")
