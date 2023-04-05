import os
import logging
# noinspection PyUnresolvedReferences
import jpype
import jpype.imports

from .libs import JAVA_HOME, CLASSPATH
os.environ['JAVA_HOME'] = str(JAVA_HOME)

logger = logging.getLogger('tuprolog')

jars = [str(j.resolve()) for j in CLASSPATH.glob('*.jar')]

if not jpype.isJVMStarted():
    jpype.startJVM(classpath=jars)

# noinspection PyUnresolvedReferences
from it.unibo import tuprolog as _tuprolog

Info = _tuprolog.Info

JVM_VERSION = '.'.join(map(str, jpype.getJVMVersion()))

logger.info("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

logger.info("Using 2P-Kt v" + str(Info.VERSION))
