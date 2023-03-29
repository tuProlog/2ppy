from setuptools import setup
from xml.etree import ElementTree

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

setup()
