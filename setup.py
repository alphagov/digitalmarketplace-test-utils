"""
Utilities for testing Digital Marketplace apps.
"""
import re
import ast
from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('dmtestutils/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='digitalmarketplace-test-utils',
    version=version,
    url='https://github.com/alphagov/digitalmarketplace-test-utils',
    license='MIT',
    author='GDS Developers',
    description=__doc__.strip().split('\n')[0],
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
