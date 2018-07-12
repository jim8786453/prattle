#!/usr/bin/env python
import os
import platform

from setuptools import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

req_file = 'requirements.txt'
install_reqs = parse_requirements(req_file, session=False)
reqs = [str(ir.req) for ir in install_reqs]
del os.link

setup(
    author='Jim Kennedy',
    author_email='jim8786453@gmail.com',
    description='Demo messaging api',
    install_requires=reqs,
    name='prattle',
    packages=['prattle'],
    version='0.0.1',
)
