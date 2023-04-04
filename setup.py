import os
import jdk
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


JAR_FOLDER = Path('tuprolog', 'libs')
JAVA_FOLDER = JAR_FOLDER / 'java'
MAVEN_EXECUTABLE = ['mvn', '--batch-mode']


def download_jars():
    print('Checking Maven...')
    proc = subprocess.Popen(args=MAVEN_EXECUTABLE + ['-v', 'help:help'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Could not run mvn:\n{stdout}\n{stderr}')
    if 'Apache Maven' not in stdout:
        raise RuntimeError(f'Could not find Apache Maven in {stdout}')
    print('Downloading JARs...')
    proc = subprocess.Popen(args=MAVEN_EXECUTABLE + ['dependency:copy-dependencies', f'-DoutputDirectory={JAR_FOLDER}'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=Path(__file__).parent)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Error while downloading JARs:\n{stdout}\n{stderr}')


class BuildPyCommand(build_py):
    def run(self):
        download_jars()
        super().run()


def install_java():
    if JAVA_FOLDER.exists():
        print('Java already installed')
        return
    java_version = os.getenv('JAVA_VERSION', '11')
    destination_folder = str(JAR_FOLDER)
    print(f'Downloading Java {java_version} in {destination_folder}...')
    installation_path = Path(jdk.install(java_version, jre=not java_version.startswith('16'), path=destination_folder))
    destination_folder = JAVA_FOLDER
    print(f'Installing Java in {destination_folder}...')
    installation_path = installation_path.rename(destination_folder)
    print(f'Installed Java in {installation_path}')


install_java()
setup(
    cmdclass={
        'build_py': BuildPyCommand
    }
)
