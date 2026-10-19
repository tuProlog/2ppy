"""A minimal fake `GuiBridge`: it records actions, and lets tests emit states and effects."""

import re

from tuprolog.tui import Effect, Page, Resolution, Snapshot, SyntaxToken


class FakeBridge:
    def __init__(self):
        self.actions = []
        self.started = 0
        self.closed = 0

    def start(self, on_state, on_effect, on_error):
        self.started += 1
        self.on_state, self.on_effect, self.on_error = on_state, on_effect, on_error

    def dispatch(self, action):
        self.actions.append(action)

    def close(self):
        self.closed += 1

    def is_timeout(self, text):
        return text != "soon"

    def documentation_preview(self, markdown):
        return markdown.split("\n")[0]

    def analyze(self, source, operators=()):
        # every word is a variable
        return tuple(
            SyntaxToken("VARIABLE", (line, match.start()), (line, match.end()))
            for line, text in enumerate(source.split("\n"))
            for match in re.finditer(r"\w+", text)
        )

    def emit(self, snapshot: Snapshot):
        self.on_state(snapshot)

    def effect(self, effect: Effect):
        self.on_effect(effect)

    def of_type(self, kind):
        return [a for a in self.actions if isinstance(a, kind)]


def page(page_id="page-1", **kwargs) -> Page:
    kwargs.setdefault("title", page_id)
    return Page(id=page_id, **kwargs)


def snapshot(*pages: Page, selected: str | None = None) -> Snapshot:
    return Snapshot(
        started=True,
        pages=pages,
        selected_page_id=selected if selected is not None else (pages[0].id if pages else None),
    )


__all__ = ["FakeBridge", "Resolution", "page", "snapshot"]
