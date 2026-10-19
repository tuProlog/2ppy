package it.unibo.tuprolog.ppy.gui

import it.unibo.tuprolog.ui.gui.application.GuiApplication
import it.unibo.tuprolog.ui.gui.application.buildGuiApplication
import it.unibo.tuprolog.ui.gui.controller.ApplicationAction
import it.unibo.tuprolog.ui.gui.controller.GuiAction
import it.unibo.tuprolog.ui.gui.controller.GuiEffect
import it.unibo.tuprolog.ui.gui.controller.PageAction
import it.unibo.tuprolog.ui.gui.identity.PageId
import it.unibo.tuprolog.ui.gui.model.GuiState
import it.unibo.tuprolog.ui.gui.model.PageState
import it.unibo.tuprolog.ui.gui.model.resolve
import it.unibo.tuprolog.ui.gui.presentation.formatDurationInput
import it.unibo.tuprolog.ui.gui.presentation.parseDurationInput
import it.unibo.tuprolog.ui.gui.solver.ResolutionSchedulingPolicy
import it.unibo.tuprolog.ui.gui.solver.SolverProfile
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineName
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.CoroutineStart
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.asCoroutineDispatcher
import kotlinx.coroutines.cancel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.util.concurrent.CompletableFuture
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicBoolean
import java.util.function.Consumer
import kotlin.time.Duration.Companion.milliseconds

/**
 * A blocking, callback-based facade over 2P-Kt's toolkit-neutral [GuiApplication], for callers that cannot use
 * Kotlin coroutines (e.g. Python, via JPype).
 *
 * The facade owns the coroutine scope the application runs in. Actions are [dispatch]ed in order, one at a time,
 * by a single coroutine; states are delivered to [onState] with latest-state semantics (a slow consumer skips
 * intermediate states, never the latest one); effects are delivered to [onEffect] losslessly and in order.
 * Callbacks run on JVM threads other than the caller's: consumers must marshal them to their own UI thread.
 * Exceptions thrown by callbacks or by dispatched actions go to [onError].
 */
class GuiFacade private constructor(
    private val onState: Consumer<GuiState>,
    private val onEffect: Consumer<GuiEffect>,
    private val onError: Consumer<Throwable>,
    profiles: List<SolverProfile>,
    timeoutMillis: Long,
    defaultOptions: Map<String, String>,
    schedulingPolicy: ResolutionSchedulingPolicy,
) : AutoCloseable {
    private class Pending(
        val action: () -> GuiAction,
        val done: CompletableFuture<Void?> = CompletableFuture(),
    )

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default + CoroutineName("2ppy-gui"))

    // the callbacks and the actions run on threads of their own, rather than on the default dispatcher's, which
    // solvers may keep busy (2P-Kt cannot interrupt a resolution between solutions): states, effects and actions
    // keep flowing whatever the solvers do; three threads, so that a callback waiting for an action does not
    // block it
    private val events =
        Executors
            .newFixedThreadPool(EVENT_THREADS) { Thread(it, "2ppy-gui-events").apply { isDaemon = true } }
            .asCoroutineDispatcher()
    private val application =
        buildGuiApplication(scope) {
            profiles.forEach { solverProfile(it) }
            defaultTimeout(timeoutMillis.milliseconds)
            defaultOptions(defaultOptions)
            schedulingPolicy(schedulingPolicy)
        }
    private val controller = application.controller
    private val actions = Channel<Pending>(Channel.UNLIMITED)
    private val started = AtomicBoolean(false)
    private val closed = AtomicBoolean(false)

    /** The current state of the application. */
    val state: GuiState
        get() = controller.state.value

    /** Whether [close] was called. */
    val isClosed: Boolean
        get() = closed.get()

    /**
     * Subscribes the callbacks, starts processing actions, and dispatches [ApplicationAction.Start]; does nothing
     * if already started.
     *
     * @return a future completing once the application has started.
     */
    fun start(): CompletableFuture<Void?> {
        if (!started.compareAndSet(false, true)) {
            return CompletableFuture.completedFuture(null)
        }
        // UNDISPATCHED: subscribed before any action runs, so that no state or effect is missed
        scope.launch(events, start = CoroutineStart.UNDISPATCHED) {
            controller.state.collect { notify(onState, it) }
        }
        scope.launch(events, start = CoroutineStart.UNDISPATCHED) {
            controller.effects.collect { notify(onEffect, it) }
        }
        scope.launch(events) {
            for (pending in actions) {
                apply(pending)
            }
        }
        return dispatch(ApplicationAction.Start)
    }

    /**
     * Enqueues [action]: actions are applied in the order they are dispatched, once [start]ed.
     *
     * @return a future completing once [action] has been applied (exceptionally if it failed, or the facade is
     * closed).
     */
    fun dispatch(action: GuiAction): CompletableFuture<Void?> = enqueue { action }

    /**
     * Enqueues setting the flag [name] of the solvers of page [pageId] to [value] (a Prolog term), as a
     * [PageAction.ChangeConfiguration] keeping the rest of the page's configuration as it is when applied.
     *
     * @return a future completing once applied, as for [dispatch].
     */
    fun changeFlag(
        pageId: PageId,
        name: String,
        value: String,
    ): CompletableFuture<Void?> =
        enqueue {
            val configuration = checkNotNull(state.workspace.page(pageId)) { "No page $pageId" }.configuration
            PageAction.ChangeConfiguration(
                pageId,
                configuration.copy(optionOverrides = configuration.optionOverrides + (name to value)),
            )
        }

    /**
     * Enqueues setting the timeout of the resolutions of page [pageId] to [timeout], written as [isTimeout]
     * accepts (e.g. `500ms`, `2s 500ms`, `1m 30s`, or `none`), as a [PageAction.ChangeTimeout].
     *
     * @return a future completing once applied, as for [dispatch].
     * @throws IllegalArgumentException if [timeout] is not a valid timeout.
     */
    fun changeTimeout(
        pageId: PageId,
        timeout: String,
    ): CompletableFuture<Void?> {
        val duration = requireNotNull(parseDurationInput(timeout)) { "Invalid timeout: $timeout" }
        return dispatch(PageAction.ChangeTimeout(pageId, duration))
    }

    private fun enqueue(action: () -> GuiAction): CompletableFuture<Void?> {
        val pending = Pending(action)
        if (closed.get() || actions.trySend(pending).isFailure) {
            pending.done.completeExceptionally(IllegalStateException("The GUI facade is closed"))
        }
        return pending.done
    }

    /** Shuts the application down, releasing its solvers and coroutines; idempotent. */
    override fun close() {
        if (!closed.compareAndSet(false, true)) return
        actions.close()
        runBlocking { application.close() }
        scope.cancel()
        events.close() // shuts its threads down, without waiting (close may run on one of them)
        while (true) {
            val pending = actions.tryReceive().getOrNull() ?: break
            pending.done.completeExceptionally(IllegalStateException("The GUI facade is closed"))
        }
    }

    private suspend fun apply(pending: Pending) {
        try {
            controller.dispatch(pending.action())
            pending.done.complete(null)
        } catch (e: CancellationException) {
            pending.done.cancel(false)
            throw e
        } catch (e: Throwable) {
            pending.done.completeExceptionally(e)
            onError.accept(e)
        }
    }

    private fun <T> notify(
        consumer: Consumer<T>,
        value: T,
    ) {
        try {
            consumer.accept(value)
        } catch (e: Throwable) {
            onError.accept(e)
        }
    }

    companion object {
        private const val EVENT_THREADS = 3

        /** The id of the Prolog solver profile of [prologProfile]. */
        const val PROLOG_PROFILE_ID: String = "prolog"

        /** The default timeout of resolutions, in milliseconds. */
        const val DEFAULT_TIMEOUT_MILLIS: Long = 5_000

        private val PRINT_STACK_TRACE = Consumer<Throwable> { it.printStackTrace() }

        /**
         * Whether [text] is a timeout: `none` or `0` (no timeout), or amounts of `ms`, `s`, `m`, `h`, `d` and `w`
         * (e.g. `2s 500ms`), up to a week.
         */
        @JvmStatic
        fun isTimeout(text: String): Boolean = parseDurationInput(text) != null

        /** The timeout of [page]'s resolutions in [state], written as [isTimeout] accepts (e.g. `5s`). */
        @JvmStatic
        fun timeoutOf(
            state: GuiState,
            page: PageState,
        ): String = formatDurationInput(state.workspace.configuration.resolve(page.configuration).timeout)

        /** The solver profile of ISO Prolog solvers, with the IO and OOP libraries (see [SolverProfiles]). */
        @JvmStatic
        fun prologProfile(): SolverProfile = SolverProfiles.prolog()

        /**
         * Creates a facade whose pages solve with [profiles] (the first one by default); call [start] to run it.
         *
         * [defaultOptions] are the flags of every solver (names to values, as Prolog terms), and
         * [schedulingPolicy] says whether resolutions of different pages may run concurrently.
         */
        @JvmStatic
        @JvmOverloads
        fun of(
            profiles: List<SolverProfile>,
            onState: Consumer<GuiState>,
            onEffect: Consumer<GuiEffect>,
            onError: Consumer<Throwable> = PRINT_STACK_TRACE,
            timeoutMillis: Long = DEFAULT_TIMEOUT_MILLIS,
            defaultOptions: Map<String, String> = emptyMap(),
            schedulingPolicy: ResolutionSchedulingPolicy = ResolutionSchedulingPolicy.PER_PAGE_CONCURRENT,
        ): GuiFacade =
            GuiFacade(
                onState,
                onEffect,
                onError,
                profiles.toList(),
                timeoutMillis,
                defaultOptions.toMap(),
                schedulingPolicy,
            )

        /** Creates a facade whose pages solve with ISO Prolog solvers; call [start] to run it. */
        @JvmStatic
        @JvmOverloads
        fun prolog(
            onState: Consumer<GuiState>,
            onEffect: Consumer<GuiEffect>,
            onError: Consumer<Throwable> = PRINT_STACK_TRACE,
            timeoutMillis: Long = DEFAULT_TIMEOUT_MILLIS,
        ): GuiFacade = of(listOf(prologProfile()), onState, onEffect, onError, timeoutMillis)
    }
}
