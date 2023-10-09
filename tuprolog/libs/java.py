import os
import jdk
import shutil
import logging
from pathlib import Path

JAVA_HOME = Path(__file__).parent / 'java'

CLASSPATH = Path(__file__).parent

logger = logging.getLogger('tuprolog')

def install_java_if_missing() -> Path:
    if JAVA_HOME.exists():
        return
    java_version = os.getenv('JAVA_VERSION', '11')
    destination_folder = str(CLASSPATH)
    logger.info(f'Downloading Java {java_version} in {destination_folder}')
    installation_path = Path(jdk.install(java_version, jre=not java_version.startswith('16'), path=destination_folder)) # Java 16 doesn't have a JRE
    destination_folder = JAVA_HOME
    logger.info(f'Installing Java {java_version} in {destination_folder}')
    shutil.copytree(installation_path, destination_folder, dirs_exist_ok=True)
    shutil.rmtree(installation_path, ignore_errors=True)
