
from setuptools import setup, find_packages
import pathlib
import subprocess

# current directory
here = pathlib.Path(__file__).parent.resolve()

version_file = here / 'VERSION'

print(f"Executing setup.py from {here}")

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

def format_git_describe_version(version):
    if '-' in version:
        splitted = version.split('-')
        tag = splitted[0]
        index = f"dev{splitted[1]}" #{hex(int(splitted[1]))[2:]}"
        # commit = splitted[2] 
        # return f"{tag}.{index}+{commit}"
        return f"{tag}.{index}"
    else:
        return version

def get_version_from_git():
    try:
        process = subprocess.run(["git", "describe"], cwd=str(here), check=True, capture_output=True)
        version = process.stdout.decode('utf-8').strip()
        version = format_git_describe_version(version)
        with version_file.open('w') as f:
            f.write(version)
        return version
    except subprocess.CalledProcessError:
        # with version_file.open('r') as f:
        return version_file.read_text().strip()

# version = os.popen('git describe').read().strip()
version = get_version_from_git()

print(f"Detected version {version} from git describe")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='2ppy',  # Required
    version=version,
    description='Python-based implementation of tuProlog -- the open ecosystem for symbolic AI --, based on 2P-Kt',
    license='Apache 2.0 License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tuProlog/2ppy', 
    author='Giovanni Ciatto', 
    author_email='giovanni.ciatto@unibo.it',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Prolog'
    ],
    keywords='prolog, symbolic ai, ecosystem, tuprolog, 2p, python',  # Optional
    # package_dir={'': 'src'},  # Optional
    packages=find_packages(),  # Required
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=['JPype1==1.3.0'],  # Optional
    zip_safe = False,
    platforms = "Independant",
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/tuProlog/2ppy/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/tuProlog/2ppy',
    },
)
