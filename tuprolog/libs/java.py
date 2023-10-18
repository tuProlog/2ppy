import sys
from pathlib import Path
from jdk4py import JAVA_HOME


CLASSPATH = Path(__file__).parent


def __jvm_lib_file_names():
    if sys.platform == "win32":
        return {"jvm.dll"}
    elif sys.platform == "darwin":
        return {"libjli.dylib"}
    else:
        return {"libjvm.so"}


def __jvmlib():
    for name in __jvm_lib_file_names():
        for path in JAVA_HOME.glob(f"**/{name}"):
            path.resolve()
            if path.exists:
                return path
    return None


def find_jvm() -> Path:
    jvm = __jvmlib()
    if jvm is None:
        raise FileNotFoundError("Could not find jvm executable.")
    return jvm
