import os
import jdk
import platform
from pathlib import Path

JAVA_HOME = Path(__file__).parent / 'java'

CLASSPATH = Path(__file__).parent

if platform.system() == 'Windows':
    JAVA_PATH = JAVA_HOME / 'bin' / 'server' / 'jvm.dll'
elif platform.system() == 'Darwin':
    JAVA_PATH = JAVA_HOME / 'lib' / 'libjli.dylib'
elif platform.system() == 'Linux':
    JAVA_PATH = JAVA_HOME / 'lib' / 'server' / 'libjvm.so'
else:
    raise RuntimeError("Unsupported platform: " + platform.system())

def install_java_if_missing() -> Path:
    if JAVA_HOME.exists():
        return
    java_version = os.getenv('JAVA_VERSION', '11')
    destination_folder = str(CLASSPATH)
    installation_path = Path(jdk.install(java_version, jre=not java_version.startswith('16'), path=destination_folder))
    destination_folder = JAVA_HOME
    installation_path = installation_path.rename(destination_folder)
    def list_files(startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
    list_files(str(installation_path))
