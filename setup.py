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
    install_requires=['requests'],
    extras_require={
        'testing': ['pytest','coverage']
    },
    package_data={
        'testing':['*.rst']},
    license="LGPL 2.1"
)
