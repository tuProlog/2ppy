import logging

# noinspection PyUnresolvedReferences
import jpype
import jpype.imports

from .libs import CLASSPATH

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('tuprolog')

jars = [str(j.resolve()) for j in CLASSPATH.glob('*.jar')]

jpype.startJVM(classpath=jars)

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog import Info

JVM_VERSION = '.'.join(map(str, jpype.getJVMVersion()))

logger.debug("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

logger.debug("Using 2P-Kt v" + str(Info.VERSION))
