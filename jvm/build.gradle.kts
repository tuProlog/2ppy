import org.jetbrains.kotlin.gradle.dsl.JvmTarget

/*
 * The JVM side of 2PPy: 2P-Kt's artifacts, plus the adapters making them usable from Python
 * (src/main/kotlin), without changing 2P-Kt itself. `installJars` copies the adapters' JAR and
 * their runtime classpath into tuprolog/libs/, where `tuprolog` puts them on the JVM's classpath.
 */

plugins {
    alias(libs.plugins.kotlin.jvm)
}

// the lowest JVM release 2P-Kt targets (jdk4py ships a newer one)
val jvmRelease = 17

kotlin {
    compilerOptions {
        jvmTarget = JvmTarget.fromTarget(jvmRelease.toString())
        allWarningsAsErrors = true
    }
}

java {
    sourceCompatibility = JavaVersion.toVersion(jvmRelease)
    targetCompatibility = JavaVersion.toVersion(jvmRelease)
}

tasks.withType<JavaCompile>().configureEach {
    options.release = jvmRelease
}

configurations.configureEach {
    // metadata-only artifact, unpublished for recent Kotlin versions (tuProlog/2p-kt#859)
    exclude(group = "org.jetbrains.kotlin", module = "kotlin-stdlib-common")
}

dependencies {
    api(libs.tuprolog.repl)
    api(libs.tuprolog.solve.prolog)
    api(libs.tuprolog.solve.problog)
    api(libs.tuprolog.gui)
    api(libs.tuprolog.gui.plp)
    testImplementation(platform(libs.junit.bom))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
}

val installJars by tasks.registering(Sync::class) {
    group = "build"
    description = "Copies the adapters' JAR and their runtime classpath into tuprolog/libs/."
    from(tasks.jar)
    from(configurations.runtimeClasspath)
    into(layout.projectDirectory.dir("../tuprolog/libs"))
    preserve {
        // the Python sources of tuprolog.libs live next to the JARs
        include("*.py", "__pycache__/**")
    }
}

tasks.assemble {
    dependsOn(installJars)
}
