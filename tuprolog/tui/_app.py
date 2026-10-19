"""The Textual application of the terminal IDE."""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

from rich.highlighter import Highlighter
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    OptionList,
    Static,
    Tab,
    TabbedContent,
    TabPane,
    Tabs,
    TextArea,
    Tree,
)
from textual.widgets.text_area import TextAreaTheme

from . import _model as m
from ._bridge import GuiBridge, JvmGuiBridge
from ._screens import (
    ARROW_BINDINGS,
    ChoiceScreen,
    DocumentationScreen,
    PathScreen,
    PromptScreen,
)

__all__ = ["PrologTui"]

# as 2P-Kt's Swing IDE: panels, labels, and the ids of their widgets
_LOWER_PANELS: tuple[tuple[m.Panel, str], ...] = (
    ("SOLUTIONS", "Solutions"),
    ("STDIN", "Stdin"),
    ("STDOUT", "Stdout"),
    ("STDERR", "Stderr"),
    ("WARNINGS", "Warnings"),
    ("DIAGNOSTICS", "Diagnostics"),
    ("OPERATORS", "Operators"),
    ("FLAGS", "Flags"),
    ("LIBRARIES", "Libraries"),
    ("STATIC_KB", "Static KB"),
    ("DYNAMIC_KB", "Dynamic KB"),
)
_MODES: tuple[tuple[m.Mode, str, str], ...] = (
    ("ONE", "solve-one", ""),
    ("TEN", "solve-ten", " 10"),
    ("HUNDRED", "solve-hundred", " 100"),
    ("ALL", "solve-all", " all"),
)


# the highlight names of the categories of tokens (as those of Textual's themes): atoms stay plain
_HIGHLIGHTS: dict[str, str] = {
    "COMMENT": "comment",
    "OPERATOR": "operator",
    "PARENTHESIS": "punctuation.bracket",
    "BRACE": "punctuation.bracket",
    "BRACKET": "punctuation.bracket",
    "FULL_STOP": "punctuation.delimiter",
    "FUNCTOR": "function",
    "VARIABLE": "type",  # no theme styles variables: types are as distinct
    "NUMBER": "number",
    "STRING": "string",
    "DIRECTIVE": "keyword",
    "ERROR": "exception",
}
_SPECIFIERS = ("xfx", "xfy", "yfx", "fy", "fx", "xf", "yf")

Tokenizer = Callable[[str], tuple[m.SyntaxToken, ...]]


class PrologTextArea(TextArea):
    """A `TextArea` highlighting Prolog text, with the tokens `tokenizer` finds in it."""

    tokenizer: Tokenizer | None = None

    @classmethod
    def editor(cls, tokenizer: Tokenizer, **kwargs: object) -> PrologTextArea:
        """A code editor (see `TextArea.code_editor`) highlighting with `tokenizer`."""
        area = cls.code_editor("", language=None, **kwargs)  # type: ignore[arg-type]
        assert isinstance(area, PrologTextArea)
        area.tokenizer = tokenizer
        return area

    def rehighlight(self) -> None:
        """Highlights the text again (e.g. as the operators the tokenizer knows changed)."""
        self._build_highlight_map()
        self.refresh()

    def _build_highlight_map(self) -> None:
        # overrides Textual's (private) tree-sitter highlighting, as it has no Prolog grammar
        self._line_cache.clear()
        highlights = self._highlights
        highlights.clear()
        if self.tokenizer is None or not self.text:
            return
        lines = self.document.lines

        def byte(line: int, column: int) -> int:  # Textual highlights UTF-8 byte offsets
            # ponytail: JVM columns count UTF-16 units, off by one per astral character before
            return len(lines[line][:column].encode()) if line < len(lines) else 0

        for token in self.tokenizer(self.text):
            name = _HIGHLIGHTS.get(token.category)
            if name is None:
                continue
            (start_line, start_column), (end_line, end_column) = token.start, token.end
            if start_line == end_line:
                end: int | None = byte(end_line, end_column)
                highlights[start_line].append((byte(start_line, start_column), end, name))
                continue
            highlights[start_line].append((byte(start_line, start_column), None, name))
            for line in range(start_line + 1, end_line):
                highlights[line].append((0, None, name))
            highlights[end_line].append((0, byte(end_line, end_column), name))


class QueryHighlighter(Highlighter):
    """Highlights a query (a line of Prolog text) as the `PrologTextArea` `editor` would."""

    def __init__(self, tokenizer: Tokenizer, editor: Callable[[], TextArea]) -> None:
        self.tokenizer = tokenizer
        self.editor = editor

    def highlight(self, text: Text) -> None:
        theme = TextAreaTheme.get_builtin_theme(self.editor().theme)
        if theme is None or not text.plain:
            return
        for token in self.tokenizer(text.plain):
            style = theme.syntax_styles.get(_HIGHLIGHTS.get(token.category, ""))
            if style is not None and token.start[0] == token.end[0] == 0:
                text.stylize(style, token.start[1], token.end[1])


class StateChanged(Message):
    """A new snapshot of the GUI application's state (posted from any thread)."""

    def __init__(self, snapshot: m.Snapshot) -> None:
        super().__init__()
        self.snapshot = snapshot


class EffectRequested(Message):
    """An effect the GUI application asks for (posted from any thread)."""

    def __init__(self, effect: m.Effect) -> None:
        super().__init__()
        self.effect = effect


class BridgeError(Message):
    """An error of the GUI application (posted from any thread)."""

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message


def _tab_id(page_id: str) -> str:
    return "tab-" + re.sub(r"[^A-Za-z0-9_-]", "_", page_id)


def _format_solution(solution: m.Solution) -> list[str]:
    if solution.kind == "yes":
        lines = [f"yes: {solution.solved_query or solution.query}"]
        lines += [f"    {variable} = {value}" for variable, value in solution.bindings]
        lines += [f"    ({key}: {value})" for key, value in solution.metadata]
        return lines
    if solution.kind == "halt":
        return [f"{'timeout' if solution.is_timeout else 'halt'}: {solution.message}"]
    return ["no."]


def _format_resolution(
    query: str, solutions: tuple[m.Solution, ...], status: str, error: str | None
) -> list[str]:
    lines = [f"?- {query}"]
    for solution in solutions:
        lines += _format_solution(solution)
    if error is not None and not any(s.kind == "halt" for s in solutions):
        lines.append(f"error: {error}")
    if status == "RUNNING":
        lines.append("... running")
    elif status == "AWAITING_CONTINUATION":
        lines.append("... more solutions may follow (Next)")
    elif status == "CANCELLED":
        lines.append("... stopped")
    return lines


def format_solutions(page: m.Page) -> str:
    """The text of the solutions panel: the concluded resolutions, then the current one."""
    lines: list[str] = []
    for entry in page.history:
        lines += _format_resolution(entry.query, entry.solutions, entry.status, entry.error)
        lines.append("")
    resolution = page.resolution
    if resolution.status in ("RUNNING", "AWAITING_CONTINUATION") and resolution.query is not None:
        lines += _format_resolution(
            resolution.query, resolution.solutions, resolution.status, resolution.error
        )
    return "\n".join(lines).rstrip()


class PrologTui(App[None]):
    """A terminal IDE for Prolog: pages of theories to edit and queries to solve against them.

    It renders the state of 2P-Kt's GUI application, sends it actions, and fulfils its effects
    (file dialogs, reading and writing files, confirmations, clipboard), through a bridge.

    Args:
        bridge: The bridge to the GUI application; by default, a `JvmGuiBridge` running 2P-Kt's.
        startup: What to open at startup; by default, a scratch page.
    """

    TITLE = "2ppy TUI"
    CSS_PATH = "tui.tcss"
    # priority: the editors bind some of these keys too (e.g. F6, ctrl+w, ctrl+e)
    BINDINGS: ClassVar[list[BindingType]] = [
        *ARROW_BINDINGS,
        Binding("ctrl+q", "request_exit", "Quit", priority=True),
        Binding("f5", "solve('ONE')", "Solve", priority=True),
        Binding("f6", "solve('TEN')", "Solve 10", priority=True),
        Binding("f7", "solve('HUNDRED')", "Solve 100", priority=True),
        Binding("f8", "stop", "Stop", priority=True),
        Binding("f9", "reset", "Reset", priority=True),
        Binding("ctrl+t", "new_scratch_page", "New scratch", priority=True),
        Binding("ctrl+n", "new_document_page", "New file", priority=True),
        Binding("ctrl+o", "open_document", "Open", priority=True),
        Binding("ctrl+s", "save", "Save", priority=True),
        Binding("ctrl+e", "save_as", "Save as", show=False, priority=True),
        Binding("ctrl+r", "reload", "Reload", show=False, priority=True),
        Binding("ctrl+w", "close_page", "Close page", priority=True),
        Binding("f1", "documentation", "Docs", show=False),
    ]

    def __init__(self, bridge: GuiBridge | None = None, startup: m.Startup | None = None) -> None:
        super().__init__()
        self.bridge: GuiBridge = JvmGuiBridge() if bridge is None else bridge
        self.startup: m.Startup | None = m.Startup() if startup is None else startup
        self.snapshot = m.Snapshot()
        self._rendered_page_id: str | None = None
        self._tab_pages: dict[str, str] = {}  # tab id -> page id
        self._pending_selection: str | None = None
        # the model values last shown by (or acknowledging) the editable widgets: a widget whose
        # value differs holds local input the model has not acknowledged yet
        self._loaded: dict[str, str] = {"source": "", "query": "", "stdin": ""}
        self._inspected: dict[str, object] = {}  # panel widget id -> the data it shows
        self._marking: set[tuple[str, m.Panel]] = set()
        self._closed = False

    # --- layout ----------------------------------------------------------------------------------

    def compose(self) -> ComposeResult:
        yield Header()
        yield Tabs(id="pages")
        source = PrologTextArea.editor(self._tokens, id="source")
        yield source
        with Horizontal(id="controls"):
            yield Label("?-", id="prompt")
            yield Input(
                placeholder="Query, e.g. member(X, [1, 2])",
                id="query",
                highlighter=QueryHighlighter(self._tokens, lambda: source),
            )
            for _, button_id, suffix in _MODES:
                yield Button(f"Solve{suffix}", id=button_id, variant="primary")
            yield Button("Stop", id="stop", variant="error", disabled=True)
            yield Button("Reset", id="reset")
            yield Label("Timeout", id="timeout-label")
            yield Input(placeholder="e.g. 5s", id="timeout")
        with TabbedContent(id="panels"):
            for panel, label in _LOWER_PANELS:
                with TabPane(label, id=f"panel-{panel.lower()}"):
                    yield from self._compose_panel(panel)
        yield Footer()

    def _compose_panel(self, panel: m.Panel) -> ComposeResult:
        widget_id = panel.lower()
        match panel:
            case "SOLUTIONS":
                yield Button("Clear solutions", id="clear-solutions")
                yield TextArea("", read_only=True, id=widget_id)
            case "DIAGNOSTICS":
                yield OptionList(id=widget_id)
            case "OPERATORS":
                yield Button("Add operator", id="add-operator")
                yield DataTable(id=widget_id, cursor_type="row", zebra_stripes=True)
            case "FLAGS":
                yield DataTable(id=widget_id, cursor_type="row", zebra_stripes=True)
                yield from self._compose_documentation_bar(widget_id)
            case "LIBRARIES":
                tree: Tree[tuple[str, str] | None] = Tree("Libraries", id=widget_id)
                tree.show_root = False
                yield tree
                yield from self._compose_documentation_bar(widget_id)
            case "STATIC_KB" | "DYNAMIC_KB":
                yield PrologTextArea.editor(self._tokens, id=widget_id, read_only=True)
            case _:
                yield TextArea(
                    "", read_only=panel != "STDIN", id=widget_id, show_line_numbers=False
                )

    def _compose_documentation_bar(self, widget_id: str) -> ComposeResult:
        with Horizontal(classes="documentation-bar"):
            yield Static("", id=f"{widget_id}-preview", markup=False)
            yield Button("Documentation (F1)", id=f"{widget_id}-documentation")

    # --- lifecycle -------------------------------------------------------------------------------

    def on_mount(self) -> None:
        self.query_one("#operators", DataTable).add_columns("Priority", "Specifier", "Name")
        self.query_one("#flags", DataTable).add_columns("Name", "Value")
        self.bridge.start(
            on_state=lambda snapshot: self.post_message(StateChanged(snapshot)),
            on_effect=lambda effect: self.post_message(EffectRequested(effect)),
            on_error=lambda message: self.post_message(BridgeError(message)),
        )
        startup = self.startup or m.Startup()
        for path, text in startup.documents:
            self.dispatch(m.OpenDocumentLoaded(path, text))
        if startup.page_count > len(startup.documents):
            self.dispatch(m.NewScratchPage(text=startup.theory or ""))

    def on_unmount(self) -> None:
        self._close_bridge()

    def _close_bridge(self) -> None:
        if not self._closed:
            self._closed = True
            self.bridge.close()

    def dispatch(self, action: m.Action) -> None:
        """Sends an action to the GUI application."""
        if not self._closed:
            self.bridge.dispatch(action)

    def _tokens(self, text: str) -> tuple[m.SyntaxToken, ...]:
        page = self.page
        return self.bridge.analyze(text, () if page is None else page.inspection.operators)

    # --- rendering -------------------------------------------------------------------------------

    @on(StateChanged)
    async def render_state(self, message: StateChanged) -> None:
        """Renders a new snapshot (on Textual's event loop)."""
        snapshot = message.snapshot
        self._complete_startup(snapshot)
        await self._render_tabs(snapshot)
        # published once the tabs are, and with the rest rendered synchronously: whoever reads it
        # (e.g. the handlers of user input) finds the widgets showing it
        self.snapshot = snapshot
        page = snapshot.selected_page
        if page is None:
            self._rendered_page_id = None
            return
        if page.id != self._rendered_page_id:
            self._rendered_page_id = page.id
            self._render_inputs(page, force=True)
        else:
            self._render_inputs(page, force=False)
        self._render_controls(page)
        self._render_panels(page)

    def _complete_startup(self, snapshot: m.Snapshot) -> None:
        startup = self.startup
        if startup is None or len(snapshot.pages) < startup.page_count:
            return
        self.startup = None
        for page in snapshot.pages:
            if startup.query is not None:
                self.dispatch(m.ChangeQuery(page.id, startup.query))
            if startup.stdin is not None:
                self.dispatch(m.ChangeStdin(page.id, startup.stdin))
        if startup.solve is not None and snapshot.selected_page_id is not None:
            self.dispatch(m.Solve(snapshot.selected_page_id, startup.solve))

    async def _render_tabs(self, snapshot: m.Snapshot) -> None:
        tabs = self.query_one("#pages", Tabs)
        wanted = {_tab_id(p.id): p for p in snapshot.pages}
        for tab_id in list(self._tab_pages):
            if tab_id not in wanted:
                await tabs.remove_tab(tab_id)
                del self._tab_pages[tab_id]
        for tab_id, page in wanted.items():
            label = page.title + (" *" if page.dirty else "")
            if tab_id in self._tab_pages:
                tab = tabs.query_one(f"#{tab_id}", Tab)
                if str(tab.label) != label:
                    tab.label = label
            else:
                self._tab_pages[tab_id] = page.id
                # awaited: activating a tab not mounted yet would activate another one
                await tabs.add_tab(Tab(label, id=tab_id))
        if self._pending_selection == snapshot.selected_page_id:
            self._pending_selection = None
        if self._pending_selection is None and snapshot.selected_page_id is not None:
            tabs.active = _tab_id(snapshot.selected_page_id)

    def _widget_value(self, key: str) -> str:
        if key == "query":
            return self.query_one("#query", Input).value
        return self.query_one(f"#{key}", TextArea).text

    def _load(self, key: str, value: str, force: bool) -> None:
        local = self._widget_value(key)
        if not force and local != self._loaded[key]:
            # local input not acknowledged yet (possibly with its change event still queued):
            # older states must not overwrite it
            if value == local:
                self._loaded[key] = value
            return
        self._loaded[key] = value
        if local == value:
            return
        if key == "query":
            query = self.query_one("#query", Input)
            with query.prevent(Input.Changed):
                query.value = value
        else:
            area = self.query_one(f"#{key}", TextArea)
            with area.prevent(TextArea.Changed):
                area.load_text(value)

    def _render_inputs(self, page: m.Page, force: bool) -> None:
        self._load("source", page.source, force)
        self._load("query", page.query, force)
        self._load("stdin", page.stdin, force)

    def _render_controls(self, page: m.Page) -> None:
        resolution = page.resolution
        verb = "Next" if resolution.can_continue else "Solve"
        for _, button_id, suffix in _MODES:
            button = self.query_one(f"#{button_id}", Button)
            button.label = verb + suffix
            button.disabled = not (resolution.can_solve or resolution.can_continue)
        self.query_one("#stop", Button).disabled = not resolution.can_stop
        timeout = self.query_one("#timeout", Input)
        # as 2P-Kt's Swing IDE: the timeout is not changed while solving, nor overwritten while edited
        timeout.disabled = resolution.status == "RUNNING"
        if not timeout.has_focus and timeout.value != page.timeout:
            timeout.value = page.timeout

    def _render_panels(self, page: m.Page) -> None:
        self._set_text("solutions", format_solutions(page))
        self.query_one("#clear-solutions", Button).disabled = not page.history
        self._set_text("stdout", page.stdout)
        self._set_text("stderr", page.stderr)
        self._set_text("warnings", "\n".join(page.warnings))
        if self._changed_data("diagnostics", page.diagnostics):
            diagnostics = self.query_one("#diagnostics", OptionList)
            diagnostics.clear_options()
            diagnostics.add_options(d.message for d in page.diagnostics)
        inspection = page.inspection
        if self._changed_data("operators", inspection.operators):
            operators = self.query_one("#operators", DataTable)
            operators.clear()
            operators.add_rows(inspection.operators)
            for area in self.query(PrologTextArea):
                area.rehighlight()
            self.query_one("#query", Input).refresh()
        if self._changed_data("flags", inspection.flags):
            flags = self.query_one("#flags", DataTable)
            flags.clear()
            for name, value, _ in inspection.flags:
                flags.add_row(name, value, key=name)
        # as 2P-Kt's Swing IDE: flags are not changed while solving
        self.query_one("#flags", DataTable).disabled = page.resolution.status == "RUNNING"
        if self._changed_data("libraries", inspection.libraries):
            self._render_libraries(inspection.libraries)
        self._set_text("static_kb", inspection.static_kb, scroll=False)
        self._set_text("dynamic_kb", inspection.dynamic_kb, scroll=False)
        panels = self.query_one("#panels", TabbedContent)
        for panel, label in _LOWER_PANELS:
            pane_id = f"panel-{panel.lower()}"
            panels.get_tab(pane_id).label = label + (" ●" if panel in page.unread else "")
        visible: set[m.Panel] = set()
        if panels.active:
            visible.add(panels.active.removeprefix("panel-").upper())  # type: ignore[arg-type]
        self._marking = {(p, panel) for p, panel in self._marking if p == page.id}
        for panel in page.unread & visible:
            self._mark_read(page.id, panel)
        self._marking -= {(page.id, panel) for panel in m.PANELS if panel not in page.unread}

    def _mark_read(self, page_id: str, panel: m.Panel) -> None:
        if (page_id, panel) not in self._marking:
            self._marking.add((page_id, panel))
            self.dispatch(m.MarkPanelRead(page_id, panel))

    def _changed_data(self, widget_id: str, data: object) -> bool:
        if self._inspected.get(widget_id) == data:
            return False
        self._inspected[widget_id] = data
        return True

    def _render_libraries(self, libraries: tuple[m.LibraryEntry, ...]) -> None:
        tree: Tree[tuple[str, str] | None] = self.query_one("#libraries", Tree)
        tree.clear()
        for library in libraries:
            # nodes hold what they document, and its documentation
            node = tree.root.add(library.alias, data=(library.alias, library.help))
            documentation = dict(library.documentation)
            for kind, names in (
                ("Predicates", library.predicates),
                ("Operators", library.operators),
                ("Functions", library.functions),
            ):
                if names:
                    group = node.add(f"{kind} ({len(names)})")
                    for name in names:
                        doc = documentation.get(name)
                        group.add_leaf(name, data=None if doc is None else (name, doc))

    def _set_text(self, widget_id: str, text: str, scroll: bool = True) -> None:
        area = self.query_one(f"#{widget_id}", TextArea)
        if area.text != text:
            area.load_text(text)
            if scroll:
                area.scroll_end(animate=False)

    # --- user input ------------------------------------------------------------------------------

    @property
    def page(self) -> m.Page | None:
        """The page shown in the widgets, if any."""
        return self.snapshot.page(self._rendered_page_id)

    def _changed(self, key: str, value: str) -> m.Page | None:
        page = self.page
        if page is None or value != self._widget_value(key):
            return None  # outdated, e.g. queued before another page was selected
        return page

    @on(TextArea.Changed, "#source")
    def source_changed(self, event: TextArea.Changed) -> None:
        """Sends the edited theory to the model."""
        page = self._changed("source", event.text_area.text)
        if page is None:
            return
        text = event.text_area.text
        if page.document_id is None:
            self.dispatch(m.ChangeScratchText(page.id, text))
        else:
            self.dispatch(m.ChangeDocumentText(page.document_id, text))

    @on(Input.Changed, "#query")
    def query_changed(self, event: Input.Changed) -> None:
        """Sends the edited query to the model."""
        page = self._changed("query", event.value)
        if page is not None:
            self.dispatch(m.ChangeQuery(page.id, event.value))

    @on(Input.Submitted, "#query")
    def query_submitted(self) -> None:
        """Solves (or continues) the query."""
        self.action_solve("ONE")

    @on(TextArea.Changed, "#stdin")
    def stdin_changed(self, event: TextArea.Changed) -> None:
        """Sends the edited standard input to the model."""
        page = self._changed("stdin", event.text_area.text)
        if page is not None:
            self.dispatch(m.ChangeStdin(page.id, event.text_area.text))

    @on(Tabs.TabActivated, "#pages")
    def page_activated(self, event: Tabs.TabActivated) -> None:
        """Selects the page of the activated tab."""
        if event.tab.id != event.tabs.active:
            return  # outdated, e.g. the automatic activation of the first tab added
        page_id = self._tab_pages.get(event.tab.id or "")
        if page_id is not None and page_id != self.snapshot.selected_page_id:
            self._pending_selection = page_id
            self.dispatch(m.SelectPage(page_id))

    @on(TabbedContent.TabActivated, "#panels")
    def panel_activated(self, event: TabbedContent.TabActivated) -> None:
        """Marks the activated panel as read."""
        page = self.page
        panel = (event.pane.id or "").removeprefix("panel-").upper()
        if page is not None and panel in page.unread:
            self._mark_read(page.id, panel)  # type: ignore[arg-type]

    @on(OptionList.OptionSelected, "#diagnostics")
    def diagnostic_selected(self, event: OptionList.OptionSelected) -> None:
        """Moves the cursor of the editor where the selected diagnostic is."""
        page = self.page
        if page is None or event.option_index >= len(page.diagnostics):
            return
        diagnostic = page.diagnostics[event.option_index]
        if diagnostic.line is not None:
            editor = self.query_one("#source", TextArea)
            editor.move_cursor((diagnostic.line, diagnostic.column or 0), center=True)
            editor.focus()

    @on(DataTable.RowSelected, "#flags")
    def flag_selected(self, event: DataTable.RowSelected) -> None:
        """Asks for a new value of the selected flag."""
        page = self.page
        name = event.row_key.value
        if page is None or name is None:
            return
        value = str(event.data_table.get_row(event.row_key)[1])

        def change(new_value: str | None) -> None:
            if new_value is not None and new_value != value:
                self.dispatch(m.ChangeFlag(page.id, name, new_value))

        self.push_screen(PromptScreen(f"Value of the flag {name}", value), change)

    @on(Input.Submitted, "#timeout")
    @on(Input.Blurred, "#timeout")
    def timeout_changed(self, event: Input.Submitted | Input.Blurred) -> None:
        """Sends the edited timeout to the model, if valid."""
        page = self.page
        text = event.value.strip()
        if page is None or text == page.timeout:
            return
        if self.bridge.is_timeout(text):
            self.dispatch(m.ChangeTimeout(page.id, text))
        else:
            self.notify(
                f"Invalid timeout: {text!r}. Expected none, or amounts of ms, s, m, h, d, w "
                "(e.g. 500ms, 2s 500ms, 1m 30s), up to a week",
                title="Error",
                severity="error",
            )
            event.input.value = page.timeout

    def _documented(self, panel: str) -> tuple[str, str] | None:
        """What the flags or libraries panel highlights, and its documentation, if any."""
        page = self.page
        if page is None:
            return None
        if panel == "flags":
            table = self.query_one("#flags", DataTable)
            if not table.row_count:
                return None
            name = str(table.get_row_at(table.cursor_row)[0])
            help_ = next((h for n, _, h in page.inspection.flags if n == name), "")
            return (name, help_) if help_ else None
        node = self.query_one("#libraries", Tree).cursor_node
        return None if node is None else node.data

    def _preview(self, panel: str) -> None:
        documented = self._documented(panel)
        preview = "" if documented is None else self.bridge.documentation_preview(documented[1])
        self.query_one(f"#{panel}-preview", Static).update(preview)

    @on(DataTable.RowHighlighted, "#flags")
    def flag_highlighted(self) -> None:
        """Previews the documentation of the highlighted flag."""
        self._preview("flags")

    @on(Tree.NodeHighlighted, "#libraries")
    def library_symbol_highlighted(self) -> None:
        """Previews the documentation of the highlighted library, or symbol."""
        self._preview("libraries")

    @on(Tree.NodeSelected, "#libraries")
    def library_symbol_selected(self, event: Tree.NodeSelected) -> None:
        """Shows the documentation of the selected symbol (libraries expand, or collapse)."""
        if event.node.data is not None and not event.node.allow_expand:
            self._show_documentation("libraries")

    @on(Button.Pressed, "#flags-documentation")
    @on(Button.Pressed, "#libraries-documentation")
    def documentation_pressed(self, event: Button.Pressed) -> None:
        """Shows the documentation of what the panel of the button highlights."""
        self._show_documentation((event.button.id or "").removesuffix("-documentation"))

    def action_documentation(self) -> None:
        """Shows the documentation of what the flags or libraries panel highlights, if shown."""
        active = self.query_one("#panels", TabbedContent).active.removeprefix("panel-")
        if active in ("flags", "libraries"):
            self._show_documentation(active)

    def _show_documentation(self, panel: str) -> None:
        documented = self._documented(panel)
        if documented is None:
            self.notify("No documentation")
        else:
            self.push_screen(DocumentationScreen(*documented))

    @on(Button.Pressed, "#add-operator")
    def add_operator(self) -> None:
        """Asks for an operator, and declares it at the end of the theory (with `op/3`)."""

        def declare(text: str | None) -> None:
            if text is None:
                return
            parts = text.split(maxsplit=2)
            valid = (
                len(parts) == 3
                and parts[0].isdigit()
                and int(parts[0]) <= 1200
                and parts[1].lower() in _SPECIFIERS
            )
            if not valid:
                self.notify(f"Invalid operator: {text!r}", title="Error", severity="error")
                return
            priority, specifier, name = parts
            source = self.query_one("#source", TextArea)
            separator = "" if not source.text or source.text.endswith("\n") else "\n"
            directive = f"{separator}:- op({int(priority)}, {specifier.lower()}, {name}).\n"
            source.insert(directive, source.document.end)

        self.push_screen(
            PromptScreen("Add an operator: priority, specifier, name (e.g. 700 xfx ===)"), declare
        )

    @on(Button.Pressed, "#clear-solutions")
    def clear_solutions(self) -> None:
        """Forgets the concluded resolutions of the current page."""
        if (page := self.page) is not None:
            self.dispatch(m.ClearHistory(page.id))

    @on(Button.Pressed, "#controls Button")
    def control_pressed(self, event: Button.Pressed) -> None:
        """Runs the command of a control button."""
        match event.button.id:
            case "stop":
                self.action_stop()
            case "reset":
                self.action_reset()
            case button_id:
                mode = next(mode for mode, b, _ in _MODES if b == button_id)
                self.action_solve(mode)

    def action_solve(self, mode: m.Mode) -> None:
        """Solves the query of the current page, or asks for more solutions."""
        page = self.page
        if page is None:
            return
        if page.resolution.can_continue:
            self.dispatch(m.Next(page.id, mode))
        elif page.resolution.can_solve:
            self.dispatch(m.Solve(page.id, mode))

    def action_stop(self) -> None:
        """Stops the resolution of the current page."""
        if (page := self.page) is not None and page.resolution.can_stop:
            self.dispatch(m.Stop(page.id))

    def action_reset(self) -> None:
        """Resets the solver of the current page."""
        if (page := self.page) is not None:
            self.dispatch(m.Reset(page.id))

    def action_new_scratch_page(self) -> None:
        """Creates a scratch page."""
        self.dispatch(m.NewScratchPage())

    def action_new_document_page(self) -> None:
        """Creates a page editing a new file."""
        self.dispatch(m.NewDocumentPage())

    def action_open_document(self) -> None:
        """Opens a file in a new page."""
        self.dispatch(m.RequestOpenDocument())

    def _save(self, save_as: bool) -> None:
        page = self.page
        if page is None:
            return
        if page.document_id is None:
            self.notify("Scratch pages are not saved: open a new file (ctrl+n) instead")
        else:
            self.dispatch(m.RequestSave(page.document_id, save_as))

    def action_save(self) -> None:
        """Saves the file of the current page."""
        self._save(save_as=False)

    def action_save_as(self) -> None:
        """Saves the file of the current page elsewhere."""
        self._save(save_as=True)

    def action_reload(self) -> None:
        """Reloads the file of the current page."""
        if (page := self.page) is not None and page.document_id is not None:
            self.dispatch(m.RequestReload(page.document_id))

    def action_close_page(self) -> None:
        """Closes the current page."""
        if (page := self.page) is not None:
            self.dispatch(m.RequestClosePage(page.id))

    def action_request_exit(self) -> None:
        """Asks to quit (confirming if files have unsaved changes)."""
        if self._closed:
            self.exit()
        else:
            self.dispatch(m.RequestExit())

    # --- effects ---------------------------------------------------------------------------------

    @on(BridgeError)
    def report_error(self, message: BridgeError) -> None:
        """Shows an error of the GUI application."""
        self.notify(message.message, title="Error", severity="error")

    @on(EffectRequested)
    def handle_effect(self, message: EffectRequested) -> None:
        """Fulfils an effect (on Textual's event loop)."""
        match message.effect:
            case m.PickOpenDocument():
                self.push_screen(PathScreen("Open file"), self._open_picked)
            case m.PickSaveDestination(_, document_id, suggested_name):
                self.push_screen(
                    PathScreen("Save as", suggested_name),
                    lambda path: self._save_picked(document_id, path),
                )
            case m.WriteDocument(_, document_id, path, text, revision):
                self._write(document_id, path, text, revision)
            case m.ReadDocument(_, document_id, path):
                self._read(document_id, path)
            case m.ConfirmCloseDirtyPage(_, page_id, _, display_name):
                self.push_screen(
                    ChoiceScreen(
                        f"{display_name} has unsaved changes: save it before closing?",
                        [("SAVE", "Save"), ("DISCARD", "Discard"), ("CANCEL", "Cancel")],
                        cancel="CANCEL",
                    ),
                    lambda choice: self.dispatch(m.ClosePageDecision(page_id, choice)),  # type: ignore[arg-type]
                )
            case m.ConfirmReloadDirtyDocument(_, document_id, display_name):
                self.push_screen(
                    ChoiceScreen(
                        f"{display_name} has unsaved changes: discard them and reload it?",
                        [("DISCARD_CHANGES", "Discard and reload"), ("CANCEL", "Cancel")],
                        cancel="CANCEL",
                    ),
                    lambda choice: self.dispatch(m.ReloadDecision(document_id, choice)),  # type: ignore[arg-type]
                )
            case m.ConfirmExitWithDirtyDocuments(_, document_ids):
                self.push_screen(
                    ChoiceScreen(
                        f"{len(document_ids)} file(s) have unsaved changes: quit anyway?",
                        [("QUIT", "Quit"), ("CANCEL", "Cancel")],
                        cancel="CANCEL",
                    ),
                    self._exit_decided,
                )
            case m.CopyToClipboard(_, text):
                self.copy_to_clipboard(text)
                self.notify("Copied to the clipboard")
            case m.ExitApplication():
                self._close_bridge()
                self.exit()

    def _open_picked(self, text: str | None) -> None:
        if text is None:
            return
        path = Path(text).expanduser()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            self.notify(f"Cannot open {path}: {error}", title="Error", severity="error")
            return
        self.dispatch(m.OpenDocumentLoaded(path.absolute(), text))

    def _save_picked(self, document_id: str, text: str | None) -> None:
        if text is None:
            self.dispatch(m.SaveCancelled(document_id))
        else:
            path = Path(text).expanduser().absolute()
            self.dispatch(m.SaveDestinationSelected(document_id, path))

    def _write(self, document_id: str, path: Path | None, text: str, revision: int) -> None:
        if path is None:
            self.dispatch(m.SaveFailed(document_id, "Not a file"))
            return
        try:
            path.write_text(text, encoding="utf-8")
        except OSError as error:
            self.notify(f"Cannot save {path}: {error}", title="Error", severity="error")
            self.dispatch(m.SaveFailed(document_id, str(error)))
        else:
            self.dispatch(m.SaveSucceeded(document_id, path, revision))

    def _read(self, document_id: str, path: Path | None) -> None:
        if path is None:
            self.dispatch(m.ReloadFailed(document_id, "Not a file"))
            return
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            self.notify(f"Cannot reload {path}: {error}", title="Error", severity="error")
            self.dispatch(m.ReloadFailed(document_id, str(error)))
        else:
            self.dispatch(m.ReloadSucceeded(document_id, text))

    def _exit_decided(self, choice: str | None) -> None:
        self.dispatch(m.ExitConfirmed() if choice == "QUIT" else m.ExitCancelled())
