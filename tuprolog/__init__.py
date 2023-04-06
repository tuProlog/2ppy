import platform
import logging
# noinspection PyUnresolvedReferences
import jpype
import jpype.imports

from .libs import JAVA_HOME, CLASSPATH, install_java_if_missing

if platform.system() == 'Windows':
    jvmpath = JAVA_HOME / 'bin' / 'server' / 'jvm.dll'
else:
    jvmpath = JAVA_HOME / 'lib' / 'server' / 'libjvm.so'

logger = logging.getLogger('tuprolog')

jars = [str(j.resolve()) for j in CLASSPATH.glob('*.jar')]

if not jpype.isJVMStarted():
    install_java_if_missing()
    jpype.startJVM(jvmpath=str(jvmpath), classpath=jars)

# noinspection PyUnresolvedReferences
from it.unibo import tuprolog as _tuprolog

Info = _tuprolog.Info

JVM_VERSION = '.'.join(map(str, jpype.getJVMVersion()))

logger.info("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

logger.info("Using 2P-Kt v" + str(Info.VERSION))
