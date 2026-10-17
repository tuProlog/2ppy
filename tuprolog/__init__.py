import os
import logging
import jpype
from .libs import CLASSPATH, find_jvm

logger = logging.getLogger('tuprolog')

jars = [str(j.resolve()) for j in CLASSPATH.glob('*.jar')]

if not jpype.isJVMStarted():
    jpype.startJVM(classpath=jars, jvmpath=str(find_jvm()))

import jpype.imports  # noqa: F401, E402
from it.unibo import tuprolog as _tuprolog  # type: ignore # noqa: E402

Info = _tuprolog.Info

JVM_VERSION = '.'.join(map(str, jpype.getJVMVersion()))

logger.info("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

logger.info("Using 2P-Kt v" + str(Info.VERSION))
