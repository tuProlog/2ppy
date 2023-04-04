import os
import jdk
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


JAR_FOLDER = Path(__file__).parent / 'tuprolog' / 'libs'
JAVA_FOLDER = JAR_FOLDER / 'java'
MAVEN_EXECUTABLE = ['mvn', '--batch-mode']


def fallback_download_jars():
    print('Downloading JARs from GitHub...')
    def java_dependencies() -> list[tuple[str, str, str]]:
        from xml.etree import ElementTree
        namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
        tree = ElementTree.parse('pom.xml')
        root = tree.getroot()
        deps = root.find('xmlns:dependencies', namespaces)
        return [
            (dep.find('xmlns:groupId', namespaces).text,
                dep.find('xmlns:artifactId', namespaces).text,
                dep.find('xmlns:version', namespaces).text)
            for dep in deps
        ]
    from urllib.parse import quote
    _, _, version = java_dependencies()[0]
    all_in_one_jar = f'https://github.com/tuProlog/2p-kt/releases/download/{quote(version)}/2p-{version}-full.jar'
    print(f'Downloading {all_in_one_jar}')
    proc = subprocess.Popen(['curl', '--silent', '-L', all_in_one_jar, '--output', str(JAR_FOLDER / f'2p-{version}-full.jar')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Error while downloading JARs from GitHub: {stdout} {stderr}')


def download_jars():
    proc = subprocess.Popen(MAVEN_EXECUTABLE + ['-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Could not run mvn.cmd: {stderr}')
    if 'Apache Maven' not in stdout:
        raise RuntimeError(f'Could not find Apache Maven in {stdout}')
    print('Downloading JARs...')
    proc = subprocess.Popen(MAVEN_EXECUTABLE + ['dependency:copy-dependencies', f'-DoutputDirectory="{JAR_FOLDER}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Error while downloading JARs: {stdout} {stderr}')


class BuildPyCommand(build_py):
    def run(self):
        try:
            download_jars()
        except:
            print('Could not download JARs using Maven, falling back to GitHub')
            fallback_download_jars()
        super().run()


def install_java():
    if JAVA_FOLDER.exists():
        print('Java already installed')
        return
    java_version = os.getenv('JAVA_VERSION', '11')
    destination_folder = str(JAR_FOLDER.resolve())
    print(f'Downloading Java {java_version} in {destination_folder}...')
    installation_path = Path(jdk.install(java_version), jre=True, path=destination_folder)
    destination_folder = str(JAVA_FOLDER.resolve())
    print(f'Installing Java {java_version} in {destination_folder}...')
    installation_path = installation_path.rename(destination_folder)
    print(f'Installed Java in {installation_path}')


install_java()
setup(
    cmdclass={
        'build_py': BuildPyCommand
    }
)
