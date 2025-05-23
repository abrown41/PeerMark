from os import path
from setuptools import setup, find_packages
import sys
import versioneer


# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (3, 7)
if sys.version_info < min_version:
    error = """
peermark does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(*(sys.version_info[:2] + min_version))
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]


setup(
    name='peermark',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Python package for building/grading Peer Marking Spreadsheets",
    long_description=readme,
    author="Andrew Brown",
    author_email='andrew.brown@qub.ac.uk',
    url='https://github.com/abrown41/PeerMark',
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    entry_points={
        'console_scripts': [
            'generate_peer = PeerMark.generate_peer_review:main',
            'extract_peer = PeerMark.extract_peer:main'
        ]
    },
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={
        "PeerMark": ["data/*.xlsx"],
    },
    install_requires=requirements,
    license="BSD (3-clause)",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
