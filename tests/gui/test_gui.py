"""Tests for `tuprolog.gui`: the JVM facade over 2P-Kt's GUI application, and its factories."""

import queue
import threading
from pathlib import Path

import pytest

from tuprolog import gui
from tuprolog.gui import (
    ApplicationAction,
    ConsumptionMode,
    DocumentOrigin,
    GuiEffect,
    PageAction,
    ResolutionStatus,
    SolutionPresentation,
    WorkspaceAction,
)

TIMEOUT = 30  # seconds


class Recorder:
    def __init__(self):
        self.states = queue.Queue()
        self.effects = queue.Queue()
        self.errors = queue.Queue()

    def gui(self, **kwargs):
        return gui.prolog_gui(self.states.put, self.effects.put, self.errors.put, **kwargs)


@pytest.fixture
def recorder():
    return Recorder()


@pytest.fixture
def facade(recorder):
    with recorder.gui() as facade:
        facade.start().get()
        yield facade
    assert recorder.errors.empty()


def wait_for(facade, condition):
    for _ in range(TIMEOUT * 20):
        if condition(facade.state):
            return facade.state
        threading.Event().wait(0.05)
    raise AssertionError(f"No state matched: {facade.state}")


def new_page(facade, text=""):
    facade.dispatch(WorkspaceAction.NewScratchPage(None, text)).get()
    return facade.state.workspace.selected_page_id


def test_exports():
    for name in ["GuiFacade", "GuiState", "PageAction", "GuiEffect", "prolog_gui", "path_origin"]:
        assert name in gui.__all__
    assert gui.PROLOG_PROFILE_ID == "prolog"


def test_start_and_state_callback(facade, recorder):
    assert facade.state.application.started
    assert recorder.states.get(timeout=TIMEOUT) is not None


def test_dispatch_is_ordered(facade):
    page_id = new_page(facade)
    futures = [facade.dispatch(PageAction.ChangeQuery(page_id, f"q{i}")) for i in range(50)]
    futures[-1].get()
    assert all(f.isDone() for f in futures)
    assert str(facade.state.workspace.page(page_id).query.text) == "q49"


def test_solve(facade):
    page_id = new_page(facade, "p(1). p(2).")
    facade.dispatch(PageAction.ChangeQuery(page_id, "p(X)")).get()
    facade.dispatch(PageAction.Solve(page_id, ConsumptionMode.TEN)).get()
    state = wait_for(
        facade,
        lambda s: s.workspace.page(page_id).resolution.status == ResolutionStatus.COMPLETED,
    )
    solutions = state.workspace.page(page_id).resolution.solutions
    assert [isinstance(s, SolutionPresentation.Yes) for s in solutions] == [True, True]
    assert [str(s.bindings[0].value) for s in solutions] == ["1", "2"]


def test_effects(facade, recorder):
    facade.dispatch(ApplicationAction.RequestExit.INSTANCE).get()
    assert isinstance(recorder.effects.get(timeout=TIMEOUT), GuiEffect.ExitApplication)


def test_callback_errors_go_to_on_error(recorder):
    def failing(_):
        raise ValueError("boom")

    with gui.prolog_gui(failing, recorder.effects.put, recorder.errors.put) as facade:
        facade.start().get()
        assert "boom" in str(recorder.errors.get(timeout=TIMEOUT))


def test_default_on_error_logs(caplog):
    def failing(_):
        raise ValueError("boom")

    with gui.prolog_gui(failing, lambda _: None) as facade:
        facade.start().get()
        wait_for(facade, lambda _: "boom" in caplog.text)


def test_close_is_idempotent(recorder):
    facade = recorder.gui(timeout=1.0)
    facade.start().get()
    facade.close()
    facade.close()
    assert facade.is_closed
    with pytest.raises(Exception, match="closed"):
        facade.dispatch(ApplicationAction.RequestExit.INSTANCE).get()


def test_path_origins(tmp_path):
    origin = gui.path_origin(tmp_path / "theory.pl")
    assert str(origin.provider_id) == gui.PATH_PROVIDER
    assert str(origin.display_name) == "theory.pl"
    assert gui.origin_path(origin) == tmp_path / "theory.pl"
    assert gui.origin_path(DocumentOrigin("browser", "handle", "theory.pl")) is None
    assert gui.path_origin("relative.pl").opaque_reference == str(Path("relative.pl").absolute())
