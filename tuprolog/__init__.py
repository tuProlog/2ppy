import os
import logging
import jpype

from .libs import JAVA_HOME, CLASSPATH, install_java_if_missing

# Override the JAVA_HOME environment variable to use the locally installed JDK
os.environ['JAVA_HOME'] = str(JAVA_HOME)

logger = logging.getLogger('tuprolog')

jars = [str(j.resolve()) for j in CLASSPATH.glob('*.jar')]

if not jpype.isJVMStarted():
    install_java_if_missing()
    jpype.startJVM(classpath=jars)

import jpype.imports
from it.unibo import tuprolog as _tuprolog # type: ignore

Info = _tuprolog.Info

JVM_VERSION = '.'.join(map(str, jpype.getJVMVersion()))

logger.info("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

logger.info("Using 2P-Kt v" + str(Info.VERSION))
