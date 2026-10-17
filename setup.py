import platform
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


PACKAGE_NAME = 'tuprolog'
JAR_FOLDER = Path(PACKAGE_NAME, 'libs')
MAVEN_EXECUTABLE = ['mvn', '--batch-mode']


def is_windows():
    return platform.system() == 'Windows'


def run_maven(*args, cwd=None) -> (str, str):
    proc = subprocess.Popen(
        MAVEN_EXECUTABLE + list(args),
        shell=is_windows(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'Error while running mvn:\n{stdout}\n{stderr}')
    return stdout, stderr


def download_jars():
    stdout, _ = run_maven('-v')
    if 'Apache Maven' not in stdout:
        raise RuntimeError(f'Could not find Apache Maven in {stdout}')
    run_maven(
        'dependency:copy-dependencies',
        f'-DoutputDirectory={JAR_FOLDER}',
        cwd=Path(__file__).parent
    )
    # run_maven(
    #     'dependency:copy-dependencies',
    #     f'-DoutputDirectory={JAR_FOLDER}',
    #     '-Dclassifier=javadoc',
    #     cwd=Path(__file__).parent
    # )


class BuildPyCommand(build_py):
    def run(self):
        download_jars()
        super().run()


setup(
    cmdclass={
        'build_py': BuildPyCommand,
    }
)
