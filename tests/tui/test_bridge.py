"""Tests for `tuprolog.tui`'s bridge to 2P-Kt's GUI application, its entry points, and the IDE
running end to end on the JVM."""

import queue
import runpy
from importlib.metadata import entry_points
from pathlib import Path
from types import SimpleNamespace

import pytest
from textual.widgets import Input, TextArea

from tuprolog import tui
from tuprolog.gui import (
    ApplicationAction,
    DocumentAction,
    DocumentId,
    DocumentOrigin,
    EffectId,
    GuiEffect,
    PageAction,
    PageId,
    WorkspaceAction,
    path_origin,
)
from tuprolog.jvmutils import jlist
from tuprolog.tui import _bridge as bridge_module
from tuprolog.tui import _model as m

TIMEOUT = 30  # seconds


def jset(items):
    import java.util  # type: ignore

    return java.util.LinkedHashSet(jlist(items))


FILE = Path("theory.pl").absolute()

ACTIONS = [
    (m.RequestExit(), ApplicationAction.RequestExit),
    (m.ExitConfirmed(), ApplicationAction.ExitConfirmed),
    (m.ExitCancelled(), ApplicationAction.ExitCancelled),
    (m.NewScratchPage("t", "x."), WorkspaceAction.NewScratchPage),
    (m.NewDocumentPage("n.pl", "x."), WorkspaceAction.NewDocumentPage),
    (m.SelectPage("page-1"), WorkspaceAction.SelectPage),
    (m.RequestOpenDocument(), WorkspaceAction.RequestOpenDocument),
    (m.OpenDocumentLoaded(FILE, "x."), WorkspaceAction.OpenDocumentLoaded),
    (m.RequestClosePage("page-1"), WorkspaceAction.RequestClosePage),
    (m.ClosePageDecision("page-1", "SAVE"), WorkspaceAction.ClosePageDecisionProvided),
    (m.ChangeScratchText("page-1", "x."), PageAction.ChangeScratchText),
    (m.ChangeDocumentText("document-1", "x."), DocumentAction.ChangeText),
    (m.ChangeQuery("page-1", "q"), PageAction.ChangeQuery),
    (m.ChangeStdin("page-1", "in"), PageAction.ChangeStdin),
    (m.Solve("page-1", "TEN"), PageAction.Solve),
    (m.Next("page-1", "HUNDRED"), PageAction.Next),
    (m.Stop("page-1"), PageAction.Stop),
    (m.Reset("page-1"), PageAction.Reset),
    (m.ClearHistory("page-1"), PageAction.ClearHistory),
    (m.MarkPanelRead("page-1", "STDOUT"), PageAction.MarkPanelRead),
    (m.RequestSave("document-1", True), DocumentAction.RequestSave),
    (m.SaveDestinationSelected("document-1", FILE), DocumentAction.SaveDestinationSelected),
    (m.SaveCancelled("document-1"), DocumentAction.SaveCancelled),
    (m.SaveSucceeded("document-1", FILE, 2), DocumentAction.SaveSucceeded),
    (m.SaveFailed("document-1", "no"), DocumentAction.SaveFailed),
    (m.RequestReload("document-1"), DocumentAction.RequestReload),
    (m.ReloadDecision("document-1", "CANCEL"), DocumentAction.ReloadDecisionProvided),
    (m.ReloadSucceeded("document-1", "x."), DocumentAction.ReloadSucceeded),
    (m.ReloadFailed("document-1", "no"), DocumentAction.ReloadFailed),
]


@pytest.mark.parametrize("action, jvm_type", ACTIONS, ids=lambda x: type(x).__name__)
def test_actions_convert(action, jvm_type):
    assert isinstance(bridge_module.jvm_action(action), jvm_type)


def test_action_fields_convert():
    solve = bridge_module.jvm_action(m.Solve("page-1", "TEN"))
    assert str(solve.page_id) == "page-1" and str(solve.mode) == "TEN"
    saved = bridge_module.jvm_action(m.SaveSucceeded("document-1", FILE, 2))
    assert saved.origin == path_origin(FILE) and saved.saved_revision == 2


def test_unknown_actions_are_rejected():
    with pytest.raises(ValueError):
        bridge_module.jvm_action(m.Action())


E, D, P = EffectId("e"), DocumentId("document-1"), PageId("page-1")
ORIGIN = path_origin(FILE)
EFFECTS = [
    (GuiEffect.PickOpenDocument(E, jset(["pl"])), m.PickOpenDocument("e")),
    (GuiEffect.PickSaveDestination(E, D, "a.pl"), m.PickSaveDestination("e", "document-1", "a.pl")),
    (
        GuiEffect.WriteDocument(E, D, ORIGIN, "x.", 3),
        m.WriteDocument("e", "document-1", FILE, "x.", 3),
    ),
    (
        GuiEffect.WriteDocument(E, D, DocumentOrigin("web", "h", "a.pl"), "x.", 3),
        m.WriteDocument("e", "document-1", None, "x.", 3),
    ),
    (GuiEffect.ReadDocument(E, D, ORIGIN), m.ReadDocument("e", "document-1", FILE)),
    (
        GuiEffect.ConfirmCloseDirtyPage(E, P, D, "a.pl"),
        m.ConfirmCloseDirtyPage("e", "page-1", "document-1", "a.pl"),
    ),
    (
        GuiEffect.ConfirmReloadDirtyDocument(E, D, "a.pl"),
        m.ConfirmReloadDirtyDocument("e", "document-1", "a.pl"),
    ),
    (
        GuiEffect.ConfirmExitWithDirtyDocuments(E, jlist([D])),
        m.ConfirmExitWithDirtyDocuments("e", ("document-1",)),
    ),
    (GuiEffect.CopyTextToClipboard(E, "t"), m.CopyToClipboard("e", "t")),
    (GuiEffect.ExitApplication(E), m.ExitApplication("e")),
]


@pytest.mark.parametrize("effect, expected", EFFECTS, ids=lambda x: type(x).__name__)
def test_effects_convert(effect, expected):
    assert bridge_module.convert_effect(effect) == expected


def test_unknown_effects_are_rejected():
    with pytest.raises(ValueError):
        bridge_module.convert_effect(SimpleNamespace(id="e"))


class Recorder:
    def __init__(self):
        self.states = queue.Queue()
        self.effects = queue.Queue()
        self.errors = queue.Queue()
        self.last = m.Snapshot()

    def start(self, bridge):
        bridge.start(self.states.put, self.effects.put, self.errors.put)

    def wait(self, condition):
        while not condition(self.last):
            self.last = self.states.get(timeout=TIMEOUT)
        return self.last


def test_jvm_bridge_solves_end_to_end():
    recorder = Recorder()
    bridge = tui.JvmGuiBridge(timeout=10)
    with pytest.raises(RuntimeError):
        bridge.dispatch(m.RequestExit())
    recorder.start(bridge)
    recorder.start(bridge)  # idempotent
    try:
        bridge.dispatch(m.NewScratchPage("demo", "p(1). p(2). p("))
        state = recorder.wait(lambda s: s.selected_page is not None)
        page = state.selected_page
        assert (page.title, page.document_id) == ("demo", None)
        assert page.diagnostics and page.diagnostics[0].message.startswith("ERROR 1:")
        assert (page.diagnostics[0].line, page.diagnostics[0].column) == (0, 14)
        assert page.timeout == "10s"
        bridge.dispatch(m.ChangeTimeout(page.id, "1m 30s"))
        recorder.wait(lambda s: s.page(page.id).timeout == "1m 30s")
        bridge.dispatch(m.ChangeScratchText(page.id, "p(1). p(2). :- write(hi)."))
        bridge.dispatch(m.ChangeQuery(page.id, "p(X), write(X)"))
        bridge.dispatch(m.Solve(page.id, "ONE"))
        state = recorder.wait(lambda s: s.page(page.id).resolution.can_continue)
        resolution = state.page(page.id).resolution
        assert resolution.solutions[0] == m.Solution(
            "yes", "p(X), write(X)", (("X", "1"),), "p(1), write(1)"
        )
        bridge.dispatch(m.Next(page.id, "TEN"))
        state = recorder.wait(lambda s: s.page(page.id).history)
        assert state.page(page.id).history[0].status == "COMPLETED"
        assert "12" in state.page(page.id).stdout
        inspection = state.page(page.id).inspection
        assert (700, "XFX", "=") in inspection.operators
        assert ("unknown", "warning") in [(name, value) for name, value, _ in inspection.flags]
        lang = next(lib for lib in inspection.libraries if lib.alias == "prolog.lang")
        assert "member/2" in dict(lang.documentation) and lang.help
        assert "op(700, XFX, =)" in dict(lang.documentation)
        assert bridge.documentation_preview(dict(lang.documentation)["member/2"])
        assert "prolog.lang" in [library.alias for library in inspection.libraries]
        assert "p(1)" in inspection.static_kb
        bridge.dispatch(m.ChangeFlag(page.id, "unknown", "fail"))
        bridge.dispatch(m.ChangeQuery(page.id, "current_flag(unknown, fail)"))
        bridge.dispatch(m.Solve(page.id, "ALL"))
        state = recorder.wait(lambda s: len(s.page(page.id).history) == 2)
        assert state.page(page.id).history[-1].solutions[0].kind == "yes"
        bridge.dispatch(m.ClearHistory(page.id))
        recorder.wait(lambda s: not s.page(page.id).history)
        bridge.dispatch(m.ChangeQuery(page.id, "q"))
        bridge.dispatch(m.Solve(page.id, "ONE"))
        state = recorder.wait(lambda s: len(s.page(page.id).history) == 1)
        assert state.page(page.id).history[-1].solutions[0].kind in ("no", "halt")
        bridge.dispatch(m.NewDocumentPage("a.pl", "x."))
        state = recorder.wait(lambda s: s.selected_page.document_id is not None)
        assert state.selected_page.dirty and state.selected_page.source == "x."
        bridge.dispatch(m.RequestExit())
        assert isinstance(recorder.effects.get(timeout=TIMEOUT), m.ConfirmExitWithDirtyDocuments)
    finally:
        bridge.close()
        bridge.close()
    assert recorder.errors.empty()


async def test_ide_solves_end_to_end():
    app = tui.PrologTui()
    async with app.run_test(size=(120, 40)) as pilot:
        for _ in range(TIMEOUT * 10):
            await pilot.pause(0.1)
            if app.snapshot.selected_page is not None:
                break
        app.query_one("#source", TextArea).insert("p(1).")
        app.query_one("#query", Input).focus()
        await pilot.press(*"p(X)", "enter")
        for _ in range(TIMEOUT * 10):
            await pilot.pause(0.1)
            if "X = 1" in app.query_one("#solutions", TextArea).text:
                break
        assert "yes: p(1)" in app.query_one("#solutions", TextArea).text
        await pilot.press("ctrl+q")
        await pilot.pause(0.5)
    assert app._closed


def test_console_script():
    (script,) = [e for e in entry_points(group="console_scripts") if e.name == "2ppy-tui"]
    assert script.load() is tui.main


@pytest.mark.filterwarnings("ignore:.*found in sys.modules:RuntimeWarning")
def test_main_module(monkeypatch):
    runs = []
    monkeypatch.setattr(tui.PrologTui, "run", lambda self: runs.append(self))
    monkeypatch.setattr("sys.argv", ["2ppy-tui"])
    runpy.run_module("tuprolog.tui", run_name="__main__")
    assert len(runs) == 1 and isinstance(runs[0].bridge, tui.JvmGuiBridge)


def test_jvm_bridge_analyzes_prolog_text():
    bridge = tui.JvmGuiBridge()
    assert bridge.is_timeout("2s 500ms") and not bridge.is_timeout("soon")
    assert [t.category for t in bridge.analyze("p(X).")] == [
        "FUNCTOR",
        "PARENTHESIS",
        "VARIABLE",
        "PARENTHESIS",
        "FULL_STOP",
    ]
    assert bridge.analyze("% a\n% b")[1] == m.SyntaxToken("COMMENT", (1, 0), (1, 3))
    tokens = bridge.analyze("a === b.", ((700, "XFX", "==="),))
    assert m.SyntaxToken("OPERATOR", (0, 2), (0, 5)) in tokens
