"""The toolkit-neutral core of tuProlog's graphical user interfaces (GUIs) and IDEs.

2P-Kt's GUI core models an IDE for logic programs without depending on any toolkit: user
interfaces only render its state, send it actions, and fulfil its effects. Its notions:

- the *state* (`GuiState`, immutable): the open *pages* (`PageState`, each with a theory to edit, a
  query, its current resolution, history, console and diagnostics) and *documents*
  (`DocumentState`, the files pages edit);
- *actions* (`GuiAction`): what users ask for, e.g. editing a theory (`PageAction.ChangeScratchText`)
  or solving a query (`PageAction.Solve`);
- *effects* (`GuiEffect`): what the application asks its user interface to do, as it cannot do it
  itself, e.g. asking where to save a file (`GuiEffect.PickSaveDestination`), or writing it
  (`GuiEffect.WriteDocument`); the user interface reports the outcome back as actions.

Solutions, warnings and diagnostics come formatted for display (`SolutionPresentation`, ...).
`gui_application` creates a `GuiFacade`, a running application whose pages solve with the
solvers of a profile (`solver_profile`: the language, libraries, initial dynamic knowledge base,
...), and `prolog_gui` one with Prolog solvers; `tuprolog.tui` is a terminal user interface built
on it.

Examples:
    >>> states = []
    >>> gui = prolog_gui(on_state=states.append, on_effect=print)
    >>> gui.start().get()
    >>> gui.dispatch(WorkspaceAction.NewScratchPage(None, "p(1).")).get()
    >>> page = gui.state.workspace.pages[0]
    >>> str(page.content.text)
    'p(1).'
    >>> gui.close()

See Also:
    `tuprolog.tui`, the terminal IDE.
"""

from ._api import *
from ._definitions import *

__all__ = [
    "PATH_PROVIDER",
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
    "documentation_preview",
    "gui_application",
    "origin_path",
    "path_origin",
    "prolog_gui",
    "solver_profile",
]
