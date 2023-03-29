import os
import jdk
from urllib import request
from pathlib import Path
from setuptools import setup
from xml.etree import ElementTree
from setuptools.command.build_py import build_py


def java_dependencies() -> list[tuple[str, str, str]]:
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


JAR_FOLDER = Path('tuprolog', 'libs')
JAVA_FOLDER = JAR_FOLDER / 'java'


def download_jars():
    for group_id, artifact_id, version in java_dependencies():
        jar_name = f'{artifact_id}-{version}.jar'
        jar_path = JAR_FOLDER / jar_name
        if not jar_path.exists():
            url = f'https://repo1.maven.org/maven2/{group_id.replace(".", "/")}/{artifact_id}/{version}/{jar_name}'
            print(f'Downloading {jar_name} from {url}')
            response = request.urlopen(url)
            data = response.read()
            jar_path.write_bytes(data)
        else:
            print(f'{jar_name} already exists')


class BuildPyCommand(build_py):
    def run(self):
        download_jars()
        super().run()


def install_java():
    if JAVA_FOLDER.exists():
        print('Java already installed')
        return
    installation_path = Path(jdk.install('11', jre=True, path=str(JAR_FOLDER)))
    installation_path.rename(JAVA_FOLDER)
    print(f'Installed Java in {installation_path}')


install_java()
setup(
    cmdclass={
        'build_py': BuildPyCommand
    }
)
