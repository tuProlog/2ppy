"""What the terminal IDE renders and dispatches: plain Python snapshots of 2P-Kt's GUI state, and
the actions and effects it exchanges with it.

They mirror the parts of `tuprolog.gui`'s JVM types the IDE uses, so that its widgets never touch
JVM objects (which live on other threads), and its tests can run without a GUI application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

__all__ = [
    "PANELS",
    "Action",
    "ChangeDocumentText",
    "ChangeFlag",
    "ChangeQuery",
    "ChangeScratchText",
    "ChangeStdin",
    "ChangeTimeout",
    "ClearHistory",
    "ClosePageDecision",
    "ConfirmCloseDirtyPage",
    "ConfirmExitWithDirtyDocuments",
    "ConfirmReloadDirtyDocument",
    "CopyToClipboard",
    "DiagnosticEntry",
    "Effect",
    "ExitApplication",
    "ExitCancelled",
    "ExitConfirmed",
    "HistoryEntry",
    "Inspection",
    "LibraryEntry",
    "MarkPanelRead",
    "NewDocumentPage",
    "NewScratchPage",
    "Next",
    "OpenDocumentLoaded",
    "Page",
    "PickOpenDocument",
    "PickSaveDestination",
    "ReadDocument",
    "ReloadDecision",
    "ReloadFailed",
    "ReloadSucceeded",
    "RequestClosePage",
    "RequestExit",
    "RequestOpenDocument",
    "RequestReload",
    "RequestSave",
    "Reset",
    "Resolution",
    "SaveCancelled",
    "SaveDestinationSelected",
    "SaveFailed",
    "SaveSucceeded",
    "SelectPage",
    "Snapshot",
    "Solution",
    "Solve",
    "Startup",
    "Stop",
    "SyntaxToken",
    "WriteDocument",
]

Mode = Literal["ONE", "TEN", "HUNDRED", "ALL"]
"""How many solutions a solve or next asks for (the names of `tuprolog.gui.ConsumptionMode`)."""

Panel = Literal[
    "SOLUTIONS",
    "STDIN",
    "STDOUT",
    "STDERR",
    "WARNINGS",
    "DIAGNOSTICS",
    "OPERATORS",
    "FLAGS",
    "LIBRARIES",
    "STATIC_KB",
    "DYNAMIC_KB",
]
"""A lower panel of a page (the names of `tuprolog.gui.PanelId`)."""

PANELS: tuple[Panel, ...] = (
    "SOLUTIONS",
    "STDIN",
    "STDOUT",
    "STDERR",
    "WARNINGS",
    "DIAGNOSTICS",
    "OPERATORS",
    "FLAGS",
    "LIBRARIES",
    "STATIC_KB",
    "DYNAMIC_KB",
)
"""The panels the IDE shows, in order (as 2P-Kt's Swing IDE)."""


# --- state ---------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Solution:
    """A solution, as formatted by 2P-Kt: `kind` is `"yes"`, `"no"` or `"halt"`; `metadata` holds
    extra values of successful solutions (e.g. their `probability`, for ProbLog)."""

    kind: Literal["yes", "no", "halt"]
    query: str
    bindings: tuple[tuple[str, str], ...] = ()
    solved_query: str | None = None
    metadata: tuple[tuple[str, str], ...] = ()
    message: str | None = None
    is_timeout: bool = False


@dataclass(frozen=True)
class Resolution:
    """The current resolution of a page, and the commands it allows."""

    status: str = "IDLE"
    query: str | None = None
    solutions: tuple[Solution, ...] = ()
    error: str | None = None
    can_solve: bool = True
    can_continue: bool = False
    can_stop: bool = False


@dataclass(frozen=True)
class HistoryEntry:
    """A concluded resolution."""

    query: str
    solutions: tuple[Solution, ...]
    status: str
    error: str | None = None


@dataclass(frozen=True)
class SyntaxToken:
    """A classified span of Prolog text, for syntax highlighting: `category` is the name of a
    `tuprolog.gui.SemanticCategory`, `start` and `end` (exclusive) are 0-based `(line, column)`."""

    category: str
    start: tuple[int, int]
    end: tuple[int, int]


@dataclass(frozen=True)
class DiagnosticEntry:
    """A problem found in the theory, at a 0-based `line` and `column` if known."""

    message: str
    line: int | None = None
    column: int | None = None


@dataclass(frozen=True)
class LibraryEntry:
    """A library of a solver: its alias, the predicates, operators and functions it defines, its
    `help`, and the `documentation` of its symbols (as pairs of a symbol, as listed, and its help).
    Helps are in Markdown."""

    alias: str
    predicates: tuple[str, ...] = ()
    operators: tuple[str, ...] = ()
    functions: tuple[str, ...] = ()
    help: str = ""
    documentation: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Inspection:
    """What the solver of a page holds: its operators (as `(priority, specifier, name)`), flags
    (as `(name, value, help)`, with help in Markdown), libraries, and static and dynamic knowledge bases (as Prolog text)."""

    operators: tuple[tuple[int, str, str], ...] = ()
    flags: tuple[tuple[str, str, str], ...] = ()
    libraries: tuple[LibraryEntry, ...] = ()
    static_kb: str = ""
    dynamic_kb: str = ""


@dataclass(frozen=True)
class Page:
    """A page: its source (from its scratch text or its document), query, resolution and panels."""

    id: str
    title: str
    source: str = ""
    document_id: str | None = None
    dirty: bool = False
    query: str = ""
    resolution: Resolution = field(default_factory=Resolution)
    history: tuple[HistoryEntry, ...] = ()
    stdin: str = ""
    timeout: str = "5s"
    stdout: str = ""
    stderr: str = ""
    warnings: tuple[str, ...] = ()
    diagnostics: tuple[DiagnosticEntry, ...] = ()
    inspection: Inspection = field(default_factory=Inspection)
    unread: frozenset[Panel] = frozenset()


@dataclass(frozen=True)
class Snapshot:
    """The state of the GUI application, as far as the IDE renders it."""

    started: bool = False
    pages: tuple[Page, ...] = ()
    selected_page_id: str | None = None

    def page(self, page_id: str | None) -> Page | None:
        """The page with the given id, if any."""
        return next((p for p in self.pages if p.id == page_id), None)

    @property
    def selected_page(self) -> Page | None:
        """The selected page, if any."""
        return self.page(self.selected_page_id)


@dataclass(frozen=True)
class Startup:
    """What the IDE opens at startup (e.g. as asked on the command line).

    It opens a page per document (a path, and its text: empty if the file does not exist yet),
    then a scratch page with `theory` if given, or if no documents are; it gives each of these
    pages `query` and `stdin`, if given, and finally solves the query of the selected page (the
    last one) with `solve`, if given.
    """

    documents: tuple[tuple[Path, str], ...] = ()
    theory: str | None = None
    query: str | None = None
    stdin: str | None = None
    solve: Mode | None = None

    @property
    def page_count(self) -> int:
        """How many pages the startup opens."""
        return len(self.documents) + (1 if self.theory is not None or not self.documents else 0)


# --- actions -------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Action:
    """Something the IDE asks the GUI application to do."""


@dataclass(frozen=True)
class RequestExit(Action):
    """The user asked to quit."""


@dataclass(frozen=True)
class ExitConfirmed(Action):
    """The user confirmed quitting despite unsaved changes."""


@dataclass(frozen=True)
class ExitCancelled(Action):
    """The user backed out of quitting."""


@dataclass(frozen=True)
class NewScratchPage(Action):
    """Creates a page with its own text."""

    title: str | None = None
    text: str = ""


@dataclass(frozen=True)
class NewDocumentPage(Action):
    """Creates a page editing a new, unsaved document."""

    name: str | None = None
    text: str = ""


@dataclass(frozen=True)
class SelectPage(Action):
    """Selects a page."""

    page_id: str


@dataclass(frozen=True)
class RequestOpenDocument(Action):
    """The user asked to open a file."""


@dataclass(frozen=True)
class OpenDocumentLoaded(Action):
    """A file was read, and becomes a new page."""

    path: Path
    text: str


@dataclass(frozen=True)
class RequestClosePage(Action):
    """The user asked to close a page."""

    page_id: str


@dataclass(frozen=True)
class ClosePageDecision(Action):
    """The user decided how to close a page with unsaved changes."""

    page_id: str
    decision: Literal["SAVE", "DISCARD", "CANCEL"]


@dataclass(frozen=True)
class ChangeScratchText(Action):
    """The text of a scratch page was edited."""

    page_id: str
    text: str


@dataclass(frozen=True)
class ChangeDocumentText(Action):
    """The text of a document was edited."""

    document_id: str
    text: str


@dataclass(frozen=True)
class ChangeQuery(Action):
    """The query of a page was edited."""

    page_id: str
    query: str


@dataclass(frozen=True)
class ChangeStdin(Action):
    """The standard input of a page was edited."""

    page_id: str
    stdin: str


@dataclass(frozen=True)
class ChangeTimeout(Action):
    """The timeout of the resolutions of a page was edited (e.g. `"2s 500ms"`, or `"none"`)."""

    page_id: str
    timeout: str


@dataclass(frozen=True)
class Solve(Action):
    """Solves the query of a page."""

    page_id: str
    mode: Mode = "ONE"


@dataclass(frozen=True)
class Next(Action):
    """Asks for more solutions of the current resolution of a page."""

    page_id: str
    mode: Mode = "ONE"


@dataclass(frozen=True)
class Stop(Action):
    """Stops the current resolution of a page."""

    page_id: str


@dataclass(frozen=True)
class Reset(Action):
    """Resets the solver of a page."""

    page_id: str


@dataclass(frozen=True)
class ClearHistory(Action):
    """Forgets the concluded resolutions of a page."""

    page_id: str


@dataclass(frozen=True)
class ChangeFlag(Action):
    """Sets a flag of the solvers of a page to a value (a Prolog term)."""

    page_id: str
    name: str
    value: str


@dataclass(frozen=True)
class MarkPanelRead(Action):
    """The user looked at a panel of a page."""

    page_id: str
    panel: Panel


@dataclass(frozen=True)
class RequestSave(Action):
    """The user asked to save a document (choosing where, if `save_as`)."""

    document_id: str
    save_as: bool = False


@dataclass(frozen=True)
class SaveDestinationSelected(Action):
    """The user chose where to save a document."""

    document_id: str
    path: Path


@dataclass(frozen=True)
class SaveCancelled(Action):
    """The user backed out of choosing where to save a document."""

    document_id: str


@dataclass(frozen=True)
class SaveSucceeded(Action):
    """A document was written."""

    document_id: str
    path: Path
    revision: int


@dataclass(frozen=True)
class SaveFailed(Action):
    """Writing a document failed."""

    document_id: str
    message: str


@dataclass(frozen=True)
class RequestReload(Action):
    """The user asked to reload a document from its file."""

    document_id: str


@dataclass(frozen=True)
class ReloadDecision(Action):
    """The user decided whether to reload a document with unsaved changes."""

    document_id: str
    decision: Literal["DISCARD_CHANGES", "CANCEL"]


@dataclass(frozen=True)
class ReloadSucceeded(Action):
    """A document was read again."""

    document_id: str
    text: str


@dataclass(frozen=True)
class ReloadFailed(Action):
    """Reading a document again failed."""

    document_id: str
    message: str


# --- effects -------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Effect:
    """Something the GUI application asks the IDE to do."""

    id: str


@dataclass(frozen=True)
class PickOpenDocument(Effect):
    """Ask for a file to open."""


@dataclass(frozen=True)
class PickSaveDestination(Effect):
    """Ask where to save a document."""

    document_id: str
    suggested_name: str


@dataclass(frozen=True)
class WriteDocument(Effect):
    """Write a document (`path` is `None` if its origin is not a file)."""

    document_id: str
    path: Path | None
    text: str
    revision: int


@dataclass(frozen=True)
class ReadDocument(Effect):
    """Read a document again (`path` is `None` if its origin is not a file)."""

    document_id: str
    path: Path | None


@dataclass(frozen=True)
class ConfirmCloseDirtyPage(Effect):
    """Ask how to close a page with unsaved changes."""

    page_id: str
    document_id: str
    display_name: str


@dataclass(frozen=True)
class ConfirmReloadDirtyDocument(Effect):
    """Ask whether to reload a document with unsaved changes."""

    document_id: str
    display_name: str


@dataclass(frozen=True)
class ConfirmExitWithDirtyDocuments(Effect):
    """Ask whether to quit despite unsaved changes."""

    document_ids: tuple[str, ...]


@dataclass(frozen=True)
class CopyToClipboard(Effect):
    """Copy a text to the clipboard."""

    text: str


@dataclass(frozen=True)
class ExitApplication(Effect):
    """Quit."""
