from setuptools import *

with open("README.md", mode='r') as file:
    text=file.read()

setup(
    name='pyautoupdate',
    version='0.0.1.dev0',
    packages=find_packages(),
    description='Interface to allow python programs to automatically update',
    long_description=text,
    url='https://github.com/rlee287/pyautoupdate'
    install_requires=['requests>=2.6'],
    package_data={
       '':['*.txt','*.ini','*.md'],
       'testing':['*.md']},
    license="LGPL 2.1"
)
