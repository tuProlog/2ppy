import os
import jdk
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


JAR_FOLDER = Path('tuprolog', 'libs')
JAVA_FOLDER = JAR_FOLDER / 'java'


def download_jars():
    proc = subprocess.Popen(['mvn.cmd' , '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Could not run mvn.cmd: {stderr}')
    if 'Apache Maven' not in stdout:
        raise RuntimeError(f'Could not find Apache Maven in {stdout}')
    print('Downloading JARs...')
    proc = subprocess.Popen(['mvn.cmd', 'dependency:copy-dependencies', f'-DoutputDirectory="{JAR_FOLDER}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Error while downloading JARs: {stdout} {stderr}')


class BuildPyCommand(build_py):
    def run(self):
        download_jars()
        super().run()


def install_java():
    if JAVA_FOLDER.exists():
        print('Java already installed')
        return
    java_version = os.getenv('JAVA_VERSION', '11')
    print(f'Installing Java {java_version}...')
    installation_path = Path(jdk.install(java_version), jre=True, path=str(JAR_FOLDER))
    installation_path = installation_path.rename(JAVA_FOLDER)
    print(f'Installed Java in {installation_path}')


install_java()
setup(
    cmdclass={
        'build_py': BuildPyCommand
    }
)
