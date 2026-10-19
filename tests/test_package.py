"""Tests for the `tuprolog` package itself (`__init__.py`) and `tuprolog.libs`."""

import logging
import re
from importlib.metadata import version
from pathlib import Path

import jpype
import pytest

import tuprolog
from tuprolog import libs
from tuprolog.libs import java

VERSIONS = Path(__file__).parent.parent / "jvm" / "gradle" / "libs.versions.toml"


def test_version_comes_from_package_metadata():
    assert tuprolog.__version__ == version("2ppy")
    assert re.match(r"^\d+\.\d+\.\d+", tuprolog.__version__)


def test_logger():
    assert isinstance(tuprolog.logger, logging.Logger)
    assert tuprolog.logger.name == "tuprolog"


def test_jvm_is_started():
    assert jpype.isJVMStarted()
    assert tuprolog.JVM_VERSION == ".".join(map(str, jpype.getJVMVersion()))


def test_jars_are_on_the_classpath():
    assert len(tuprolog.jars) > 0
    for jar in tuprolog.jars:
        assert Path(jar).is_file()
        assert Path(jar).suffix == ".jar"
        assert Path(jar).parent == libs.CLASSPATH.resolve()


def test_info_matches_the_declared_version():
    assert isinstance(tuprolog.Info, jpype.JClass)
    expected = re.search(r'^tuprolog = "([^"]+)"', VERSIONS.read_text(), re.MULTILINE)
    assert expected is not None
    assert str(tuprolog.Info.VERSION) == expected.group(1)


def test_libs_reexports():
    assert libs.CLASSPATH == java.CLASSPATH
    assert libs.JAVA_HOME == java.JAVA_HOME
    assert libs.find_jvm is java.find_jvm


def test_classpath_is_the_libs_directory():
    assert libs.CLASSPATH == Path(java.__file__).parent
    assert libs.CLASSPATH.is_dir()


def test_find_jvm():
    jvm = libs.find_jvm()
    assert jvm.exists()
    assert jvm.name in java.__jvm_lib_file_names()


@pytest.mark.parametrize(
    "platform, name",
    [("win32", "jvm.dll"), ("darwin", "libjli.dylib"), ("linux", "libjvm.so")],
)
def test_jvm_lib_file_names(monkeypatch, platform, name):
    monkeypatch.setattr(java.sys, "platform", platform)
    assert java.__jvm_lib_file_names() == {name}


def test_find_jvm_without_jvm(monkeypatch, tmp_path):
    monkeypatch.setattr(java, "JAVA_HOME", tmp_path)
    with pytest.raises(FileNotFoundError):
        java.find_jvm()


def test_find_jvm_in_nested_directory(monkeypatch, tmp_path):
    (name,) = java.__jvm_lib_file_names()
    lib = tmp_path / "lib" / "server" / name
    lib.parent.mkdir(parents=True)
    lib.touch()
    monkeypatch.setattr(java, "JAVA_HOME", tmp_path)
    assert java.find_jvm() == lib


def test_find_jvm_ignores_broken_links(monkeypatch, tmp_path):
    (name,) = java.__jvm_lib_file_names()
    (tmp_path / name).symlink_to(tmp_path / "missing")
    monkeypatch.setattr(java, "JAVA_HOME", tmp_path)
    with pytest.raises(FileNotFoundError):
        java.find_jvm()
