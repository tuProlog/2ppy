"""The command line of the terminal IDE: `2ppy-tui [OPTIONS] [FILE ...]`."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import os
import shlex
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tuprolog import __version__
from tuprolog.core.parsing import parse_term
from tuprolog.gui import solver_profile
from tuprolog.solve.library import Library
from tuprolog.theory import theory
from tuprolog.theory.parsing import parse_theory
from tuprolog.unify import Unificator

from ._bridge import JvmGuiBridge
from ._model import Startup

__all__ = ["ENVIRONMENT_PREFIX", "environment_arguments", "main", "parse_command_line", "parser"]

ENVIRONMENT_PREFIX = "TWOPPY_"
"""The prefix of the environment variables standing for command-line options (see
`environment_arguments`)."""

_MODES = {"one": "ONE", "ten": "TEN", "hundred": "HUNDRED", "all": "ALL"}

EPILOG = """\
library specs: 'io' (ISO Prolog streams), 'oop' (Python objects, see --oop-*), 'oop-jvm' (JVM
objects), or MODULE:NAME / FILE.py:NAME, naming a tuprolog.solve.library.Library, or a callable
returning one (e.g. mylibs:geometry, ./libs.py:make_library).

examples:
  2ppy-tui family.pl -q "ancestor(abe, X)" --solve ten
  2ppy-tui -t "p(1). p(2)." -q "p(X)" --flag unknown=fail
  2ppy-tui --dialect problog -t "0.3::rain. wet :- rain." -q wet --solve
  2ppy-tui --dynamic-kb facts.pl --library io --library mylibs:geometry --no-builtins

environment variables: TWOPPY_<OPTION> stands for --<option> (e.g. TWOPPY_QUERY for --query,
TWOPPY_DYNAMIC_KB for --dynamic-kb), before the command-line arguments: a value for options with
one, true/1/yes/on for those without, space-separated values (shell-quoted) for repeatable ones;
TWOPPY_FILES lists files to open.
"""


def parser() -> argparse.ArgumentParser:
    """The parser of the command-line arguments."""
    result = argparse.ArgumentParser(
        prog="2ppy-tui",
        description="2ppy TUI: a terminal IDE for logic programming, on tuProlog.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    result.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    pages = result.add_argument_group("pages")
    pages.add_argument(
        "files",
        nargs="*",
        type=Path,
        metavar="FILE",
        help="theory files to open, a page each (the static knowledge base of its solver); "
        "missing ones are created on save",
    )
    pages.add_argument(
        "-t", "--theory", metavar="TEXT", help="the theory of a scratch page, as Prolog text"
    )
    pages.add_argument("-q", "--query", metavar="QUERY", help="the query of the initial pages")
    pages.add_argument(
        "-s",
        "--solve",
        nargs="?",
        const="one",
        choices=list(_MODES),
        help="solve the query of the selected page at startup, asking for 1 (the default), 10, "
        "100 or all solutions",
    )
    stdin = pages.add_mutually_exclusive_group()
    stdin.add_argument("--stdin", metavar="TEXT", help="the standard input of the initial pages")
    stdin.add_argument(
        "--stdin-file", type=Path, metavar="FILE", help="read the standard input from a file"
    )
    solvers = result.add_argument_group("solvers")
    solvers.add_argument(
        "--dialect",
        choices=["prolog", "problog"],
        default="prolog",
        help="the logic language (default: prolog)",
    )
    solvers.add_argument(
        "-d",
        "--dynamic-kb",
        action="append",
        type=Path,
        default=[],
        metavar="FILE",
        help="load the clauses of a file into the dynamic knowledge base of every solver "
        "(repeatable)",
    )
    solvers.add_argument(
        "-l",
        "--library",
        action="append",
        default=[],
        metavar="SPEC",
        help="load a library (repeatable; see below); default: io and oop",
    )
    solvers.add_argument(
        "--no-default-libraries",
        action="store_true",
        help="do not load the default libraries, only the --library ones",
    )
    solvers.add_argument(
        "--oop-allow-all-imports",
        action="store_true",
        help="let the oop library import any Python module",
    )
    solvers.add_argument(
        "--oop-allow-private",
        action="store_true",
        help="let the oop library reach private attributes",
    )
    solvers.add_argument(
        "--no-builtins", action="store_true", help="solvers without the standard library"
    )
    solvers.add_argument(
        "--unificator",
        metavar="SPEC",
        help="MODULE:NAME / FILE.py:NAME of a tuprolog.unify.Unificator, or a callable returning one",
    )
    solvers.add_argument(
        "-f",
        "--flag",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="set a flag of every solver, e.g. unknown=fail (repeatable)",
    )
    solvers.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        metavar="SECONDS",
        help="the timeout of resolutions (default: 5)",
    )
    solvers.add_argument(
        "--scheduling",
        choices=["concurrent", "single"],
        default="concurrent",
        help="whether resolutions of different pages run concurrently, or starting one stops "
        "the others (default: concurrent)",
    )
    return result


def _load_object(spec: str) -> Any:
    """The object a `MODULE:NAME` or `FILE.py:NAME` spec names (called, if callable)."""
    source, separator, name = spec.rpartition(":")
    if not separator or not source or not name:
        raise ValueError(f"expected MODULE:NAME or FILE.py:NAME, got {spec!r}")
    if source.endswith(".py"):
        path = Path(source)
        module_spec = importlib.util.spec_from_file_location(path.stem, path)
        if module_spec is None or module_spec.loader is None or not path.is_file():
            raise ValueError(f"no such file: {source}")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
    else:
        module = importlib.import_module(source)
    try:
        value = getattr(module, name)
    except AttributeError:
        raise ValueError(f"{source} has no {name!r}") from None
    return value


def _instance(spec: str, kind: type, kind_name: str) -> Any:
    value = _load_object(spec)
    if not isinstance(value, kind) and callable(value):
        value = value()
    if not isinstance(value, kind):
        raise TypeError(f"{spec} is not a {kind_name}")
    return value


def _libraries(arguments: argparse.Namespace) -> list[Library]:
    from tuprolog.solve.libs import IOLib, oop_lib

    def oop() -> Library:
        return oop_lib(
            allow_all_imports=arguments.oop_allow_all_imports,
            allow_private=arguments.oop_allow_private,
        )

    def jvm_oop() -> Library:
        import it.unibo.tuprolog.solve.libs.oop as jvm  # type: ignore

        return jvm.OOPLib.INSTANCE

    named = {"io": lambda: IOLib, "oop": oop, "oop-jvm": jvm_oop}
    specs = ([] if arguments.no_default_libraries else ["io", "oop"]) + arguments.library
    result: list[Library] = []
    for spec in dict.fromkeys(specs):  # without duplicates, in order
        if spec in named:
            result.append(named[spec]())
        else:
            result.append(_instance(spec, Library, "library"))
    return result


def _flags(specs: list[str]) -> dict[str, str]:
    result = {}
    for spec in specs:
        name, separator, value = spec.partition("=")
        if not separator or not name.strip() or not value.strip():
            raise ValueError(f"expected NAME=VALUE, got {spec!r}")
        parse_term(value)  # raises if not a term
        result[name.strip()] = value.strip()
    return result


def _read(path: Path, missing_ok: bool = False) -> str:
    if missing_ok and not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _split(value: str) -> list[str]:
    """Splits a value at spaces, honouring shell quotes, but not backslashes (e.g. in Windows paths)."""
    lexer = shlex.shlex(value, posix=True)
    lexer.whitespace_split = True
    lexer.escape = ""
    return list(lexer)


def environment_arguments(environ: Mapping[str, str]) -> list[str]:
    """The command-line arguments the environment variables named `TWOPPY_<OPTION>` stand for.

    `<OPTION>` is the long name of an option of `parser` in upper case, with `_` for `-` (e.g.
    `TWOPPY_DYNAMIC_KB` for `--dynamic-kb`). Their values are those of options with one, `true`
    (or `1`, `yes`, `on`) for options without, and space-separated values (quoted as in a shell)
    for repeatable options. `TWOPPY_FILES` lists files to open, as quoted in a shell. Empty
    variables are ignored.

    Args:
        environ: The environment variables, e.g. `os.environ`.

    Returns:
        The arguments.

    Examples:
        >>> environment_arguments({"TWOPPY_QUERY": "p(X)", "TWOPPY_FLAG": "a=1 'b=f(x, y)'"})
        ['--query', 'p(X)', '--flag', 'a=1', '--flag', 'b=f(x, y)']
        >>> environment_arguments({"TWOPPY_NO_BUILTINS": "true", "TWOPPY_FILES": "a.pl b.pl"})
        ['a.pl', 'b.pl', '--no-builtins']
    """
    result: list[str] = []
    for action in parser()._actions:  # the options, as declared
        if isinstance(action, (argparse._HelpAction, argparse._VersionAction)):
            continue
        options = [o for o in action.option_strings if o.startswith("--")]
        name = options[0].removeprefix("--") if options else action.dest
        value = environ.get(ENVIRONMENT_PREFIX + name.upper().replace("-", "_"), "").strip()
        if not value:
            continue
        if not options:
            result += _split(value)
        elif isinstance(action, argparse._StoreTrueAction):
            if value.lower() in ("1", "true", "yes", "on"):
                result.append(options[0])
        elif isinstance(action, argparse._AppendAction):
            for item in _split(value):
                result += [options[0], item]
        else:
            result += [options[0], value]
    return result


def parse_command_line(
    argv: Sequence[str] | None = None, environ: Mapping[str, str] | None = None
) -> tuple[JvmGuiBridge, Startup]:
    """Parses the command-line arguments into a bridge to the GUI application, and a startup.

    Args:
        argv: The arguments; by default, those of the process.
        environ: The environment variables standing for arguments, before them (see
            `environment_arguments`); by default, those of the process.

    Returns:
        The bridge (with the solver profile, flags, timeout and scheduling asked for) and the
        startup (the pages, query and standard input asked for).

    Raises:
        SystemExit: If the arguments are invalid (after printing why), or after printing the help
            or the version.
    """
    command = parser()
    arguments = command.parse_intermixed_args(
        environment_arguments(os.environ if environ is None else environ)
        + list(sys.argv[1:] if argv is None else argv)
    )
    try:
        if arguments.timeout <= 0:
            raise ValueError("the timeout must be positive")
        documents = tuple(
            (path.absolute(), _read(path, missing_ok=True)) for path in arguments.files
        )
        clauses = [c for path in arguments.dynamic_kb for c in parse_theory(_read(path))]
        stdin = _read(arguments.stdin_file) if arguments.stdin_file is not None else arguments.stdin
        unificator = (
            None
            if arguments.unificator is None
            else _instance(arguments.unificator, Unificator, "unificator")
        )
        profile = solver_profile(
            dialect=arguments.dialect,
            libraries=_libraries(arguments),
            dynamic_kb=theory(clauses),
            unificator=unificator,
            builtins=not arguments.no_builtins,
        )
        bridge = JvmGuiBridge(
            profiles=[profile],
            timeout=arguments.timeout,
            flags=_flags(arguments.flag),
            scheduling=arguments.scheduling,
        )
    except Exception as error:  # noqa: BLE001  (reported as a usage error)
        command.error(str(error))
    startup = Startup(
        documents=documents,
        theory=arguments.theory,
        query=arguments.query,
        stdin=stdin,
        solve=None if arguments.solve is None else _MODES[arguments.solve],  # type: ignore[arg-type]
    )
    return bridge, startup


def main(argv: Sequence[str] | None = None) -> None:
    """Runs the terminal IDE, as asked by the command-line arguments (see `parser`)."""
    from ._app import PrologTui

    bridge, startup = parse_command_line(argv)
    PrologTui(bridge, startup).run()
