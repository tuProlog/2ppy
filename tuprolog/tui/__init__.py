"""2ppy TUI: a terminal IDE for Prolog, built with [Textual](https://textual.textualize.io/).

Run it with `2ppy-tui` or `python -m tuprolog.tui` (`--help` lists the options: files to open,
theory, query, standard input, and how solvers are built: dialect, libraries, dynamic knowledge
base, unificator, flags, timeout; see `parser`). As 2P-Kt's Swing IDE, it shows pages (as tabs),
each with a theory to edit, a query to solve against it (both colored by syntax), the timeout of
its resolutions, and panels (as tabs, at the bottom) for
the solutions, the standard input, output and error of the solver, its warnings, the problems
found in the theory, and what the solver holds: operators (more can be added), flags (editable),
libraries, static and dynamic knowledge bases (flags and libraries with their documentation, `F1`). Arrow keys move among controls, unless the focused one uses them
(e.g. editors). Pages either have their own text (*scratch* pages, `ctrl+t`) or edit files
(`ctrl+n` creates one, `ctrl+o` opens one, `ctrl+s` saves it). `F5`, `F6` and `F7` ask for 1, 10
and 100 solutions (the `Solve all` button, for all of them) (then for the next ones), `F8` stops a resolution, `F9` resets the solver, and
`ctrl+q` quits (asking to confirm if files have unsaved changes).

The IDE holds no logic of its own: it renders the state of 2P-Kt's GUI application (see
`tuprolog.gui`), sends it the actions of the user, and fulfils its effects (e.g. asking for a path,
then writing the file). It talks to it through a `GuiBridge`: `JvmGuiBridge` runs 2P-Kt's,
converting its JVM states into snapshots (`Snapshot`, `Page`, ...), and the IDE's actions (e.g.
`Solve`) into JVM ones. `ReloadDecision`, `Solution` and `Solve` are importable by name, but
left out of `__all__`, as other tuprolog modules export the same names.

Examples:
    ```text
    $ 2ppy-tui
    ```

See Also:
    - `tuprolog.gui`, the GUI application the IDE renders.
    - `tuprolog.repl`, for a command-line shell.
"""

from ._app import PrologTui
from ._bridge import GuiBridge, JvmGuiBridge
from ._cli import main, parse_command_line, parser
from ._model import *
from ._model import (  # out of __all__: other modules export these names
    ReloadDecision,
    Solution,
    Solve,
)

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
    "GuiBridge",
    "HistoryEntry",
    "Inspection",
    "JvmGuiBridge",
    "LibraryEntry",
    "MarkPanelRead",
    "NewDocumentPage",
    "NewScratchPage",
    "Next",
    "OpenDocumentLoaded",
    "Page",
    "PickOpenDocument",
    "PickSaveDestination",
    "PrologTui",
    "ReadDocument",
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
    "Startup",
    "Stop",
    "SyntaxToken",
    "WriteDocument",
    "main",
    "parse_command_line",
    "parser",
]
