import logging

logging.basicConfig(level=logging.DEBUG)

import jpype
import jpype.imports

jpype.startJVM(classpath = ['libs/*'])

logging.debug("Started JVM v" + '.'.join(map(str, jpype.getJVMVersion())))

from .jvmutils import jiterable, jiterator

from it.unibo.tuprolog import Info

logging.debug("Using 2P-Kt v" + str(Info.VERSION))
