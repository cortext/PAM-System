# -*- coding: utf-8 -*-

# Learn more: https://github.com/cortext/cib

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Corporate Invention Board',
    version='0.1',
    description='Project for building corporate invention board',
    long_description=open('README.rst').read(),
    license='LGPL',
    author='Juan Pablo O',
    author_email='juanpablospinadelgado@esiee.fr',
    url='https://github.com/cortext/pam',
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
          'console_scripts': [
              'pam = pam.__main__:_main'
          ]
    },
	classifiers = (
		'Natural Language :: English',
		'Programming Language :: Python',
		)
)

