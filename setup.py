#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_f:
    README = readme_f.read()

with open('requirements.txt') as requirements_f:
    REQUIREMENTS = requirements_f.readlines()

with open('tests/requirements.txt') as test_requirements_f:
    TEST_REQUIREMENTS = test_requirements_f.readlines()

setup(
    name='aur',
    version='0.9.2',
    description='Arch User Repository API interface.',
    long_description=README,
    author='Chris Down',
    author_email='chris@chrisdown.name',
    url='https://github.com/cdown/aur',
    packages=['aur'],
    license='ISC',
    zip_safe=False,
    keywords='aur arch linux',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS
)
