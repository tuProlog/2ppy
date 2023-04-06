import os
import jdk
from pathlib import Path
import platform

JAVA_HOME = Path(__file__).parent / 'java'

CLASSPATH = Path(__file__).parent

if platform.system() == 'Windows':
    JAVA_PATH = JAVA_HOME / 'bin' / 'server' / 'jvm.dll'
elif platform.system() == 'Darwin':
    JAVA_PATH = JAVA_HOME / 'lib' / 'server' / 'libjvm.dylib'
else:
    JAVA_PATH = JAVA_HOME / 'lib' / 'server' / 'libjvm.so'    

def install_java_if_missing() -> Path:
    if JAVA_HOME.exists():
        return
    java_version = os.getenv('JAVA_VERSION', '11')
    destination_folder = str(CLASSPATH)
    installation_path = Path(jdk.install(java_version, jre=not java_version.startswith('16'), path=destination_folder))
    destination_folder = JAVA_HOME
    installation_path = installation_path.rename(destination_folder)
