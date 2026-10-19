package it.unibo.tuprolog.ppy.gui

import it.unibo.tuprolog.solve.Solution
import it.unibo.tuprolog.solve.SolveOptions
import it.unibo.tuprolog.solve.SolverBuilder
import it.unibo.tuprolog.solve.SolverFactory
import it.unibo.tuprolog.solve.library.Library
import it.unibo.tuprolog.solve.setProbabilistic
import it.unibo.tuprolog.solve.libs.io.IOLib
import it.unibo.tuprolog.solve.libs.oop.OOPLib
import it.unibo.tuprolog.solve.problog.ProblogSolverFactory
import it.unibo.tuprolog.solve.prolog.PrologSolverFactory
import it.unibo.tuprolog.theory.Theory
import it.unibo.tuprolog.ui.gui.identity.FeatureId
import it.unibo.tuprolog.ui.gui.identity.SolverProfileId
import it.unibo.tuprolog.ui.gui.model.FeatureValue
import it.unibo.tuprolog.ui.gui.plp.plpFeatureState
import it.unibo.tuprolog.ui.gui.prolog.SolverFactorySession
import it.unibo.tuprolog.ui.gui.prolog.solverFactoryProfile
import it.unibo.tuprolog.ui.gui.solver.SolverCapabilities
import it.unibo.tuprolog.ui.gui.solver.SolverProfile
import it.unibo.tuprolog.ui.gui.solver.SolverSessionCreationRequest
import it.unibo.tuprolog.unify.Unificator

/**
 * Factories of [SolverProfile]s whose solvers can be customised beyond what 2P-Kt's `solverFactoryProfile` offers:
 * their libraries, initial dynamic knowledge base, unificator, standard library, and probabilistic solving.
 *
 * The static knowledge base of a page's solver is always the page's text.
 */
object SolverProfiles {
    /** The id of [prolog]'s profile. */
    const val PROLOG_ID: String = "prolog"

    /** The id of [problog]'s profile. */
    const val PROBLOG_ID: String = "problog"

    /** The libraries of 2P-Kt's IDEs: 2P-Kt's OOP and IO libraries. */
    @JvmStatic
    val defaultLibraries: List<Library> = listOf(OOPLib, IOLib)

    /**
     * A profile building its solvers from [factory].
     *
     * @param libraries the libraries loaded on top of the standard one
     * @param dynamicKb the initial dynamic knowledge base of every solver (e.g. after a reset)
     * @param unificator the unificator of the solvers, or `null` for the factory's default
     * @param builtins whether the solvers have the factory's standard library
     * @param probabilistic whether every resolution is probabilistic (as for ProbLog), with the probability of each
     * solution in its metadata
     */
    @JvmStatic
    @JvmOverloads
    fun of(
        factory: SolverFactory,
        id: String,
        displayName: String,
        libraries: List<Library> = defaultLibraries,
        dynamicKb: Theory = Theory.empty(),
        unificator: Unificator? = null,
        builtins: Boolean = true,
        probabilistic: Boolean = false,
    ): SolverProfile {
        val configured = ConfiguredSolverFactory(factory, dynamicKb.toImmutableTheory(), unificator, builtins)
        val capabilities =
            setOf(SolverCapabilities.CANCELLATION) +
                if (probabilistic) setOf(SolverCapabilities.PROBABILISTIC_SOLUTIONS) else emptySet()
        return solverFactoryProfile(
            configured,
            SolverProfileId(id),
            displayName,
            capabilities = capabilities,
            solutionFeatures = if (probabilistic) Solution::plpFeatureState else { _ -> emptyMap() },
            runtimeLibraries = libraries.toList(),
            newSession = if (probabilistic) ::ProbabilisticSession else ::SolverFactorySession,
        )
    }

    /** A profile of ISO Prolog solvers; see [of] for the parameters. */
    @JvmStatic
    @JvmOverloads
    fun prolog(
        libraries: List<Library> = defaultLibraries,
        dynamicKb: Theory = Theory.empty(),
        unificator: Unificator? = null,
        builtins: Boolean = true,
    ): SolverProfile = of(PrologSolverFactory, PROLOG_ID, "Prolog", libraries, dynamicKb, unificator, builtins)

    /** A profile of ProbLog solvers, solving probabilistically; see [of] for the parameters. */
    @JvmStatic
    @JvmOverloads
    fun problog(
        libraries: List<Library> = defaultLibraries,
        dynamicKb: Theory = Theory.empty(),
        unificator: Unificator? = null,
        builtins: Boolean = true,
    ): SolverProfile =
        of(ProblogSolverFactory, PROBLOG_ID, "ProbLog", libraries, dynamicKb, unificator, builtins, probabilistic = true)
}

/** A [SolverFactory] whose builders start with the given dynamic knowledge base, unificator and standard library. */
private class ConfiguredSolverFactory(
    private val delegate: SolverFactory,
    private val dynamicKb: Theory,
    private val unificator: Unificator?,
    private val builtins: Boolean,
) : SolverFactory by delegate {
    override fun newBuilder(): SolverBuilder {
        var builder = delegate.newBuilder().dynamicKb(dynamicKb)
        if (unificator != null) builder = builder.unificator(unificator)
        if (!builtins) builder = builder.noBuiltins()
        return builder
    }
}

/** A session solving every query probabilistically (2P-Kt's own, in gui-plp, is internal). */
private class ProbabilisticSession(
    factory: SolverFactory,
    creationRequest: SolverSessionCreationRequest,
    capabilities: Set<String>,
    solutionFeatures: (Solution) -> Map<FeatureId, Map<String, FeatureValue>>,
    runtimeLibraries: List<Library>,
) : SolverFactorySession(factory, creationRequest, capabilities, solutionFeatures, runtimeLibraries) {
    override fun configureSolveOptions(options: SolveOptions): SolveOptions = options.setProbabilistic(true)
}
