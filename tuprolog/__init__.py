import logging
from importlib.metadata import version

import jpype

from .libs import CLASSPATH, find_jvm

__version__ = version("2ppy")  # pyproject.toml is the only source

logger = logging.getLogger("tuprolog")

jars = [str(j.resolve()) for j in CLASSPATH.glob("*.jar")]

if not jpype.isJVMStarted():
    jpype.startJVM("--enable-native-access=ALL-UNNAMED", classpath=jars, jvmpath=str(find_jvm()))

import jpype.imports
from it.unibo import tuprolog as _tuprolog  # type: ignore

Info = _tuprolog.Info

JVM_VERSION = ".".join(map(str, jpype.getJVMVersion()))

logger.info("Started JVM v" + JVM_VERSION + " with classpath: " + str(jars))

logger.info("Using 2P-Kt v" + str(Info.VERSION))

from . import errors
