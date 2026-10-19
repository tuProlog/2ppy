"""Tests for the Textual application of `tuprolog.tui`, driven headlessly against a fake bridge."""

import time
from pathlib import Path

import pytest
from rich.text import Text
from textual.widgets import Button, DataTable, Input, OptionList, Tabs, TextArea, Tree

from tuprolog.tui import (
    ChangeDocumentText,
    ChangeFlag,
    ChangeQuery,
    ChangeScratchText,
    ChangeStdin,
    ChangeTimeout,
    ClearHistory,
    ClosePageDecision,
    ConfirmCloseDirtyPage,
    ConfirmExitWithDirtyDocuments,
    ConfirmReloadDirtyDocument,
    CopyToClipboard,
    DiagnosticEntry,
    ExitApplication,
    ExitCancelled,
    ExitConfirmed,
    HistoryEntry,
    Inspection,
    LibraryEntry,
    MarkPanelRead,
    NewDocumentPage,
    NewScratchPage,
    Next,
    OpenDocumentLoaded,
    PickOpenDocument,
    PickSaveDestination,
    PrologTui,
    ReadDocument,
    ReloadDecision,
    ReloadFailed,
    ReloadSucceeded,
    RequestClosePage,
    RequestExit,
    RequestOpenDocument,
    RequestReload,
    RequestSave,
    Reset,
    Resolution,
    SaveCancelled,
    SaveDestinationSelected,
    SaveFailed,
    SaveSucceeded,
    SelectPage,
    Solution,
    Solve,
    Stop,
    WriteDocument,
)
from tuprolog.tui._app import StateChanged, format_solutions
from tuprolog.tui._screens import ChoiceScreen, DocumentationScreen, PathScreen, PromptScreen

from .fakes import FakeBridge, page, snapshot

SIZE = (120, 40)


@pytest.fixture
def bridge():
    return FakeBridge()


async def until(pilot, condition, timeout=10.0):
    """Waits for a condition, e.g. a screen being pushed or dismissed, as slow runners may need."""
    deadline = time.monotonic() + timeout
    while not condition():
        assert time.monotonic() < deadline, "Timed out"
        await pilot.pause(0.02)


def _laid_out(app, selector):
    try:
        widget = app.screen.query_one(selector)
    except Exception:  # noqa: BLE001  (not mounted yet)
        return False
    return widget.display and widget.region.area > 0


async def click(pilot, selector):
    """Clicks a widget once laid out: right after its tab or screen is shown, slow runners may not
    have placed it yet, and the click would land elsewhere."""
    await until(pilot, lambda: _laid_out(pilot.app, selector))
    await pilot.pause()
    await pilot.click(selector)


async def show(pilot, bridge, state):
    bridge.emit(state)
    await pilot.pause()
    await pilot.pause()


def text(app, widget_id):
    return app.query_one(f"#{widget_id}", TextArea).text


def label(app, button_id):
    return str(app.query_one(f"#{button_id}", Button).label)


def disabled(app, button_id):
    return app.query_one(f"#{button_id}", Button).disabled


async def test_startup_creates_a_scratch_page(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        assert bridge.started == 1
        assert bridge.actions == [NewScratchPage()]
        await show(pilot, bridge, snapshot(page(source="p(1).", query="p(X)")))
        assert text(app, "source") == "p(1)."
        assert app.query_one("#query", Input).value == "p(X)"
        assert app.query_one("#pages", Tabs).active == "tab-page-1"
        assert bridge.actions == [NewScratchPage()]  # programmatic updates are not sent back
    assert bridge.closed == 1


async def test_edits_target_the_shown_page(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page("page-1"), page("page-2"), selected="page-2"))
        app.query_one("#source", TextArea).insert("q.")
        app.query_one("#query", Input).focus()
        await pilot.press("q")
        app.query_one("#stdin", TextArea).insert("in")
        await pilot.pause()
        assert bridge.of_type(ChangeScratchText) == [ChangeScratchText("page-2", "q.")]
        assert bridge.of_type(ChangeQuery) == [ChangeQuery("page-2", "q")]
        assert bridge.of_type(ChangeStdin) == [ChangeStdin("page-2", "in")]


async def test_document_edits_target_the_document(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(document_id="document-1", source="a.")))
        app.query_one("#source", TextArea).insert("b. ")
        await pilot.pause()
        assert bridge.of_type(ChangeDocumentText) == [ChangeDocumentText("document-1", "b. a.")]


async def test_solving_shows_the_result(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(query="p(X)")))
        await pilot.press("f5")
        assert bridge.of_type(Solve) == [Solve("page-1", "ONE")]
        yes = Solution("yes", "p(X)", bindings=(("X", "1"),), solved_query="p(1)")
        done = page(
            query="p(X)",
            resolution=Resolution("COMPLETED", "p(X)", (yes,)),
            history=(HistoryEntry("p(X)", (yes,), "COMPLETED"),),
        )
        await show(pilot, bridge, snapshot(done))
        assert text(app, "solutions") == "?- p(X)\nyes: p(1)\n    X = 1"


async def test_solve_10_becomes_next_10(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(query="p(X)")))
        await click(pilot, "#solve-ten")
        assert bridge.of_type(Solve) == [Solve("page-1", "TEN")]
        awaiting = Resolution(
            "AWAITING_CONTINUATION",
            "p(X)",
            (Solution("yes", "p(X)"),),
            can_solve=False,
            can_continue=True,
            can_stop=True,
        )
        await show(pilot, bridge, snapshot(page(query="p(X)", resolution=awaiting)))
        assert [label(app, b) for b in ("solve-one", "solve-ten", "solve-hundred")] == [
            "Next",
            "Next 10",
            "Next 100",
        ]
        assert "more solutions may follow" in text(app, "solutions")
        await pilot.press("f6", "f7")
        assert bridge.of_type(Next) == [Next("page-1", "TEN"), Next("page-1", "HUNDRED")]


async def test_stop_and_reset_follow_the_model(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page()))
        assert disabled(app, "stop") and not disabled(app, "solve-one")
        await pilot.press("f8")
        assert bridge.of_type(Stop) == []
        running = Resolution("RUNNING", "p", can_solve=False, can_stop=True)
        await show(pilot, bridge, snapshot(page(resolution=running)))
        assert not disabled(app, "stop") and disabled(app, "solve-one")
        await click(pilot, "#stop")
        await click(pilot, "#reset")
        assert bridge.of_type(Stop) == [Stop("page-1")]
        assert bridge.of_type(Reset) == [Reset("page-1")]


async def test_late_results_stay_on_their_page(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page("page-1"), page("page-2")))
        app.query_one("#pages", Tabs).active = "tab-page-2"
        await pilot.pause()
        assert bridge.of_type(SelectPage) == [SelectPage("page-2")]
        late = HistoryEntry("late", (Solution("no", "late"),), "COMPLETED")
        # a result of page-1, arriving before the selection is applied
        await show(pilot, bridge, snapshot(page("page-1", history=(late,)), page("page-2")))
        assert app.query_one("#pages", Tabs).active == "tab-page-2"
        await show(
            pilot,
            bridge,
            snapshot(page("page-1", history=(late,)), page("page-2"), selected="page-2"),
        )
        assert text(app, "solutions") == ""
        await show(
            pilot,
            bridge,
            snapshot(page("page-1", history=(late,)), page("page-2"), selected="page-1"),
        )
        assert "late" in text(app, "solutions")


async def test_stale_states_do_not_overwrite_newer_input(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page()))
        app.query_one("#query", Input).focus()
        await pilot.press("a", "b", "c")
        query = app.query_one("#query", Input)
        await show(pilot, bridge, snapshot(page(query="a")))
        assert query.value == "abc"
        await show(pilot, bridge, snapshot(page(query="abc")))
        await show(pilot, bridge, snapshot(page(query="xyz")))  # e.g. changed by the model
        assert query.value == "xyz"


async def test_selecting_a_page_loads_its_values(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page("page-1"), page("page-2", source="two.")))
        app.query_one("#query", Input).focus()
        await pilot.press("x")
        await show(
            pilot,
            bridge,
            snapshot(page("page-1"), page("page-2", source="two.", query="q"), selected="page-2"),
        )
        assert text(app, "source") == "two."
        assert app.query_one("#query", Input).value == "q"


async def test_panels_render_and_are_marked_read(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        state = page(
            stdout="hello",
            stderr="oops",
            warnings=("careful",),
            diagnostics=(DiagnosticEntry("ERROR 1:2: unexpected", 0, 1),),
            unread=frozenset({"SOLUTIONS", "STDOUT", "DIAGNOSTICS"}),
        )
        await show(pilot, bridge, snapshot(state))
        await show(pilot, bridge, snapshot(state))
        assert [text(app, w) for w in ("stdout", "stderr", "warnings")] == [
            "hello",
            "oops",
            "careful",
        ]
        diagnostics = app.query_one("#diagnostics", OptionList)
        assert str(diagnostics.get_option_at_index(0).prompt) == "ERROR 1:2: unexpected"
        assert bridge.of_type(MarkPanelRead) == [MarkPanelRead("page-1", "SOLUTIONS")]
        await click(pilot, "#--content-tab-panel-stdout")
        await pilot.pause()
        assert MarkPanelRead("page-1", "STDOUT") in bridge.actions
        assert MarkPanelRead("page-1", "DIAGNOSTICS") not in bridge.actions


async def test_commands(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(document_id="document-1")))
        for key in ["ctrl+t", "ctrl+n", "ctrl+o", "ctrl+s", "ctrl+e", "ctrl+r", "ctrl+w"]:
            await pilot.press(key)
        assert bridge.actions[1:] == [
            NewScratchPage(),
            NewDocumentPage(),
            RequestOpenDocument(),
            RequestSave("document-1", False),
            RequestSave("document-1", True),
            RequestReload("document-1"),
            RequestClosePage("page-1"),
        ]
        await pilot.press("ctrl+q")
        assert bridge.actions[-1] == RequestExit()


async def test_scratch_pages_are_not_saved(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page()))
        await pilot.press("ctrl+s")
        assert bridge.of_type(RequestSave) == []


@pytest.mark.parametrize(
    "button, decision", [("save", "SAVE"), ("discard", "DISCARD"), ("cancel", "CANCEL")]
)
async def test_dirty_close_confirmation(bridge, button, decision):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(document_id="document-1", dirty=True)))
        bridge.effect(ConfirmCloseDirtyPage("e1", "page-1", "document-1", "a.pl"))
        await pilot.pause()
        await click(pilot, f"#choice-{button}")
        await pilot.pause()
        assert bridge.of_type(ClosePageDecision) == [ClosePageDecision("page-1", decision)]


@pytest.mark.parametrize("key, action", [("enter", ExitConfirmed()), ("escape", ExitCancelled())])
async def test_dirty_exit_confirmation(bridge, key, action):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        bridge.effect(ConfirmExitWithDirtyDocuments("e1", ("document-1",)))
        await pilot.pause()
        await pilot.press(key)  # the first button (Quit) has focus
        await pilot.pause()
        assert bridge.actions[-1] == action


async def test_dirty_reload_confirmation(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        bridge.effect(ConfirmReloadDirtyDocument("e1", "document-1", "a.pl"))
        await pilot.pause()
        await click(pilot, "#choice-discard-changes")
        await pilot.pause()
        assert bridge.actions[-1] == ReloadDecision("document-1", "DISCARD_CHANGES")


async def type_path(pilot, path):
    await until(pilot, lambda: isinstance(pilot.app.screen, PathScreen))
    field = pilot.app.screen.query_one("#path", Input)
    field.value = str(path)
    await pilot.press("enter")
    await pilot.pause()


async def test_open_file(bridge, tmp_path):
    file = tmp_path / "theory.pl"
    file.write_text("p(è).", encoding="utf-8")
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        bridge.effect(PickOpenDocument("e1"))
        await pilot.pause()
        await type_path(pilot, file)
        assert bridge.actions[-1] == OpenDocumentLoaded(file, "p(è).")
        bridge.effect(PickOpenDocument("e2"))
        await pilot.pause()
        await type_path(pilot, tmp_path / "missing.pl")
        bridge.effect(PickOpenDocument("e3"))
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert len(bridge.of_type(OpenDocumentLoaded)) == 1


async def test_save_destination(bridge, tmp_path):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        bridge.effect(PickSaveDestination("e1", "document-1", "untitled.pl"))
        await pilot.pause()
        await until(pilot, lambda: isinstance(pilot.app.screen, PathScreen))
        assert pilot.app.screen.query_one("#path", Input).value == "untitled.pl"
        await type_path(pilot, tmp_path / "a.pl")
        assert bridge.actions[-1] == SaveDestinationSelected("document-1", tmp_path / "a.pl")
        bridge.effect(PickSaveDestination("e2", "document-1", "untitled.pl"))
        await pilot.pause()
        await click(pilot, "#cancel")
        await pilot.pause()
        assert bridge.actions[-1] == SaveCancelled("document-1")


async def test_write_document(bridge, tmp_path):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        file = tmp_path / "a.pl"
        bridge.effect(WriteDocument("e1", "document-1", file, "p(è).", 3))
        await pilot.pause()
        assert file.read_text(encoding="utf-8") == "p(è)."
        assert bridge.actions[-1] == SaveSucceeded("document-1", file, 3)
        bridge.effect(WriteDocument("e2", "document-1", tmp_path, "x", 4))  # a directory
        await pilot.pause()
        assert isinstance(bridge.actions[-1], SaveFailed)
        bridge.effect(WriteDocument("e3", "document-1", None, "x", 5))
        await pilot.pause()
        assert bridge.actions[-1] == SaveFailed("document-1", "Not a file")


async def test_read_document(bridge, tmp_path):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        file = tmp_path / "a.pl"
        file.write_text("q.", encoding="utf-8")
        bridge.effect(ReadDocument("e1", "document-1", file))
        await pilot.pause()
        assert bridge.actions[-1] == ReloadSucceeded("document-1", "q.")
        bridge.effect(ReadDocument("e2", "document-1", tmp_path / "missing.pl"))
        await pilot.pause()
        assert isinstance(bridge.actions[-1], ReloadFailed)
        bridge.effect(ReadDocument("e3", "document-1", None))
        await pilot.pause()
        assert bridge.actions[-1] == ReloadFailed("document-1", "Not a file")


async def test_clipboard_and_exit_effects_are_handled_once(bridge, monkeypatch):
    app = PrologTui(bridge)
    copied = []
    monkeypatch.setattr(app, "copy_to_clipboard", copied.append)
    async with app.run_test(size=SIZE) as pilot:
        bridge.effect(CopyToClipboard("e1", "text"))
        await pilot.pause()
        assert copied == ["text"]
        bridge.effect(ExitApplication("e2"))
        bridge.effect(ExitApplication("e3"))  # e.g. a late duplicate: no second shutdown
    assert bridge.closed == 1
    assert app.return_code == 0


async def test_errors_are_notified(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        bridge.on_error("boom")
        await pilot.pause()
        assert any("boom" in str(n.message) for n in app._notifications)


def test_format_solutions():
    halt = Solution("halt", "q", message="error", is_timeout=False)
    timeout = Solution("halt", "q", message="too long", is_timeout=True)
    history = (
        HistoryEntry("q", (halt,), "FAILED", "error"),
        HistoryEntry("r", (), "FAILED", "syntax"),
        HistoryEntry("s", (timeout,), "CANCELLED"),
    )
    assert format_solutions(page(history=history)) == (
        "?- q\nhalt: error\n\n?- r\nerror: syntax\n\n?- s\ntimeout: too long\n... stopped"
    )
    running = Resolution("RUNNING", "t", can_solve=False, can_stop=True)
    assert format_solutions(page(resolution=running)) == "?- t\n... running"


def test_paths_are_paths():
    assert isinstance(SaveSucceeded("d", Path("a"), 1).path, Path)


async def test_states_do_not_overwrite_input_whose_change_is_still_queued(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page()))
        app.query_one("#query", Input).value = "p"  # its Changed message is still queued
        await app.render_state(StateChanged(snapshot(page(query=""))))
        assert app.query_one("#query", Input).value == "p"
        await pilot.pause()
        assert bridge.of_type(ChangeQuery) == [ChangeQuery("page-1", "p")]


async def test_queued_changes_of_another_page_are_dropped(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page("page-1"), page("page-2", query="two")))
        app.query_one("#query", Input).value = "one"  # queued while page-1 is shown
        await app.render_state(
            StateChanged(snapshot(page("page-1"), page("page-2", query="two"), selected="page-2"))
        )
        await pilot.pause()
        assert app.query_one("#query", Input).value == "two"
        assert bridge.of_type(ChangeQuery) == []


async def test_title():
    app = PrologTui(FakeBridge())
    async with app.run_test(size=SIZE):
        assert app.title == "2ppy TUI"


async def test_panels_are_those_of_the_swing_ide(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page()))
        labels = [str(tab.label) for tab in app.query_one("#panels").query("ContentTab")]
        assert labels == [
            "Solutions",
            "Stdin",
            "Stdout",
            "Stderr",
            "Warnings",
            "Diagnostics",
            "Operators",
            "Flags",
            "Libraries",
            "Static KB",
            "Dynamic KB",
        ]


INSPECTION = Inspection(
    operators=((700, "XFX", "="),),
    flags=(("unknown", "error", "`flag(unknown)`\nWhat unknown predicates do."),),
    libraries=(
        LibraryEntry(
            "prolog.lang",
            predicates=("member/2",),
            functions=("abs/1",),
            help="`library(prolog.lang)`\nThe standard library.",
            documentation=(("member/2", "`member(?X, ?L)`\nX is in L."),),
        ),
    ),
    static_kb="p(1) :- true.",
    dynamic_kb="q(2) :- true.",
)


async def test_inspection_panels_render(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(inspection=INSPECTION)))
        assert app.query_one("#operators", DataTable).get_row_at(0) == [700, "XFX", "="]
        assert app.query_one("#flags", DataTable).get_row_at(0) == ["unknown", "error"]
        library = app.query_one("#libraries", Tree).root.children[0]
        assert str(library.label) == "prolog.lang"
        assert [str(group.label) for group in library.children] == [
            "Predicates (1)",
            "Functions (1)",
        ]
        assert text(app, "static_kb") == "p(1) :- true."
        assert text(app, "dynamic_kb") == "q(2) :- true."


async def test_flags_are_edited(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(inspection=INSPECTION)))
        await click(pilot, "#--content-tab-panel-flags")
        app.query_one("#flags", DataTable).focus()
        await pilot.press("enter")
        await until(
            pilot, lambda: isinstance(app.screen, PromptScreen) and isinstance(app.focused, Input)
        )
        app.screen.query_one(Input).value = "fail"
        await pilot.press("enter")
        assert bridge.of_type(ChangeFlag) == [ChangeFlag("page-1", "unknown", "fail")]
        running = Resolution("RUNNING", "p", can_solve=False, can_stop=True)
        await show(pilot, bridge, snapshot(page(inspection=INSPECTION, resolution=running)))
        assert app.query_one("#flags", DataTable).disabled


async def test_solutions_are_cleared_and_solved_all(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page()))
        assert disabled(app, "clear-solutions")
        await click(pilot, "#solve-all")
        assert bridge.of_type(Solve) == [Solve("page-1", "ALL")]
        history = (HistoryEntry("p", (Solution("no", "p"),), "COMPLETED"),)
        await show(pilot, bridge, snapshot(page(history=history)))
        await click(pilot, "#clear-solutions")
        assert bridge.of_type(ClearHistory) == [ClearHistory("page-1")]


async def test_diagnostics_lead_to_the_source(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        diagnostic = DiagnosticEntry("ERROR 2:3: unexpected", 1, 2)
        await show(pilot, bridge, snapshot(page(source="p.\nq(.", diagnostics=(diagnostic,))))
        await click(pilot, "#--content-tab-panel-diagnostics")
        app.query_one("#diagnostics", OptionList).focus()
        await pilot.press("down", "enter")
        source = app.query_one("#source", TextArea)
        assert source.has_focus and source.cursor_location == (1, 2)


async def test_arrow_keys_move_among_controls(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page()))
        app.query_one("#solve-one", Button).focus()
        await pilot.press("right")
        assert app.focused.id == "solve-ten"
        await pilot.press("down", "left", "up")  # down and up move too
        assert app.focused.id == "solve-one"
        await pilot.press("left", "left")  # the query keeps the arrow keys it uses
        assert app.focused.id == "query"
        bridge.effect(ConfirmExitWithDirtyDocuments("e", ("document-1",)))
        await pilot.pause()
        await until(
            pilot, lambda: isinstance(app.screen, ChoiceScreen) and _laid_out(app, "#choice-quit")
        )
        app.screen.query_one("#choice-quit", Button).focus()
        await pilot.press("right", "enter")
        assert bridge.of_type(ExitCancelled) == [ExitCancelled()]


async def test_timeout_is_edited(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(timeout="5s")))
        timeout = app.query_one("#timeout", Input)
        assert timeout.value == "5s"
        timeout.focus()
        timeout.value = "2s 500ms"
        await pilot.press("enter")
        assert bridge.of_type(ChangeTimeout) == [ChangeTimeout("page-1", "2s 500ms")]
        timeout.value = "soon"
        await pilot.press("tab")  # leaving the field commits it too
        await pilot.pause()
        assert timeout.value == "5s"
        assert any("Invalid timeout" in str(n.message) for n in app._notifications)
        assert len(bridge.of_type(ChangeTimeout)) == 1
        running = Resolution("RUNNING", "p", can_solve=False, can_stop=True)
        await show(pilot, bridge, snapshot(page(timeout="5s", resolution=running)))
        assert timeout.disabled


@pytest.mark.parametrize(
    "source, answer, expected",
    [
        ("p.", "700 XFX ===", "p.\n:- op(700, xfx, ===).\n"),
        ("", "200 fy ~", ":- op(200, fy, ~).\n"),
        ("p.", "1300 xfx ===", "p."),
        ("p.", "700 xxx ===", "p."),
    ],
)
async def test_operators_are_added_to_the_theory(bridge, source, answer, expected):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(source=source)))
        await click(pilot, "#--content-tab-panel-operators")
        await click(pilot, "#add-operator")
        await until(
            pilot, lambda: isinstance(app.screen, PromptScreen) and isinstance(app.focused, Input)
        )
        app.screen.query_one(Input).value = answer
        await pilot.press("enter")
        await pilot.pause()
        assert text(app, "source") == expected
        if expected == source:
            assert any("Invalid operator" in str(n.message) for n in app._notifications)
        else:
            assert bridge.of_type(ChangeScratchText)[-1] == ChangeScratchText("page-1", expected)


async def test_prolog_text_is_highlighted(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(source="ab\ncd", query="ef")))
        # the fake bridge finds a variable per word: highlighted as types
        assert app.query_one("#source", TextArea)._highlights[1] == [(0, 2, "type")]
        highlighter = app.query_one("#query", Input).highlighter
        assert highlighter is not None and highlighter(Text("ef")).spans
        inspection = Inspection(static_kb="gh :- true.")
        await show(pilot, bridge, snapshot(page(inspection=inspection)))
        assert app.query_one("#static_kb", TextArea)._highlights[0][0] == (0, 2, "type")


def preview(app, panel):
    return str(app.query_one(f"#{panel}-preview").render())


async def test_flags_are_documented(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(inspection=INSPECTION)))
        await click(pilot, "#--content-tab-panel-flags")
        assert preview(app, "flags") == "`flag(unknown)`"  # the fake bridge's: the first line
        await pilot.press("f1")
        await until(pilot, lambda: isinstance(app.screen, DocumentationScreen))
        await pilot.press("escape")
        await until(pilot, lambda: not isinstance(app.screen, DocumentationScreen))
        await click(pilot, "#flags-documentation")
        await until(pilot, lambda: isinstance(app.screen, DocumentationScreen))
        await click(pilot, "#close")
        await until(pilot, lambda: not isinstance(app.screen, DocumentationScreen))


async def test_libraries_are_documented(bridge):
    app = PrologTui(bridge)
    async with app.run_test(size=SIZE) as pilot:
        await show(pilot, bridge, snapshot(page(inspection=INSPECTION)))
        await click(pilot, "#--content-tab-panel-libraries")
        tree = app.query_one("#libraries", Tree)
        tree.focus()
        tree.root.expand_all()
        await pilot.press("down")  # the library
        assert preview(app, "libraries") == "`library(prolog.lang)`"
        await pilot.press("down", "down")  # Predicates, then member/2
        assert preview(app, "libraries") == "`member(?X, ?L)`"
        await pilot.press("enter")
        await until(pilot, lambda: isinstance(app.screen, DocumentationScreen))
        await pilot.press("escape")
        await until(pilot, lambda: not isinstance(app.screen, DocumentationScreen))
        await pilot.press("down", "down")  # Functions, then abs/1: undocumented
        assert preview(app, "libraries") == ""
        await pilot.press("enter", "f1")
        await until(pilot, lambda: not isinstance(app.screen, DocumentationScreen))
        assert any("No documentation" in str(n.message) for n in app._notifications)
