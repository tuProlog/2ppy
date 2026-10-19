"""End-to-end tests of every feature of the terminal IDE: the real Textual application, on 2P-Kt's
GUI application (on the JVM), started as the command line would, and driven by keys and clicks."""

from __future__ import annotations

import asyncio
import contextlib
import time
from collections.abc import AsyncIterator, Callable
from pathlib import Path

import pytest
from textual.pilot import Pilot
from textual.widgets import (
    Button,
    DataTable,
    Input,
    Markdown,
    OptionList,
    Tab,
    TabbedContent,
    Tabs,
    TextArea,
    Tree,
)

from tuprolog.tui import PrologTui, parse_command_line
from tuprolog.tui._screens import ChoiceScreen, DocumentationScreen, PathScreen, PromptScreen

SIZE = (140, 45)
TIMEOUT = 30.0  # seconds
RESOURCES = Path(__file__).parent / "resources"


class Ide:
    """The IDE under test, with helpers to drive it and read it."""

    def __init__(self, app: PrologTui, pilot: Pilot) -> None:
        self.app = app
        self.pilot = pilot

    # --- waiting ---

    async def until(self, condition: Callable[[], object], timeout: float = TIMEOUT) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            await self.pilot.pause(0.05)
            try:
                if condition():
                    return
            except Exception:  # noqa: BLE001, S110  (e.g. a widget not mounted yet)
                pass
        raise AssertionError(f"Timed out; solutions: {self.text('solutions')!r}")

    async def settle(self) -> None:
        """Waits for the model to acknowledge the local input."""
        await self.until(
            lambda: (
                self.page is not None
                and self.page.source == self.text("source")
                and self.page.query == self.query.value
                and self.page.stdin == self.text("stdin")
            )
        )

    # --- reading ---

    @property
    def page(self):
        return self.app.snapshot.selected_page

    @property
    def pages(self):
        return self.app.snapshot.pages

    @property
    def query(self) -> Input:
        return self.app.query_one("#query", Input)

    def text(self, widget_id: str) -> str:
        return self.app.query_one(f"#{widget_id}", TextArea).text

    def diagnostics(self) -> list[str]:
        options = self.app.query_one("#diagnostics", OptionList)
        return [str(options.get_option_at_index(i).prompt) for i in range(options.option_count)]

    def label(self, button_id: str) -> str:
        return str(self.app.query_one(f"#{button_id}", Button).label)

    def enabled(self, button_id: str) -> bool:
        return not self.app.query_one(f"#{button_id}", Button).disabled

    def tab_labels(self) -> list[str]:
        tabs = self.app.query_one("#pages", Tabs)
        return [str(tab.label) for tab in tabs.query(Tab)]

    def panel_label(self, panel: str) -> str:
        return str(self.app.query_one("#panels", TabbedContent).get_tab(f"panel-{panel}").label)

    def notifications(self) -> list[str]:
        return [str(n.message) for n in self.app._notifications]

    async def outcome(self) -> str:
        """Waits for the first solution of the current resolution, and returns its kind (or
        `"error"`, if the resolution failed without solutions, e.g. for a syntax error)."""
        await self.until(
            lambda: self.page.resolution.solutions or self.page.resolution.status == "FAILED"
        )
        solutions = self.page.resolution.solutions
        return solutions[0].kind if solutions else "error"

    # --- acting ---

    async def write_theory(self, text: str) -> None:
        editor = self.app.query_one("#source", TextArea)
        editor.focus()
        editor.select_all()
        editor.replace(text, *editor.selection)  # as typing would
        await self.settle()

    async def type_query(self, text: str) -> None:
        self.query.focus()
        self.query.value = ""
        await self.pilot.press(*text) if text else None
        await self.settle()

    async def solve(self, query: str, key: str = "f5") -> None:
        """Solves a query, waiting until it concludes or awaits continuation."""
        await self.type_query(query)
        await self.pilot.press(key)
        await self.until(
            lambda: (
                self.page.resolution.query == query
                and self.page.resolution.status not in ("IDLE", "RUNNING")
            )
        )

    async def click(self, selector: str) -> None:
        """Clicks a widget once laid out: right after its tab or screen is shown, slow runners may
        not have placed it yet, and the click would land elsewhere."""

        def laid_out() -> bool:
            widget = self.app.screen.query_one(selector)
            return bool(widget.display) and widget.region.area > 0

        await self.until(laid_out)
        await self.pilot.click(selector)

    async def answer_path(self, path: Path | str) -> None:
        await self.until(lambda: isinstance(self.app.screen, PathScreen))
        self.app.screen.query_one("#path", Input).value = str(path)
        await self.pilot.press("enter")
        await self.until(lambda: not isinstance(self.app.screen, PathScreen))

    async def until_exited(self) -> None:
        """Waits for the IDE to exit (without the pilot, which stops working meanwhile)."""
        deadline = time.monotonic() + TIMEOUT
        while self.app.is_running and time.monotonic() < deadline:
            await asyncio.sleep(0.05)
        assert not self.app.is_running

    async def choose(self, button_id: str) -> None:
        await self.until(lambda: isinstance(self.app.screen, ChoiceScreen))
        await self.click(f"#{button_id}")
        await self.until(lambda: not isinstance(self.app.screen, ChoiceScreen))


@contextlib.asynccontextmanager
async def ide(*argv: str, pages: int = 1) -> AsyncIterator[Ide]:
    # a generous default timeout, as runners may be slow and busy (e.g. with the computations of
    # earlier tests, which 2P-Kt cannot interrupt); tests passing --timeout override it
    bridge, startup = parse_command_line(["--timeout", "60", *argv])
    app = PrologTui(bridge, startup)
    async with app.run_test(size=SIZE) as pilot:
        driver = Ide(app, pilot)
        await driver.until(lambda: len(driver.pages) >= pages and driver.page is not None)
        await driver.settle()
        yield driver
        if app.is_running:
            app.exit()
    assert app._closed


# --- startup ----------------------------------------------------------------------------------


async def test_starts_with_a_scratch_page():
    async with ide() as t:
        assert len(t.pages) == 1 and t.page.document_id is None
        assert t.tab_labels() == [t.page.title]
        assert t.enabled("solve-one") and t.enabled("reset") and not t.enabled("stop")
        assert [t.label(b) for b in ("solve-one", "solve-ten", "solve-hundred")] == [
            "Solve",
            "Solve 10",
            "Solve 100",
        ]


# --- editing and solving ------------------------------------------------------------------------


async def test_theory_edits_reach_the_solver():
    async with ide() as t:
        await t.write_theory("parent(abe, homer). parent(homer, bart).")
        await t.solve("parent(abe, X)")
        assert "yes: parent(abe, homer)\n    X = homer" in t.text("solutions")


async def test_enter_in_the_query_solves():
    async with ide("-t", "p(1).") as t:
        await t.type_query("p(X)")
        await t.pilot.press("enter")
        await t.until(lambda: "X = 1" in t.text("solutions"))


async def test_solve_one_then_next_until_exhausted():
    async with ide("-t", "p(1). p(2). p(3).") as t:
        await t.solve("p(X)")
        assert t.label("solve-one") == "Next" and t.label("solve-ten") == "Next 10"
        assert t.enabled("stop")
        assert "more solutions may follow" in t.text("solutions")
        await t.pilot.press("f5")
        await t.until(lambda: len(t.page.resolution.solutions) == 2)
        await t.click("#solve-ten")
        await t.until(lambda: t.page.history)
        assert t.label("solve-one") == "Solve" and not t.enabled("stop")
        assert [line for line in t.text("solutions").splitlines() if "X =" in line] == [
            "    X = 1",
            "    X = 2",
            "    X = 3",
        ]


async def test_solve_10_and_next_10():
    async with ide("-t", "n(X) :- between(1, 25, X).") as t:
        await t.solve("n(X)", key="f6")
        assert len(t.page.resolution.solutions) == 10 and t.label("solve-ten") == "Next 10"
        await t.pilot.press("f6")
        await t.until(lambda: len(t.page.resolution.solutions) == 20)
        await t.click("#solve-ten")
        await t.until(lambda: t.page.history)
        assert len(t.page.history[-1].solutions) == 25


async def test_solve_100_and_next_100():
    async with ide("-t", "n(X) :- between(1, 150, X).") as t:
        await t.type_query("n(X)")
        await t.click("#solve-hundred")
        await t.until(lambda: t.page.resolution.can_continue)
        assert len(t.page.resolution.solutions) == 100 and t.label("solve-hundred") == "Next 100"
        await t.pilot.press("f7")
        await t.until(lambda: t.page.history)
        assert len(t.page.history[-1].solutions) == 150


async def test_failures_and_errors_are_shown():
    async with ide() as t:
        await t.solve("1 > 2")
        assert "no." in t.text("solutions")
        await t.solve("X is foo + 1")
        assert "halt:" in t.text("solutions")


async def test_history_keeps_every_query():
    async with ide("-t", "a. b.") as t:
        await t.solve("a")
        await t.solve("b")
        await t.pilot.press("f6")  # exhausts b
        await t.until(lambda: t.page.history[-1].query == "b")
        text = t.text("solutions")
        assert text.index("?- a") < text.index("?- b")
        assert [h.query for h in t.page.history] == ["a", "b"]


@pytest.mark.parametrize("how", ["button", "key"])
async def test_stop_a_resolution_awaiting_continuation(how):
    async with ide("-q", "repeat", "-s") as t:
        await t.until(lambda: t.page.resolution.can_continue and t.enabled("stop"))
        if how == "button":
            await t.click("#stop")
        else:
            await t.pilot.press("f8")
        await t.until(lambda: t.page.history)
        assert t.page.history[-1].status == "CANCELLED"
        assert "... stopped" in t.text("solutions") and not t.enabled("stop")
        assert t.label("solve-one") == "Solve"


async def test_stop_a_running_resolution():
    # 2P-Kt checks for cancellation between solutions: a resolution yielding none stops when
    # its computation ends (here, timing out), still reported as cancelled
    # solved once the IDE is ready, so that the timeout does not run out while it starts (e.g.
    # under coverage, on a slow runner)
    async with ide("--timeout", "20", "-t", "loop :- loop.", "-q", "loop") as t:
        await t.pilot.press("f5")
        # as in test_late_results_stay_on_their_page: on busy runners (e.g. Windows ones), the IDE
        # may render the resolution only once concluded, leaving nothing to stop
        await t.until(lambda: t.enabled("stop") or t.page.history, timeout=60)
        if t.page.history:
            assert t.page.history[-1].status == "COMPLETED" and not t.enabled("stop")
            return
        assert not t.enabled("solve-one") and "... running" in t.text("solutions")
        await t.pilot.press("f8")
        await t.until(lambda: t.page.history, timeout=60)
        assert t.page.history[-1].status == "CANCELLED"


@pytest.mark.parametrize("how", ["button", "key"])
async def test_reset_discards_asserted_clauses(how):
    async with ide("--flag", "unknown=fail") as t:
        await t.solve("assertz(fact(1))")
        await t.solve("fact(X)")
        assert "X = 1" in t.text("solutions")
        if how == "button":
            await t.click("#reset")
        else:
            await t.pilot.press("f9")
        await t.until(lambda: t.page.resolution.status == "IDLE" or not t.page.history)
        await t.solve("fact(X)")
        assert t.page.history[-1].solutions[0].kind == "no"


# --- panels -----------------------------------------------------------------------------------


async def test_stdin_panel_feeds_the_solver():
    async with ide() as t:
        stdin = t.app.query_one("#stdin", TextArea)
        await t.click("#--content-tab-panel-stdin")
        stdin.focus()
        stdin.insert("hello.")
        await t.settle()
        await t.solve("read(X)")
        assert "X = hello" in t.text("solutions")


async def test_stdout_panel_and_its_unread_marker():
    async with ide() as t:
        await t.solve("write(hi), nl")
        await t.until(lambda: t.text("stdout") == "hi\n")
        assert t.panel_label("stdout").endswith("●")
        await t.click("#--content-tab-panel-stdout")
        await t.until(lambda: not t.panel_label("stdout").endswith("●"))
        assert "STDOUT" not in t.page.unread


async def test_stderr_panel():
    async with ide() as t:
        await t.solve("write(stderr, oops)")
        await t.until(lambda: t.text("stderr") == "oops")
        await t.click("#--content-tab-panel-stderr")
        await t.until(lambda: not t.panel_label("stderr").endswith("●"))


async def test_warnings_panel():
    async with ide() as t:
        await t.solve("undefined_predicate")
        await t.until(lambda: "undefined_predicate" in t.text("warnings"))
        await t.click("#--content-tab-panel-warnings")
        await t.until(lambda: not t.panel_label("warnings").endswith("●"))


async def test_diagnostics_panel():
    async with ide() as t:
        await t.write_theory("p(1). p(")
        await t.until(lambda: t.diagnostics()[0].startswith("ERROR 1:"))
        await t.click("#--content-tab-panel-diagnostics")
        await t.until(lambda: not t.panel_label("diagnostics").endswith("●"))
        t.app.query_one("#diagnostics", OptionList).focus()
        await t.pilot.press("down", "enter")
        source = t.app.query_one("#source", TextArea)
        await t.until(lambda: source.has_focus and source.cursor_location[1] > 0)
        await t.write_theory("p(1).")
        await t.until(lambda: t.diagnostics() == [])


async def test_inspection_panels():
    async with ide() as t:
        await t.write_theory("p(1).")
        await t.solve("assertz(q(2))")
        await t.until(lambda: "q(2)" in t.text("dynamic_kb"))
        assert "p(1)" in t.text("static_kb")
        operators = t.app.query_one("#operators", DataTable)
        assert [700, "XFX", "="] in [operators.get_row_at(i) for i in range(operators.row_count)]
        libraries = t.app.query_one("#libraries", Tree).root.children
        assert "prolog.lang" in [str(library.label) for library in libraries]


async def test_flags_panel_changes_flags():
    async with ide() as t:
        await t.solve("true")
        flags = t.app.query_one("#flags", DataTable)
        await t.until(lambda: flags.row_count > 0)
        await t.click("#--content-tab-panel-flags")
        flags.focus()
        row = next(i for i in range(flags.row_count) if flags.get_row_at(i)[0] == "unknown")
        flags.move_cursor(row=row)
        await t.pilot.press("enter")
        await t.until(
            lambda: isinstance(t.app.screen, PromptScreen) and isinstance(t.app.focused, Input)
        )
        t.app.screen.query_one(Input).value = "fail"
        await t.pilot.press("enter")
        await t.solve("current_flag(unknown, X)")
        assert "X = fail" in t.text("solutions")


async def test_clear_solutions_and_solve_all():
    async with ide() as t:
        await t.write_theory("p(1). p(2). p(3).")
        await t.solve("p(X)", key="f5")
        await t.click("#solve-all")
        await t.until(lambda: t.page.history and t.page.history[-1].status == "COMPLETED")
        assert "X = 3" in t.text("solutions")
        await t.click("#clear-solutions")
        await t.until(lambda: t.text("solutions") == "")


# --- pages ------------------------------------------------------------------------------------


async def test_pages_are_independent_and_selectable():
    async with ide("-t", "first.") as t:
        first = t.page.id
        await t.type_query("first")
        await t.pilot.press("ctrl+t")
        await t.until(lambda: len(t.pages) == 2 and t.page.id != first)
        assert t.text("source") == "" and t.query.value == ""
        await t.write_theory("second.")
        await t.solve("second")
        await t.click(f"#tab-{first}")
        await t.until(lambda: t.page.id == first)
        assert t.text("source") == "first." and t.query.value == "first"
        assert t.text("solutions") == ""


async def test_late_results_stay_on_their_page():
    # the resolution of the first page concludes (timing out) while the second one is shown
    async with ide("--timeout", "10", "-t", "loop :- loop.", "-q", "loop", "-s") as t:
        first = t.page.id
        # on busy runners, the IDE may render the resolution only once concluded
        await t.until(lambda: t.enabled("stop") or t.page.history)
        await t.pilot.press("ctrl+t")
        await t.until(lambda: t.page.id != first)
        await t.until(lambda: t.app.snapshot.page(first).history)
        assert t.text("solutions") == ""
        await t.click(f"#tab-{first}")
        await t.until(lambda: "timeout:" in t.text("solutions"))


async def test_close_a_clean_page():
    async with ide() as t:
        await t.pilot.press("ctrl+t")
        await t.until(lambda: len(t.pages) == 2)
        await t.pilot.press("ctrl+w")
        await t.until(lambda: len(t.pages) == 1)
        assert len(t.tab_labels()) == 1


# --- files ------------------------------------------------------------------------------------


async def new_dirty_file(t: Ide, text: str = "fact.") -> None:
    await t.pilot.press("ctrl+n")
    await t.until(lambda: t.page.document_id is not None)
    await t.write_theory(text)
    await t.until(lambda: t.page.dirty and t.tab_labels()[-1].endswith("*"))


async def test_new_file_is_saved_where_asked(tmp_path):
    async with ide() as t:
        await new_dirty_file(t, "p(è).")
        await t.pilot.press("ctrl+s")
        await t.answer_path(tmp_path / "new.pl")
        await t.until(lambda: not t.page.dirty)
        assert (tmp_path / "new.pl").read_text(encoding="utf-8") == "p(è)."
        assert t.page.title == "new.pl" and not t.tab_labels()[-1].endswith("*")


async def test_saving_can_be_cancelled():
    async with ide() as t:
        await new_dirty_file(t)
        await t.pilot.press("ctrl+s")
        await t.until(lambda: isinstance(t.app.screen, PathScreen))
        await t.pilot.press("escape")
        await t.until(lambda: not isinstance(t.app.screen, PathScreen))
        assert t.page.dirty


async def test_save_failures_are_reported(tmp_path):
    async with ide() as t:
        await new_dirty_file(t)
        await t.pilot.press("ctrl+s")
        await t.answer_path(tmp_path)  # a directory
        await t.until(lambda: any("Cannot save" in n for n in t.notifications()))
        assert t.page.dirty


async def test_open_save_and_save_as(tmp_path):
    file = tmp_path / "theory.pl"
    file.write_text("a.", encoding="utf-8")
    async with ide() as t:
        await t.pilot.press("ctrl+o")
        await t.answer_path(file)
        await t.until(lambda: len(t.pages) == 2 and t.page.title == "theory.pl")
        assert t.text("source") == "a."
        await t.write_theory("a. b.")
        await t.pilot.press("ctrl+s")  # saved where it came from, without asking
        await t.until(lambda: not t.page.dirty)
        assert file.read_text(encoding="utf-8") == "a. b."
        await t.pilot.press("ctrl+e")
        await t.answer_path(tmp_path / "copy.pl")
        await t.until(lambda: (tmp_path / "copy.pl").exists())
        assert (tmp_path / "copy.pl").read_text(encoding="utf-8") == "a. b."


async def test_opening_a_missing_file_is_reported(tmp_path):
    async with ide() as t:
        await t.pilot.press("ctrl+o")
        await t.answer_path(tmp_path / "missing.pl")
        await t.until(lambda: any("Cannot open" in n for n in t.notifications()))
        assert len(t.pages) == 1


async def test_scratch_pages_are_not_saved():
    async with ide() as t:
        await t.pilot.press("ctrl+s")
        await t.until(lambda: any("not saved" in n for n in t.notifications()))
        assert not isinstance(t.app.screen, PathScreen)


async def test_reload_a_clean_file(tmp_path):
    file = tmp_path / "theory.pl"
    file.write_text("old.", encoding="utf-8")
    async with ide(str(file)) as t:
        file.write_text("new.", encoding="utf-8")
        await t.pilot.press("ctrl+r")
        await t.until(lambda: t.text("source") == "new.")


@pytest.mark.parametrize(
    "choice, expected", [("choice-discard-changes", "disk."), ("choice-cancel", "edited.")]
)
async def test_reload_a_dirty_file(tmp_path, choice, expected):
    file = tmp_path / "theory.pl"
    file.write_text("disk.", encoding="utf-8")
    async with ide(str(file)) as t:
        await t.write_theory("edited.")
        await t.pilot.press("ctrl+r")
        await t.choose(choice)
        await t.until(lambda: t.text("source") == expected and t.page.source == expected)


async def test_reload_failures_are_reported(tmp_path):
    file = tmp_path / "theory.pl"
    file.write_text("a.", encoding="utf-8")
    async with ide(str(file)) as t:
        file.unlink()
        await t.pilot.press("ctrl+r")
        await t.until(lambda: any("Cannot reload" in n for n in t.notifications()))
        assert t.text("source") == "a."


async def test_close_a_dirty_page_saving_it(tmp_path):
    async with ide() as t:
        await new_dirty_file(t, "kept.")
        await t.pilot.press("ctrl+w")
        await t.choose("choice-save")
        await t.answer_path(tmp_path / "kept.pl")
        await t.until(lambda: len(t.pages) == 1)
        assert (tmp_path / "kept.pl").read_text(encoding="utf-8") == "kept."


@pytest.mark.parametrize("choice, pages", [("choice-discard", 1), ("choice-cancel", 2)])
async def test_close_a_dirty_page(choice, pages):
    async with ide() as t:
        await new_dirty_file(t)
        await t.pilot.press("ctrl+w")
        await t.choose(choice)
        await t.until(lambda: len(t.pages) == pages)
        await asyncio.sleep(0.2)
        assert len(t.pages) == pages


# --- quitting ---------------------------------------------------------------------------------


async def test_quit():
    async with ide() as t:
        await t.pilot.press("ctrl+q")
        await t.until_exited()


async def test_quit_with_unsaved_changes():
    async with ide() as t:
        await new_dirty_file(t)
        await t.pilot.press("ctrl+q")
        await t.choose("choice-cancel")
        assert t.app.is_running
        await t.pilot.press("ctrl+q")
        await t.until(lambda: isinstance(t.app.screen, ChoiceScreen))
        await t.click("#choice-quit")
        await t.until_exited()


# --- command line -----------------------------------------------------------------------------


async def test_files_open_a_page_each(tmp_path):
    existing = tmp_path / "a.pl"
    existing.write_text("a.", encoding="utf-8")
    missing = tmp_path / "b.pl"
    async with ide(str(existing), str(missing), pages=2) as t:
        assert [p.title for p in t.pages] == ["a.pl", "b.pl"]
        assert t.page.title == "b.pl" and t.text("source") == ""
        await t.write_theory("b.")
        await t.pilot.press("ctrl+s")  # created where asked on the command line
        await t.until(lambda: missing.exists())
        assert missing.read_text(encoding="utf-8") == "b."


async def test_files_and_theory(tmp_path):
    file = tmp_path / "a.pl"
    file.write_text("a.", encoding="utf-8")
    async with ide(str(file), "-t", "t.", "-q", "a", pages=2) as t:
        assert t.page.document_id is None and t.text("source") == "t."
        await t.until(lambda: all(p.query == "a" for p in t.pages))


@pytest.mark.parametrize("mode, count", [(None, 1), ("one", 1), ("ten", 10), ("hundred", 100)])
async def test_query_and_solve_at_startup(mode, count):
    argv = ["-t", "n(X) :- between(1, 200, X).", "-q", "n(X)", "--solve"]
    async with ide(*argv + ([mode] if mode else [])) as t:
        await t.until(lambda: len(t.page.resolution.solutions) == count)
        assert t.query.value == "n(X)"


async def test_stdin_at_startup(tmp_path):
    async with ide("--stdin", "word.", "-q", "read(X)", "-s") as t:
        await t.until(lambda: "X = word" in t.text("solutions"))
        assert t.text("stdin") == "word."
    file = tmp_path / "input.txt"
    file.write_text("other.", encoding="utf-8")
    async with ide("--stdin-file", str(file), "-q", "read(X)", "-s") as t:
        await t.until(lambda: "X = other" in t.text("solutions"))


async def test_dynamic_kb(tmp_path):
    first, second = tmp_path / "a.pl", tmp_path / "b.pl"
    first.write_text("d(1).", encoding="utf-8")
    second.write_text("d(2).", encoding="utf-8")
    async with ide("-d", str(first), "--dynamic-kb", str(second), "-q", "d(X)", "-s", "ten") as t:
        await t.until(lambda: t.page.history)
        assert [s.bindings for s in t.page.history[-1].solutions] == [
            (("X", "1"),),
            (("X", "2"),),
        ]
        await t.solve("retract(d(1))")
        await t.pilot.press("f9")  # reset: the dynamic KB is loaded again
        await t.solve("d(X)", key="f6")
        assert len(t.page.history[-1].solutions) == 2


async def test_flags():
    async with ide("-f", "unknown=fail", "-q", "undefined", "-s") as t:
        assert await t.outcome() == "no" and t.text("warnings") == ""
    async with ide("--flag", "unknown=error", "-q", "undefined", "-s") as t:
        assert await t.outcome() == "halt"


async def test_timeout():
    async with ide("--timeout", "0.5", "-t", "loop :- loop.", "-q", "loop", "-s") as t:
        await t.until(lambda: "timeout:" in t.text("solutions"))


async def test_default_libraries_and_no_default_libraries():
    async with ide("-q", "X := hello.upper", "-s") as t:
        await t.until(lambda: "X = 'HELLO'" in t.text("solutions"))
    async with ide("--no-default-libraries", "-q", "X := hello.upper", "-s") as t:
        assert await t.outcome() != "yes"  # no := operator, nor its predicate


async def test_named_and_custom_libraries():
    spec = f"{RESOURCES / 'custom_library.py'}:greetings"
    argv = ["--no-default-libraries", "-l", "io", "-l", spec, "-q", "greeting(X)", "-s", "ten"]
    async with ide(*argv) as t:
        await t.until(lambda: t.page.history)
        assert "X = ciao" in t.text("solutions")
        await t.solve("write(stderr, e)")
        await t.until(lambda: t.text("stderr") == "e")


async def test_jvm_oop_library():
    argv = [
        "--no-default-libraries",
        "-l",
        "oop-jvm",
        "--timeout",
        "30",
        "-q",
        "X := $math.abs(-3)",
    ]
    async with ide(*argv, "-s") as t:
        await t.outcome()
        assert "X = 3" in t.text("solutions"), t.text("solutions")


async def test_oop_library_options():
    async with ide("-q", "X := $sys.maxsize", "-s") as t:
        assert await t.outcome() != "yes"
    async with ide("--oop-allow-all-imports", "-q", "X := $sys.maxsize", "-s") as t:
        assert await t.outcome() == "yes"


async def test_no_builtins():
    async with ide("-f", "unknown=fail", "-q", "member(X, [1])", "-s") as t:
        assert await t.outcome() == "yes"
    async with ide("--no-builtins", "-f", "unknown=fail", "-q", "member(X, [1])", "-s") as t:
        assert await t.outcome() == "no"


async def test_unificator():
    async with ide("-q", "1 = 1.0", "-s") as t:
        assert await t.outcome() == "no"
    async with ide("--unificator", "tuprolog.unify:naive_unificator", "-q", "1 = 1.0", "-s") as t:
        assert await t.outcome() == "yes"


async def test_problog_dialect():
    argv = ["--dialect", "problog", "-t", "0.3::rain. wet :- rain.", "-q", "wet", "-s"]
    async with ide(*argv) as t:
        await t.until(lambda: "(probability: 0.3)" in t.text("solutions"))


@pytest.mark.parametrize("scheduling", ["single", "concurrent"])
async def test_scheduling(scheduling):
    async with ide("--scheduling", scheduling, "-q", "repeat", "-s") as t:
        first = t.page.id
        await t.until(lambda: t.page.resolution.can_continue)
        await t.pilot.press("ctrl+t")
        await t.until(lambda: t.page.id != first)
        await t.solve("true")
        if scheduling == "concurrent":  # the first page still awaits continuation
            other = t.app.snapshot.page(first)
            assert other.resolution.can_continue and not other.history
        else:  # starting a resolution stopped the first page's
            await t.until(lambda: t.app.snapshot.page(first).history)
            history = t.app.snapshot.page(first).history
            assert [(h.query, h.status) for h in history] == [("repeat", "CANCELLED")]


async def test_timeout_field_sets_the_timeout():
    async with ide("-t", "loop :- loop.") as t:
        timeout = t.app.query_one("#timeout", Input)
        await t.until(lambda: timeout.value == "1m")  # the command line's
        timeout.focus()
        timeout.value = "1s"
        await t.pilot.press("enter")
        await t.until(lambda: t.page.timeout == "1s")
        await t.solve("loop")
        assert "timeout:" in t.text("solutions")


async def test_operators_are_added_and_highlighted():
    async with ide("-t", "p.") as t:
        await t.click("#--content-tab-panel-operators")
        await t.click("#add-operator")
        await t.until(
            lambda: isinstance(t.app.screen, PromptScreen) and isinstance(t.app.focused, Input)
        )
        t.app.screen.query_one(Input).value = "700 xfx ==="
        await t.pilot.press("enter")
        await t.settle()
        assert t.page.source == "p.\n:- op(700, xfx, ===).\n"
        await t.solve("X = (a === b)")
        assert "X = a === b" in t.text("solutions")
        operators = t.app.query_one("#operators", DataTable)
        await t.until(
            lambda: (
                [700, "XFX", "==="] in [operators.get_row_at(i) for i in range(operators.row_count)]
            )
        )
        source = t.app.query_one("#source", TextArea)
        assert "number" in {name for _, _, name in source._highlights[1]}


async def test_libraries_and_flags_are_documented():
    async with ide() as t:
        await t.solve("true")
        tree = t.app.query_one("#libraries", Tree)
        await t.until(lambda: tree.root.children)
        await t.click("#--content-tab-panel-libraries")
        tree.focus()
        await t.pilot.press("down")
        await t.until(lambda: str(t.app.query_one("#libraries-preview").render()) != "")
        await t.pilot.press("f1")
        await t.until(lambda: isinstance(t.app.screen, DocumentationScreen))
        assert "library" in t.app.screen.query_one("#documentation", Markdown).source
        await t.pilot.press("escape")
        await t.click("#--content-tab-panel-flags")
        await t.until(lambda: str(t.app.query_one("#flags-preview").render()) != "")
        await t.click("#flags-documentation")
        await t.until(lambda: isinstance(t.app.screen, DocumentationScreen))
        assert "flag(" in t.app.screen.query_one("#documentation", Markdown).source
