"""The bridge between the terminal IDE and 2P-Kt's GUI application, running on the JVM."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any, Literal, Protocol

from tuprolog.core import Term
from tuprolog.gui import (
    ApplicationAction,
    CloseDecision,
    ConsumptionMode,
    DocumentAction,
    DocumentId,
    GuiEffect,
    GuiFacade,
    OperatorPresentation,
    PageAction,
    PageContent,
    PageId,
    PanelId,
    PrologSyntaxAnalyzer,
    ReloadDecision,
    SolutionPresentation,
    SolverProfile,
    WorkspaceAction,
    documentation_preview,
    gui_application,
    origin_path,
    path_origin,
)
from tuprolog.jvmutils import jlist

from . import _model as m

__all__ = ["GuiBridge", "JvmGuiBridge"]

Scheduling = Literal["concurrent", "single"]


class GuiBridge(Protocol):
    """What the terminal IDE needs from a GUI application.

    Callbacks may be called on any thread: the IDE forwards them to its own event loop.
    """

    def start(
        self,
        on_state: Callable[[m.Snapshot], object],
        on_effect: Callable[[m.Effect], object],
        on_error: Callable[[str], object],
    ) -> None:
        """Starts the application, which reports states, effects and errors to the callbacks."""

    def dispatch(self, action: m.Action) -> None:
        """Enqueues an action: actions are applied in order."""

    def close(self) -> None:
        """Shuts the application down; idempotent."""

    def is_timeout(self, text: str) -> bool:
        """Whether `text` is a timeout (e.g. `"2s 500ms"`, or `"none"`), for `tuprolog.tui.ChangeTimeout`."""

    def analyze(
        self, source: str, operators: tuple[tuple[int, str, str], ...] = ()
    ) -> tuple[m.SyntaxToken, ...]:
        """The tokens of Prolog text, given the `(priority, specifier, name)` of extra operators."""

    def documentation_preview(self, markdown: str) -> str:
        """A short preview of the Markdown documentation of a symbol."""


class JvmGuiBridge:
    """A `GuiBridge` running 2P-Kt's GUI application (a `tuprolog.gui.GuiFacade`), converting its JVM states and effects into `tuprolog.tui` snapshots and effects, and
    actions the other way round.

    Args:
        profiles: The solver profiles (see `tuprolog.gui.solver_profile`); by default, Prolog's.
        timeout: The default timeout of resolutions, in seconds.
        flags: The flags of every solver (names to values, as terms or their Prolog text).
        scheduling: Whether resolutions of different pages may run concurrently
            (`"concurrent"`), or starting one stops the others (`"single"`).
    """

    def __init__(
        self,
        profiles: Iterable[SolverProfile] | None = None,
        timeout: float = 5.0,
        flags: Mapping[str, str | Term] | None = None,
        scheduling: Scheduling = "concurrent",
    ) -> None:
        self.profiles = None if profiles is None else list(profiles)
        self.timeout = timeout
        self.flags = dict(flags or {})
        self.scheduling: Scheduling = scheduling
        self._facade: GuiFacade | None = None

    def start(
        self,
        on_state: Callable[[m.Snapshot], object],
        on_effect: Callable[[m.Effect], object],
        on_error: Callable[[str], object],
    ) -> None:
        if self._facade is not None:
            return
        self._facade = gui_application(
            on_state=lambda state: on_state(snapshot(state)),
            on_effect=lambda effect: on_effect(convert_effect(effect)),
            on_error=lambda error: on_error(str(error)),
            profiles=self.profiles,
            timeout=self.timeout,
            flags=self.flags,
            scheduling=self.scheduling,
        )
        self._facade.start()

    def dispatch(self, action: m.Action) -> None:
        if self._facade is None:
            raise RuntimeError("The GUI application is not started")
        if isinstance(action, m.ChangeFlag):
            # the facade completes the page's configuration, as it is when the action is applied
            self._facade.changeFlag(PageId(action.page_id), action.name, action.value)
        elif isinstance(action, m.ChangeTimeout):
            self._facade.changeTimeout(PageId(action.page_id), action.timeout)
        else:
            self._facade.dispatch(jvm_action(action))

    def close(self) -> None:
        if self._facade is not None:
            self._facade.close()

    def is_timeout(self, text: str) -> bool:
        return bool(GuiFacade.isTimeout(text))

    def analyze(
        self, source: str, operators: tuple[tuple[int, str, str], ...] = ()
    ) -> tuple[m.SyntaxToken, ...]:
        presented = jlist(OperatorPresentation(n, p, s) for p, s, n in operators)
        return tuple(
            m.SyntaxToken(
                str(token.category),
                (int(token.range.start.line), int(token.range.start.column)),
                (int(token.range.end_exclusive.line), int(token.range.end_exclusive.column)),
            )
            for token in PrologSyntaxAnalyzer.analyze(source, presented).tokens
        )

    def documentation_preview(self, markdown: str) -> str:
        return documentation_preview(markdown)


# --- JVM -> Python -------------------------------------------------------------------------------


def _solution(value: Any) -> m.Solution:
    query = str(value.query)
    if isinstance(value, SolutionPresentation.Yes):
        return m.Solution(
            "yes",
            query,
            bindings=tuple((str(b.variable), str(b.value)) for b in value.bindings),
            solved_query=None if value.solved_query is None else str(value.solved_query),
            metadata=tuple(sorted((str(k), str(v)) for k, v in value.metadata.items())),
        )
    if isinstance(value, SolutionPresentation.Halt):
        return m.Solution("halt", query, message=str(value.message), is_timeout=value.is_timeout)
    return m.Solution("no", query)


def _optional_str(value: Any) -> str | None:
    return None if value is None else str(value)


def _diagnostic(value: Any) -> m.DiagnosticEntry:
    if value.range is None:
        return m.DiagnosticEntry(f"{value.severity}: {value.message}")
    start = value.range.start
    return m.DiagnosticEntry(
        f"{value.severity} {start.line + 1}:{start.column + 1}: {value.message}",
        int(start.line),
        int(start.column),
    )


def _operator(value: Any) -> tuple[int, str, str]:
    return int(value.priority), str(value.specifier), str(value.name)


def _library(library: Any) -> m.LibraryEntry:
    documentation = {str(k): str(v) for k, v in library.documentation.items()}
    predicates = tuple(str(p) for p in library.predicates)
    functions = tuple(str(f) for f in library.functions)
    operators = {}  # as listed -> as documented (e.g. "op(700, XFX, =)" -> "=/2")
    for operator in library.operators:
        priority, specifier, name = _operator(operator)
        arity = 2 if len(specifier) == 3 else 1
        operators[f"op({priority}, {specifier}, {name})"] = f"{name}/{arity}"
    documented = {s: documentation[s] for s in predicates + functions if s in documentation}
    documented |= {o: documentation[s] for o, s in operators.items() if s in documentation}
    return m.LibraryEntry(
        str(library.alias),
        predicates=predicates,
        operators=tuple(operators),
        functions=functions,
        help=str(library.help),
        documentation=tuple(documented.items()),
    )


def _inspection(value: Any) -> m.Inspection:
    if value is None:
        return m.Inspection()
    return m.Inspection(
        operators=tuple(_operator(o) for o in value.operators),
        flags=tuple((str(f.name), str(f.value), str(f.help)) for f in value.flags),
        libraries=tuple(_library(library) for library in value.libraries),
        static_kb=str(value.static_knowledge_base),
        dynamic_kb=str(value.dynamic_knowledge_base),
    )


def _page(state: Any, page: Any) -> m.Page:
    content = page.content
    document_id: str | None = None
    dirty = False
    if isinstance(content, PageContent.Scratch):
        source = str(content.text)
    else:
        document = state.workspace.document(content.document_id)
        document_id = str(content.document_id)
        source = str(document.text)
        dirty = bool(document.is_dirty)
    resolution = page.resolution
    console = page.console
    unread = {
        "SOLUTIONS": resolution.has_unread_changes,
        "STDOUT": console.stdout.has_unread_changes,
        "STDERR": console.stderr.has_unread_changes,
        "WARNINGS": console.warnings.has_unread_changes,
        "DIAGNOSTICS": page.diagnostics.has_unread_changes,
    }
    return m.Page(
        id=str(page.id),
        title=str(page.title),
        source=source,
        document_id=document_id,
        dirty=dirty,
        query=str(page.query.text),
        resolution=m.Resolution(
            status=str(resolution.status),
            query=_optional_str(resolution.query),
            solutions=tuple(_solution(s) for s in resolution.solutions),
            error=_optional_str(resolution.error),
            can_solve=bool(resolution.can_solve),
            can_continue=bool(resolution.can_continue),
            can_stop=bool(resolution.can_stop),
        ),
        history=tuple(
            m.HistoryEntry(
                query=str(entry.query),
                solutions=tuple(_solution(s) for s in entry.solutions),
                status=str(entry.terminal_status),
                error=_optional_str(entry.error),
            )
            for entry in page.history.resolutions
        ),
        stdin=str(console.stdin),
        timeout=str(GuiFacade.timeoutOf(state, page)),
        stdout=str(console.stdout.text),
        stderr=str(console.stderr.text),
        warnings=tuple(str(w.message) for w in console.warnings.values),
        diagnostics=tuple(_diagnostic(d) for d in page.diagnostics.values),
        inspection=_inspection(page.solver_session.inspection),
        unread=frozenset(panel for panel, flag in unread.items() if flag),  # type: ignore[misc]
    )


def snapshot(state: Any) -> m.Snapshot:
    """Converts a `tuprolog.gui.GuiState` into a snapshot."""
    workspace = state.workspace
    return m.Snapshot(
        started=bool(state.application.started),
        pages=tuple(_page(state, page) for page in workspace.pages),
        selected_page_id=_optional_str(workspace.selected_page_id),
    )


def convert_effect(effect: Any) -> m.Effect:
    """Converts a `tuprolog.gui.GuiEffect` into an effect."""
    effect_id = str(effect.id)
    if isinstance(effect, GuiEffect.PickOpenDocument):
        return m.PickOpenDocument(effect_id)
    if isinstance(effect, GuiEffect.PickSaveDestination):
        return m.PickSaveDestination(effect_id, str(effect.document_id), str(effect.suggested_name))
    if isinstance(effect, GuiEffect.WriteDocument):
        return m.WriteDocument(
            effect_id,
            str(effect.document_id),
            origin_path(effect.origin),
            str(effect.text),
            int(effect.revision),
        )
    if isinstance(effect, GuiEffect.ReadDocument):
        return m.ReadDocument(effect_id, str(effect.document_id), origin_path(effect.origin))
    if isinstance(effect, GuiEffect.ConfirmCloseDirtyPage):
        return m.ConfirmCloseDirtyPage(
            effect_id, str(effect.page_id), str(effect.document_id), str(effect.display_name)
        )
    if isinstance(effect, GuiEffect.ConfirmReloadDirtyDocument):
        return m.ConfirmReloadDirtyDocument(
            effect_id, str(effect.document_id), str(effect.display_name)
        )
    if isinstance(effect, GuiEffect.ConfirmExitWithDirtyDocuments):
        return m.ConfirmExitWithDirtyDocuments(
            effect_id, tuple(str(d) for d in effect.dirty_documents)
        )
    if isinstance(effect, GuiEffect.CopyTextToClipboard):
        return m.CopyToClipboard(effect_id, str(effect.text))
    if isinstance(effect, GuiEffect.ExitApplication):
        return m.ExitApplication(effect_id)
    raise ValueError(f"Unsupported effect: {effect}")


# --- Python -> JVM -------------------------------------------------------------------------------


def jvm_action(action: m.Action) -> Any:
    """Converts an action into a `tuprolog.gui.GuiAction`."""
    match action:
        case m.RequestExit():
            return ApplicationAction.RequestExit.INSTANCE
        case m.ExitConfirmed():
            return ApplicationAction.ExitConfirmed.INSTANCE
        case m.ExitCancelled():
            return ApplicationAction.ExitCancelled.INSTANCE
        case m.NewScratchPage(title, text):
            return WorkspaceAction.NewScratchPage(title, text)
        case m.NewDocumentPage(name, text):
            return WorkspaceAction.NewDocumentPage(name, text)
        case m.SelectPage(page_id):
            return WorkspaceAction.SelectPage(PageId(page_id))
        case m.RequestOpenDocument():
            return WorkspaceAction.RequestOpenDocument.INSTANCE
        case m.OpenDocumentLoaded(path, text):
            return WorkspaceAction.OpenDocumentLoaded(path_origin(path), text, False)
        case m.RequestClosePage(page_id):
            return WorkspaceAction.RequestClosePage(PageId(page_id))
        case m.ClosePageDecision(page_id, decision):
            return WorkspaceAction.ClosePageDecisionProvided(
                PageId(page_id), CloseDecision.valueOf(decision)
            )
        case m.ChangeScratchText(page_id, text):
            return PageAction.ChangeScratchText(PageId(page_id), text)
        case m.ChangeDocumentText(document_id, text):
            return DocumentAction.ChangeText(DocumentId(document_id), text)
        case m.ChangeQuery(page_id, query):
            return PageAction.ChangeQuery(PageId(page_id), query)
        case m.ChangeStdin(page_id, stdin):
            return PageAction.ChangeStdin(PageId(page_id), stdin)
        case m.Solve(page_id, mode):
            return PageAction.Solve(PageId(page_id), ConsumptionMode.valueOf(mode))
        case m.Next(page_id, mode):
            return PageAction.Next(PageId(page_id), ConsumptionMode.valueOf(mode))
        case m.Stop(page_id):
            return PageAction.Stop(PageId(page_id))
        case m.Reset(page_id):
            return PageAction.Reset(PageId(page_id))
        case m.ClearHistory(page_id):
            return PageAction.ClearHistory(PageId(page_id))
        case m.MarkPanelRead(page_id, panel):
            return PageAction.MarkPanelRead(PageId(page_id), PanelId.valueOf(panel))
        case m.RequestSave(document_id, save_as):
            return DocumentAction.RequestSave(DocumentId(document_id), save_as)
        case m.SaveDestinationSelected(document_id, path):
            return DocumentAction.SaveDestinationSelected(
                DocumentId(document_id), path_origin(path)
            )
        case m.SaveCancelled(document_id):
            return DocumentAction.SaveCancelled(DocumentId(document_id))
        case m.SaveSucceeded(document_id, path, revision):
            return DocumentAction.SaveSucceeded(
                DocumentId(document_id), path_origin(path), revision
            )
        case m.SaveFailed(document_id, message):
            return DocumentAction.SaveFailed(DocumentId(document_id), message)
        case m.RequestReload(document_id):
            return DocumentAction.RequestReload(DocumentId(document_id))
        case m.ReloadDecision(document_id, decision):
            return DocumentAction.ReloadDecisionProvided(
                DocumentId(document_id), ReloadDecision.valueOf(decision)
            )
        case m.ReloadSucceeded(document_id, text):
            return DocumentAction.ReloadSucceeded(DocumentId(document_id), text)
        case m.ReloadFailed(document_id, message):
            return DocumentAction.ReloadFailed(DocumentId(document_id), message)
    raise ValueError(f"Unsupported action: {action}")
