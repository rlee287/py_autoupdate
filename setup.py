from setuptools import *

setup(
    name='py_autoupdate',
    version='0.0.1.dev0',
    packages=find_packages(),
    install_requires=['requests>=2.6']
    package_data={
       '':['*.txt','*.ini','*.md']
       'testing':['*.md']
    license="LGPL 2.1"
)
