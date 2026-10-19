"""The JVM types of 2P-Kt's toolkit-neutral GUI core, re-exported by `tuprolog.gui`."""

import it.unibo.tuprolog.ppy.gui as _ppy_gui  # type: ignore
import it.unibo.tuprolog.ui.gui.controller as _controller  # type: ignore
import it.unibo.tuprolog.ui.gui.identity as _identity  # type: ignore
import it.unibo.tuprolog.ui.gui.model as _model  # type: ignore
import it.unibo.tuprolog.ui.gui.presentation as _presentation  # type: ignore
import it.unibo.tuprolog.ui.gui.solver as _solver  # type: ignore
import jpype.imports  # noqa: F401

import tuprolog.jvmutils  # noqa: F401  (snake_case accessors of JVM objects)

__all__ = [
    "PROLOG_PROFILE_ID",
    "ApplicationAction",
    "BindingPresentation",
    "CloseDecision",
    "ConsumptionMode",
    "Diagnostic",
    "DiagnosticSeverity",
    "DocumentAction",
    "DocumentId",
    "DocumentOrigin",
    "DocumentState",
    "EffectId",
    "GuiAction",
    "GuiEffect",
    "GuiFacade",
    "GuiState",
    "OperatorPresentation",
    "PageAction",
    "PageContent",
    "PageId",
    "PageState",
    "PanelId",
    "PrologSyntaxAnalyzer",
    "ReloadDecision",
    "ResolutionHistoryEntry",
    "ResolutionState",
    "ResolutionStatus",
    "SemanticCategory",
    "SemanticToken",
    "SolutionPresentation",
    "SolverProfile",
    "WarningPresentation",
    "WorkspaceAction",
    "WorkspaceState",
]


GuiFacade = _ppy_gui.GuiFacade
"""A running GUI application, driven by actions and observed through callbacks.

It runs 2P-Kt's GUI controller on JVM threads, hiding its coroutines: `start()` starts it,
`dispatch(action)` enqueues a `GuiAction` (actions are applied one at a time, in order), and
`close()` shuts it down (it is idempotent, and the facade is a context manager). `start()` and
`dispatch(action)` return a `java.util.concurrent.CompletableFuture`, completing once the action
is applied (e.g. `facade.dispatch(action).get()` waits for it). The `state` property is the current
`GuiState`. The state and effect callbacks run on JVM threads: user interfaces must forward them to
their own thread. Create one with `tuprolog.gui.prolog_gui`.

Note:
    The JVM class `it.unibo.tuprolog.ppy.gui.GuiFacade` of 2PPy (see `jvm/` in its repository),
    wrapping 2P-Kt's `GuiApplication`.
"""


PROLOG_PROFILE_ID = str(GuiFacade.PROLOG_PROFILE_ID)
"""The id of the solver profile of Prolog pages, i.e. `"prolog"`."""


SolverProfile = _solver.SolverProfile
"""A kind of solver pages can query (e.g. Prolog), with its id, display name and capabilities."""


GuiState = _model.GuiState
"""The whole state of a GUI application, at one point in time (immutable).

Members: `application` (whether it `started`, or an exit was requested) and `workspace` (a
`WorkspaceState`).
"""


WorkspaceState = _model.WorkspaceState
"""The open documents and pages of a GUI application (immutable).

Members: `pages` (the `PageState`s, in tab order), `documents` (a map from `DocumentId`s to
`DocumentState`s), `selected_page_id`, and the lookups `page(page_id)` and `document(document_id)`
(`None` if missing).
"""


PageState = _model.PageState
"""One page of a GUI application: a theory to edit, and queries to solve against it (immutable).

Members: `id` (a `PageId`), `title`, `content` (a `PageContent`), `query` (its `text`), `resolution`
(a `ResolutionState`), `history` (its `resolutions`, `ResolutionHistoryEntry`s), `console` (`stdin`,
`stdout.text`, `stderr.text`, `warnings.values`), `diagnostics` (its `values`, `Diagnostic`s) and
`semantic_tokens` (from parsing the theory).
"""


PageContent = _model.PageContent
"""What a page edits: `PageContent.Scratch` (the page's own `text`) or
`PageContent.DocumentReference` (the `document_id` of a document, possibly shared by pages)."""


DocumentState = _model.DocumentState
"""An open document (immutable): its `id`, `display_name`, `text`, `origin` (a `DocumentOrigin`,
`None` if never saved), `revision`, and whether it `is_dirty` (it has unsaved changes)."""


DocumentOrigin = _model.DocumentOrigin
"""Where a document is read from and saved to: a `provider_id` (e.g. `"path"`, for files), an
`opaque_reference` (e.g. the file's path) and a `display_name`."""


ResolutionState = _model.ResolutionState
"""The current resolution of a page (immutable).

Members: `status` (a `ResolutionStatus`), `query`, `solutions` (`SolutionPresentation`s so far),
`error`, and the commands it allows: `can_solve`, `can_continue` (more solutions may be asked for)
and `can_stop`.
"""


ResolutionStatus = _model.ResolutionStatus
"""The status of a resolution: `IDLE`, `RUNNING`, `AWAITING_CONTINUATION`, `COMPLETED`,
`FAILED`, or `CANCELLED`."""


ResolutionHistoryEntry = _model.ResolutionHistoryEntry
"""A concluded resolution: its `query`, `solutions`, `terminal_status` and `error`."""


PanelId = _model.PanelId
"""A panel of a page, which may have unread changes: `SOLUTIONS`, `STDIN`, `STDOUT`, `STDERR`,
`WARNINGS`, `DIAGNOSTICS`, ..."""


SolutionPresentation = _presentation.SolutionPresentation
"""A solution of a query, formatted for display: `SolutionPresentation.Yes` (with `bindings`,
`BindingPresentation`s, and `solved_query`), `SolutionPresentation.No`, or
`SolutionPresentation.Halt` (with a `message`, and `is_timeout`)."""


BindingPresentation = _presentation.BindingPresentation
"""The value of a variable in a solution, formatted for display: `variable` and `value`."""


WarningPresentation = _presentation.WarningPresentation
"""A warning of a solver, formatted for display: `message` and `logic_stack_trace`."""


OperatorPresentation = _presentation.OperatorPresentation
"""An operator, formatted for display: `name`, `priority` and `specifier` (e.g. `"XFX"`); built as
`OperatorPresentation(name, priority, specifier)`."""


SemanticCategory = _presentation.SemanticCategory
"""The syntactic role of a token of Prolog text, for syntax highlighting: `COMMENT`, `OPERATOR`,
`PARENTHESIS`, `BRACE`, `BRACKET`, `FUNCTOR`, `ATOM`, `VARIABLE`, `NUMBER`, `STRING`, `FULL_STOP`,
`DIRECTIVE`, or `ERROR`."""


SemanticToken = _presentation.SemanticToken
"""A classified span of Prolog text: `range` (its `start` and `end_exclusive` positions, each with
an `offset` and zero-based `line` and `column`), `category` (a `SemanticCategory`), and
`modifiers`."""


PrologSyntaxAnalyzer = _presentation.PrologSyntaxAnalyzer.INSTANCE
"""Classifies the tokens of Prolog text, for syntax highlighting:
`PrologSyntaxAnalyzer.analyze(source, operators)` (with a JVM list of `OperatorPresentation`s on
top of the standard ones, e.g. built by `tuprolog.jvmutils.jlist`) returns its `tokens`
(`SemanticToken`s) and `diagnostics` (syntax errors).

Examples:
    >>> from tuprolog.jvmutils import jlist
    >>> analysis = PrologSyntaxAnalyzer.analyze("p(X).", jlist([]))
    >>> [str(token.category) for token in analysis.tokens]
    ['FUNCTOR', 'PARENTHESIS', 'VARIABLE', 'PARENTHESIS', 'FULL_STOP']
"""


Diagnostic = _presentation.Diagnostic
"""A problem in a page's theory or query (e.g. a syntax error): `severity` (a
`DiagnosticSeverity`), `message`, and `range` (its `start` and `end_exclusive` positions, each with
zero-based `line` and `column`; `None` if unknown)."""


DiagnosticSeverity = _presentation.DiagnosticSeverity
"""The severity of a `Diagnostic`: `INFO`, `WARNING`, or `ERROR`."""


PageId = _identity.PageId
"""The identifier of a page, e.g. `PageId("page-1")`; `str()` gives its value."""


DocumentId = _identity.DocumentId
"""The identifier of a document, e.g. `DocumentId("document-1")`; `str()` gives its value."""


EffectId = _identity.EffectId
"""The identifier of a `GuiEffect`."""


GuiAction = _controller.GuiAction
"""Something a user interface asks a GUI application to do: an `ApplicationAction`, a
`WorkspaceAction`, a `PageAction` or a `DocumentAction`, dispatched by `GuiFacade.dispatch`."""


ApplicationAction = _controller.ApplicationAction
"""Actions about the whole application: `Start`, `RequestExit`, `ExitConfirmed`, and
`ExitCancelled` (singletons, e.g. `ApplicationAction.RequestExit.INSTANCE`)."""


WorkspaceAction = _controller.WorkspaceAction
"""Actions about pages: e.g. `NewScratchPage(title, text)`, `NewDocumentPage(name, text)`,
`SelectPage(page_id)`, `RequestOpenDocument.INSTANCE`, `OpenDocumentLoaded(origin, text, pending)`,
`RequestClosePage(page_id)`, and `ClosePageDecisionProvided(page_id, decision)`."""


PageAction = _controller.PageAction
"""Actions about one page: e.g. `ChangeScratchText(page_id, text)`, `ChangeQuery(page_id, query)`,
`ChangeStdin(page_id, stdin)`, `Solve(page_id, mode)`, `Next(page_id, mode)`, `Stop(page_id)`,
`Reset(page_id)`, and `MarkPanelRead(page_id, panel)`."""


DocumentAction = _controller.DocumentAction
"""Actions about one document: e.g. `ChangeText(document_id, text)`,
`RequestSave(document_id, force_save_as)`, `SaveDestinationSelected(document_id, origin)`,
`SaveSucceeded(document_id, origin, revision)`, `SaveFailed(document_id, message)`,
`RequestReload(document_id)`, `ReloadSucceeded(document_id, text)`, and so on."""


GuiEffect = _controller.GuiEffect
"""Something a GUI application asks its user interface to do, as it cannot do it itself.

E.g. `PickOpenDocument`, `PickSaveDestination`, `WriteDocument`, `ReadDocument`,
`ConfirmCloseDirtyPage`, `ConfirmReloadDirtyDocument`, `ConfirmExitWithDirtyDocuments`,
`CopyTextToClipboard`, and `ExitApplication`: the user interface reports the outcome back with
the matching actions (e.g. `DocumentAction.SaveSucceeded`).
"""


ConsumptionMode = _controller.ConsumptionMode
"""How many solutions `PageAction.Solve` and `PageAction.Next` ask for: `ONE`, `TEN`,
`HUNDRED`, or `ALL`."""


CloseDecision = _controller.CloseDecision
"""How to close a page with unsaved changes: `SAVE`, `DISCARD`, or `CANCEL`."""


ReloadDecision = _controller.ReloadDecision
"""Whether to reload a document with unsaved changes: `DISCARD_CHANGES` or `CANCEL`."""
