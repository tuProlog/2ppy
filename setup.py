import os
import platform
import jdk
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


JAR_FOLDER = Path('tuprolog', 'libs')
JAVA_FOLDER = JAR_FOLDER / 'java'
MAVEN_EXECUTABLE = ['mvn', '--batch-mode']


def is_windows():
    return platform.system() == 'Windows'


def download_jars():
    proc = subprocess.Popen(MAVEN_EXECUTABLE + ['-v'], shell=is_windows(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Could not run mvn:\n{stdout}\n{stderr}')
    if 'Apache Maven' not in stdout:
        raise RuntimeError(f'Could not find Apache Maven in {stdout}')
    proc = subprocess.Popen(MAVEN_EXECUTABLE + ['dependency:copy-dependencies', f'-DoutputDirectory={JAR_FOLDER}'], shell=is_windows(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=Path(__file__).parent)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Error while downloading JARs:\n{stdout}\n{stderr}')


class BuildPyCommand(build_py):
    def run(self):
        download_jars()
        super().run()


def install_java():
    if JAVA_FOLDER.exists():
        return
    java_version = os.getenv('JAVA_VERSION', '11')
    destination_folder = str(JAR_FOLDER)
    installation_path = Path(jdk.install(java_version, jre=not java_version.startswith('16'), path=destination_folder))
    destination_folder = JAVA_FOLDER
    installation_path = installation_path.rename(destination_folder)


install_java()
setup(
    cmdclass={
        'build_py': BuildPyCommand
    }
)
