"""The modal screens of the terminal IDE: asking for a text (e.g. a path), or for a choice, and
showing documentation."""

from __future__ import annotations

from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Markdown

__all__ = ["ARROW_BINDINGS", "ChoiceScreen", "DocumentationScreen", "PathScreen", "PromptScreen"]

ARROW_BINDINGS: list[BindingType] = [
    # not priority: widgets using arrow keys (e.g. editors, inputs, tables, tabs) keep them
    Binding("left,up", "app.focus_previous", "Previous control", show=False),
    Binding("right,down", "app.focus_next", "Next control", show=False),
]
"""Arrow keys moving the focus among controls (the app's bindings do not apply to modal screens)."""


class PromptScreen(ModalScreen[str | None]):
    """Asks for a text: dismissed with the (stripped) text, or `None` if empty or cancelled.

    Args:
        title: What the text is for, e.g. `"Value of unknown"`.
        default: The initial text.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "cancel", "Cancel"),
        *ARROW_BINDINGS,
    ]
    PLACEHOLDER = ""

    def __init__(self, title: str, default: str = "") -> None:
        super().__init__()
        self._title = title
        self._default = default

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label(self._title, classes="dialog-title")
            yield Input(value=self._default, placeholder=self.PLACEHOLDER, id="path")
            with Horizontal(classes="dialog-buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    @on(Input.Submitted)
    @on(Button.Pressed, "#ok")
    def submit(self) -> None:
        """Dismisses the screen with the typed text, if any."""
        self.dismiss(self.query_one("#path", Input).value.strip() or None)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Dismisses the screen with `None`."""
        self.dismiss(None)


class PathScreen(PromptScreen):
    """Asks for a file path, as a `PromptScreen`."""

    PLACEHOLDER = "Path"


class ChoiceScreen(ModalScreen[str]):
    """Asks to choose among options: dismissed with the chosen key, or `cancel` on escape.

    Args:
        message: The question.
        options: The options, as pairs of a key and a button label.
        cancel: The key escape chooses.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "cancel", "Cancel"),
        *ARROW_BINDINGS,
    ]

    def __init__(self, message: str, options: list[tuple[str, str]], cancel: str) -> None:
        super().__init__()
        self._message = message
        self._options = options
        self._cancel = cancel

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label(self._message, classes="dialog-title")
            with Horizontal(classes="dialog-buttons"):
                for key, label in self._options:
                    yield Button(label, id=f"choice-{key.lower().replace('_', '-')}", name=key)

    @on(Button.Pressed)
    def choose(self, event: Button.Pressed) -> None:
        """Dismisses the screen with the key of the pressed button."""
        self.dismiss(event.button.name or self._cancel)

    def action_cancel(self) -> None:
        """Dismisses the screen with the cancel key."""
        self.dismiss(self._cancel)


class DocumentationScreen(ModalScreen[None]):
    """Shows the Markdown documentation of a symbol (e.g. a flag, or a predicate of a library).

    Args:
        title: What is documented, e.g. `"member/2"`.
        markdown: The documentation.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "close", "Close"),
        *ARROW_BINDINGS,
    ]

    def __init__(self, title: str, markdown: str) -> None:
        super().__init__()
        self._title = title
        self._markdown = markdown

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog documentation"):
            yield Label(self._title, classes="dialog-title")
            with VerticalScroll():
                yield Markdown(self._markdown, id="documentation")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Close", variant="primary", id="close")

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Dismisses the screen."""
        self.dismiss(None)
