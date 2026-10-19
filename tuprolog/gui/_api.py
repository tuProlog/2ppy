"""Pythonic factories of GUI applications, re-exported by `tuprolog.gui`."""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable, Mapping
from os import PathLike
from pathlib import Path
from typing import Any, Literal

import it.unibo.tuprolog.ppy.gui as _ppy_gui  # type: ignore
import it.unibo.tuprolog.ui.gui.presentation as _presentation  # type: ignore
import it.unibo.tuprolog.ui.gui.solver as _solver  # type: ignore
from jpype import JOverride

from tuprolog.core import Term
from tuprolog.jvmutils import jimplements, jlist, jmap
from tuprolog.solve.library import Library
from tuprolog.theory import Theory, theory
from tuprolog.unify import Unificator

from ._definitions import DocumentOrigin, GuiFacade, SolverProfile

__all__ = [
    "PATH_PROVIDER",
    "documentation_preview",
    "gui_application",
    "origin_path",
    "path_origin",
    "prolog_gui",
    "solver_profile",
]

Dialect = Literal["prolog", "problog"]
"""The logic languages of solver profiles."""

Scheduling = Literal["concurrent", "single"]
"""Whether resolutions of different pages may run concurrently (`"concurrent"`), or starting one
stops the others (`"single"`)."""

_SCHEDULING = {
    "concurrent": _solver.ResolutionSchedulingPolicy.PER_PAGE_CONCURRENT,
    "single": _solver.ResolutionSchedulingPolicy.SINGLE_ACTIVE_RESOLUTION,
}

PATH_PROVIDER = "path"
"""The provider id of the `DocumentOrigin`s of files, whose reference is the file's path."""

_logger = logging.getLogger("tuprolog.gui")


@jimplements("java.util.function.Consumer", deferred=True)
class _Consumer:
    """A JVM `Consumer` calling a Python callable."""

    def __init__(self, function: Callable[[Any], Any]) -> None:
        self._function = function

    @JOverride
    def accept(self, value: Any) -> None:
        self._function(value)


def _log_error(error: Any) -> None:
    _logger.error("Error in the GUI application: %s", error, exc_info=isinstance(error, Exception))


def _default_libraries() -> list[Library]:
    from tuprolog.solve.libs import IOLib, OOPLib

    return [IOLib, OOPLib]


def solver_profile(
    dialect: Dialect = "prolog",
    libraries: Iterable[Library] | None = None,
    dynamic_kb: Theory | None = None,
    unificator: Unificator | None = None,
    builtins: bool = True,
) -> SolverProfile:
    """Creates a solver profile: how the solvers of GUI pages are built.

    The static knowledge base of each page's solver is the page's text; everything else comes
    from the profile, every time a solver is (re)built, e.g. after a reset.

    Args:
        dialect: The logic language: `"prolog"` (ISO Prolog) or `"problog"` (probabilistic
            logic programming: solutions show their probability).
        libraries: The libraries loaded on top of the standard one; by default,
            `tuprolog.solve.libs.IOLib` and `tuprolog.solve.libs.OOPLib` (Python objects).
        dynamic_kb: The initial dynamic knowledge base of every solver; empty by default.
        unificator: The unificator of the solvers; by default, the standard one.
        builtins: Whether the solvers have the standard library (e.g. `member/2`, `is/2`).

    Returns:
        The profile, for `gui_application`.

    Examples:
        >>> from tuprolog.theory.parsing import parse_theory
        >>> profile = solver_profile(dynamic_kb=parse_theory("counter(0)."))
        >>> str(profile.display_name)
        'Prolog'

    Note:
        Wraps 2PPy's `SolverProfiles.of`, on top of 2P-Kt's `solverFactoryProfile`.
    """
    if dialect not in ("prolog", "problog"):
        raise ValueError(f"Unknown dialect: {dialect}")
    arguments = (
        jlist(_default_libraries() if libraries is None else list(libraries)),
        theory() if dynamic_kb is None else dynamic_kb,
        unificator,
        builtins,
    )
    profiles = _ppy_gui.SolverProfiles.INSTANCE
    return profiles.prolog(*arguments) if dialect == "prolog" else profiles.problog(*arguments)


def gui_application(
    on_state: Callable[[Any], Any],
    on_effect: Callable[[Any], Any],
    on_error: Callable[[Any], Any] | None = None,
    profiles: Iterable[SolverProfile] | None = None,
    timeout: float = 5.0,
    flags: Mapping[str, str | Term] | None = None,
    scheduling: Scheduling = "concurrent",
) -> GuiFacade:
    """Creates a GUI application, whose pages solve queries with the solvers of a profile.

    The application is not started: call its `start()` method, then `dispatch(action)` actions
    to it, and eventually `close()` it (or use it as a context manager).

    Args:
        on_state: Called with every new `GuiState` (intermediate states may be skipped, the
            latest one never is), on a JVM thread.
        on_effect: Called with every `GuiEffect`, in order, on a JVM thread.
        on_error: Called with the exceptions raised by actions or by the callbacks; by default,
            they are logged on the `tuprolog.gui` logger.
        profiles: The solver profiles (see `solver_profile`): new pages use the first one; by
            default, `solver_profile()`'s.
        timeout: The default timeout of resolutions, in seconds.
        flags: The flags of every solver (names to values, as terms or their Prolog text, e.g.
            `{"unknown": "fail"}`).
        scheduling: Whether resolutions of different pages may run concurrently
            (`"concurrent"`), or starting one stops the others (`"single"`).

    Returns:
        The application, a `GuiFacade`.

    Examples:
        >>> from tuprolog.gui import ConsumptionMode, PageAction, WorkspaceAction
        >>> with gui_application(on_state=lambda state: None, on_effect=print) as gui:
        ...     gui.start().get()
        ...     gui.dispatch(WorkspaceAction.NewScratchPage("demo", "p(1).")).get()
        ...     page = gui.state.workspace.pages[0]
        ...     gui.dispatch(PageAction.ChangeQuery(page.id, "p(X)")).get()
        ...     page = gui.state.workspace.page(page.id)
        >>> page.title, page.query.text
        ('demo', 'p(X)')

    Note:
        Wraps 2PPy's `GuiFacade.of`, on top of 2P-Kt's `buildGuiApplication`.
    """
    if scheduling not in _SCHEDULING:
        raise ValueError(f"Unknown scheduling: {scheduling}")
    report = _log_error if on_error is None else on_error

    def reporting(function: Callable[[Any], Any]) -> Callable[[Any], None]:
        # Python exceptions would reach the JVM as opaque proxies: report them here instead
        def call(value: Any) -> None:
            try:
                function(value)
            except Exception as error:  # noqa: BLE001  (reported, not swallowed)
                report(error)

        return call

    return GuiFacade.of(
        jlist([solver_profile()] if profiles is None else list(profiles)),
        _Consumer(reporting(on_state)),
        _Consumer(reporting(on_effect)),
        _Consumer(report),
        int(timeout * 1000),
        jmap({name: str(value) for name, value in (flags or {}).items()}),
        _SCHEDULING[scheduling],
    )


def prolog_gui(
    on_state: Callable[[Any], Any],
    on_effect: Callable[[Any], Any],
    on_error: Callable[[Any], Any] | None = None,
    timeout: float = 5.0,
) -> GuiFacade:
    """Creates a GUI application whose pages solve queries with Prolog solvers.

    A shorthand for `gui_application` with the default profile (see `solver_profile`).

    Args:
        on_state: Called with every new `GuiState`, on a JVM thread.
        on_effect: Called with every `GuiEffect`, in order, on a JVM thread.
        on_error: Called with the exceptions raised by actions or by the callbacks; by default,
            they are logged on the `tuprolog.gui` logger.
        timeout: The default timeout of resolutions, in seconds.

    Returns:
        The application, a `GuiFacade`.

    Examples:
        >>> with prolog_gui(on_state=lambda state: None, on_effect=print) as gui:
        ...     gui.start().get()
        >>> gui.is_closed
        True
    """
    return gui_application(on_state, on_effect, on_error, timeout=timeout)


def path_origin(path: str | PathLike[str]) -> DocumentOrigin:
    """The `DocumentOrigin` of a file, whose provider is `PATH_PROVIDER`.

    Args:
        path: The path of the file; it is made absolute.

    Returns:
        The origin, displayed as the file's name.

    Examples:
        >>> origin = path_origin("theory.pl")
        >>> origin.display_name, origin.provider_id
        ('theory.pl', 'path')
    """
    absolute = Path(path).absolute()
    return DocumentOrigin(PATH_PROVIDER, str(absolute), absolute.name or str(absolute))


def origin_path(origin: DocumentOrigin) -> Path | None:
    """The path of the file a `DocumentOrigin` refers to, if its provider is `PATH_PROVIDER`.

    Args:
        origin: The origin.

    Returns:
        The path, or `None` for origins of other providers.

    Examples:
        >>> origin_path(path_origin("theory.pl")).name
        'theory.pl'
    """
    if str(origin.provider_id) != PATH_PROVIDER:
        return None
    return Path(str(origin.opaque_reference))


def documentation_preview(markdown: str, max_length: int = 200) -> str:
    """A short preview of the Markdown documentation of a symbol (e.g. a flag, or a predicate of a
    library), as 2P-Kt's IDEs show it: the first paragraph after its signature.

    Args:
        markdown: The documentation (e.g. the `help` of a flag, or a value of the
            `documentation` of a library, in a solver's inspection).
        max_length: The maximum length of the preview.

    Returns:
        The preview.

    Examples:
        >>> documentation_preview("`p(?X)`\\n\\nTrue of every `X`.\\n\\n**Examples**\\n\\n...")
        'True of every X.'

    Note:
        Wraps 2P-Kt's `documentationPreview`.
    """
    return str(_presentation.MarkdownKt.documentationPreview(markdown, max_length))
