from cmd import Cmd
from typing import IO
from tuprolog.core.parsing import TermParser, ParseException
from tuprolog.theory.parsing import ClausesParser
from tuprolog.solve import solution_formatter, TermFormatter
from tuprolog.solve import Solver


class PrologREPL(Cmd):
    use_rawinput = False

    def __init__(self,
                 solver: Solver,
                 name: str,
                 completekey: str = "tab",
                 stdin: IO[str] | None = None,
                 stdout: IO[str] | None = None):
        super().__init__(completekey, stdin, stdout)
        self.intro = f"""
Welcome to the {name} REPL.
    Usage
        Assert a clause by typing it in.
        Query the theory by typing ?- followed by a query.
        Type ":help" for more information.
        Type ":exit" to exit.
"""
        self.solver = solver
        self.name = name
        self.clauses_parser = ClausesParser.withOperators(self.solver.operators)
        self.query_parser = TermParser.withOperators(self.solver.operators)
        self.solution_formatter = solution_formatter(TermFormatter.prettyExpressions(self.solver.operators))
        self.multi_line_command = ""

    @property
    def prompt(self) -> str:
        return "...>" if self.multi_line_command else f"{self.name}>"

    def emptyline(self) -> bool:
        if self.multi_line_command:
            return False
        return super().emptyline()

    def precmd(self, line: str) -> str:
        if line.startswith(":") or line.endswith("."):
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
        if line.startswith(":"):
            return super().parseline(line[1:])
        if line.startswith("?-"):
            return "query", line[2:].strip(), line
        return "assert", line, line

    def do_query(self, arg: str) -> bool:
        """Query the theory."""
        try:
            query = self.query_parser.parse_struct(arg)
            solutions = self.solver.solve(query)
            for solution in solutions:
                formatted = str(self.solution_formatter.format(solution))
                self.stdout.write(formatted)
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
        return False

    def on_parsing_error(self, err: ParseException) -> None:
        self.stdout.write(f"Error: {err.message}\n".replace("'<EOF>'", "end of input"))
