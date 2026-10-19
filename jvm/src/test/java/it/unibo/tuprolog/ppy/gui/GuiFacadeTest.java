package it.unibo.tuprolog.ppy.gui;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import it.unibo.tuprolog.ui.gui.controller.ApplicationAction;
import it.unibo.tuprolog.ui.gui.controller.ConsumptionMode;
import it.unibo.tuprolog.ui.gui.controller.GuiEffect;
import it.unibo.tuprolog.ui.gui.controller.PageAction;
import it.unibo.tuprolog.ui.gui.controller.WorkspaceAction;
import it.unibo.tuprolog.ui.gui.identity.PageId;
import it.unibo.tuprolog.ui.gui.model.GuiState;
import it.unibo.tuprolog.ui.gui.model.PageState;
import it.unibo.tuprolog.ui.gui.model.ResolutionStatus;
import it.unibo.tuprolog.ui.gui.presentation.SolutionPresentation;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.function.Predicate;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** Exercises the facade as Java (hence JPype) sees it: static factories, consumers, futures, no coroutines. */
class GuiFacadeTest {
    private static final long TIMEOUT_SECONDS = 30;

    private final BlockingQueue<GuiState> states = new LinkedBlockingQueue<>();
    private final BlockingQueue<GuiEffect> effects = new LinkedBlockingQueue<>();
    private final BlockingQueue<Throwable> errors = new LinkedBlockingQueue<>();
    private GuiFacade facade;

    @BeforeEach
    void createFacade() {
        facade = GuiFacade.prolog(states::add, effects::add, errors::add);
    }

    @AfterEach
    void closeFacade() {
        facade.close();
        assertTrue(errors.isEmpty(), () -> "Unexpected errors: " + errors);
    }

    private static void await(CompletableFuture<?> future) throws Exception {
        future.get(TIMEOUT_SECONDS, TimeUnit.SECONDS);
    }

    private GuiState awaitState(Predicate<GuiState> condition) throws InterruptedException {
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(TIMEOUT_SECONDS);
        while (System.nanoTime() < deadline) {
            GuiState state = states.poll(100, TimeUnit.MILLISECONDS);
            if (state != null && condition.test(state)) {
                return state;
            }
            if (condition.test(facade.getState())) {
                return facade.getState();
            }
        }
        throw new AssertionError("No state matched within " + TIMEOUT_SECONDS + "s: " + facade.getState());
    }

    private PageId newScratchPage(String text) throws Exception {
        await(facade.start());
        await(facade.dispatch(new WorkspaceAction.NewScratchPage(null, text)));
        return facade.getState().getWorkspace().getSelectedPageId();
    }

    private PageState page(PageId id) {
        return facade.getState().getWorkspace().page(id);
    }

    private static Predicate<GuiState> onPage(PageId id, Predicate<PageState> condition) {
        return state -> {
            PageState page = state.getWorkspace().page(id);
            return page != null && condition.test(page);
        };
    }

    @Test
    void startDeliversTheStartedState() throws Exception {
        await(facade.start());
        assertTrue(facade.getState().getApplication().getStarted());
        awaitState(state -> state.getApplication().getStarted());
        await(facade.start()); // idempotent
    }

    @Test
    void actionsDispatchedBeforeStartAreAppliedAfterIt() throws Exception {
        CompletableFuture<Void> created = facade.dispatch(new WorkspaceAction.NewScratchPage("early", ""));
        assertTrue(facade.getState().getWorkspace().getPages().isEmpty());
        await(facade.start());
        await(created);
        assertEquals("early", facade.getState().getWorkspace().getPages().get(0).getTitle());
    }

    @Test
    void actionsAreAppliedInDispatchOrder() throws Exception {
        PageId id = newScratchPage("");
        CompletableFuture<Void> last = null;
        for (int i = 0; i < 100; i++) {
            last = facade.dispatch(new PageAction.ChangeQuery(id, "q" + i));
        }
        await(last);
        assertEquals("q99", page(id).getQuery().getText());
    }

    @Test
    void solvingDeliversSolutions() throws Exception {
        PageId id = newScratchPage("p(1). p(2).");
        await(facade.dispatch(new PageAction.ChangeQuery(id, "p(X)")));
        await(facade.dispatch(new PageAction.Solve(id, ConsumptionMode.ONE)));
        GuiState state = awaitState(onPage(id, p -> p.getResolution().getCanContinue()));
        List<SolutionPresentation> solutions = state.getWorkspace().page(id).getResolution().getSolutions();
        SolutionPresentation.Yes yes = assertInstanceOf(SolutionPresentation.Yes.class, solutions.get(0));
        assertEquals("1", yes.getBindings().get(0).getValue());
        await(facade.dispatch(new PageAction.Next(id, ConsumptionMode.TEN)));
        awaitState(onPage(id, p -> p.getResolution().getStatus() == ResolutionStatus.COMPLETED));
    }

    @Test
    void changeFlagOverridesTheFlagOfThePageSolvers() throws Exception {
        PageId id = newScratchPage("");
        await(facade.changeFlag(id, "unknown", "fail"));
        assertEquals("fail", page(id).getConfiguration().getOptionOverrides().get("unknown"));
        await(facade.dispatch(new PageAction.ChangeQuery(id, "current_flag(unknown, fail)")));
        await(facade.dispatch(new PageAction.Solve(id, ConsumptionMode.ONE)));
        GuiState state = awaitState(onPage(id, p -> !p.getResolution().getSolutions().isEmpty()));
        assertInstanceOf(
            SolutionPresentation.Yes.class,
            state.getWorkspace().page(id).getResolution().getSolutions().get(0)
        );
    }

    @Test
    void changeTimeoutSetsThePageTimeout() throws Exception {
        PageId id = newScratchPage("");
        assertEquals("5s", GuiFacade.timeoutOf(facade.getState(), page(id)));
        assertTrue(GuiFacade.isTimeout("1m 30s"));
        assertFalse(GuiFacade.isTimeout("soon"));
        await(facade.changeTimeout(id, "1m 30s"));
        assertEquals("1m 30s", GuiFacade.timeoutOf(facade.getState(), page(id)));
        assertThrows(IllegalArgumentException.class, () -> facade.changeTimeout(id, "soon"));
    }

    @Test
    void effectsAreDelivered() throws Exception {
        await(facade.start());
        await(facade.dispatch(ApplicationAction.RequestExit.INSTANCE));
        GuiEffect effect = effects.poll(TIMEOUT_SECONDS, TimeUnit.SECONDS);
        assertInstanceOf(GuiEffect.ExitApplication.class, effect);
    }

    @Test
    void callbackErrorsAreReported() throws Exception {
        try (GuiFacade failing = GuiFacade.prolog(state -> { throw new IllegalStateException("boom"); }, effects::add, errors::add)) {
            await(failing.start());
            Throwable error = errors.poll(TIMEOUT_SECONDS, TimeUnit.SECONDS);
            assertInstanceOf(IllegalStateException.class, error);
        }
        errors.clear();
    }

    @Test
    void closeIsIdempotentAndRejectsLaterActions() throws Exception {
        await(facade.start());
        facade.close();
        facade.close();
        assertTrue(facade.isClosed());
        CompletableFuture<Void> rejected = facade.dispatch(ApplicationAction.RequestExit.INSTANCE);
        ExecutionException error = assertThrows(ExecutionException.class, () -> await(rejected));
        assertInstanceOf(IllegalStateException.class, error.getCause());
    }

    @Test
    void statesAndActionsFlowWhileSolversKeepEveryThreadBusy() throws Exception {
        // more endless resolutions than cores: they keep every thread of the default dispatcher busy, as 2P-Kt
        // cannot interrupt them until they time out
        int busy = Runtime.getRuntime().availableProcessors() + 1;
        BlockingQueue<GuiState> seen = new LinkedBlockingQueue<>();
        try (GuiFacade loaded = GuiFacade.prolog(seen::add, effects::add, errors::add, 10_000)) {
            await(loaded.start());
            for (int i = 0; i < busy; i++) {
                await(loaded.dispatch(new WorkspaceAction.NewScratchPage(null, "loop :- loop.")));
                PageId id = loaded.getState().getWorkspace().getSelectedPageId();
                await(loaded.dispatch(new PageAction.ChangeQuery(id, "loop")));
                await(loaded.dispatch(new PageAction.Solve(id, ConsumptionMode.ONE)));
            }
            Thread.sleep(500); // the resolutions start computing
            seen.clear();
            long start = System.nanoTime();
            await(loaded.dispatch(new WorkspaceAction.NewScratchPage("responsive", "")));
            long deadline = start + TimeUnit.SECONDS.toNanos(5);
            boolean delivered = false;
            while (!delivered && System.nanoTime() < deadline) {
                GuiState state = seen.poll(100, TimeUnit.MILLISECONDS);
                delivered = state != null
                        && state.getWorkspace().getPages().stream().anyMatch(p -> p.getTitle().equals("responsive"));
            }
            assertTrue(delivered, "No state delivered while the solvers were busy");
        }
    }
}
