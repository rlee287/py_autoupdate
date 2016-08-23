from setuptools import setup, find_packages

import re

with open("README.rst", mode='r') as readme_file:
    text=readme_file.read()

#below version code pulled from requests module
with open('__init__.py', 'r') as fd:
    version_number = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                               fd.read(), re.MULTILINE).group(1)
if not version_number:
    raise RuntimeError('Cannot find version information')

setup(
    name='pyautoupdate',
    version=version_number,
    packages=find_packages(),
    description='Interface to allow python programs to automatically update',
    long_description=text,
    url='https://github.com/rlee287/pyautoupdate',
    classifiers=(
        'Intended Audience :: Developers'
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)'
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    install_requires=['requests'],
    extras_require={
        'testing': ['pytest','coverage']
    },
    package_data={
        'testing':['*.rst']},
    license="LGPL 2.1"
)
