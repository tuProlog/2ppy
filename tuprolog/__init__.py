import logging

logging.basicConfig(level=logging.DEBUG)

import jpype
import jpype.imports

from .libs import CLASSPATH

jars = [str(j.resolve()) for j in CLASSPATH.glob('*.jar')]

jpype.startJVM(classpath = jars)

JVM_VERSION = '.'.join(map(str, jpype.getJVMVersion()))

logging.debug("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

from it.unibo.tuprolog import Info

logging.debug("Using 2P-Kt v" + str(Info.VERSION))
