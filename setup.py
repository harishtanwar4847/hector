# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in hector/__init__.py
from hector import __version__ as version

setup(
	name='hector',
	version=version,
	description='Hector',
	author='Atrina Technologies Pvt Ltd',
	author_email='developers@atriina.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
