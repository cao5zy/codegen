#!/usr/bin/env python
from setuptools import setup, find_packages
name = "codegen"

requires = []

setup(
    name = name,
    version = '0.0.1',
    scripts = ["scripts/codegen"]
    author = 'Zongying Cao',
    author_email = 'zongying.cao@dxc.com',
    description = 'codegen is a library for generating the infrastructure code of microservices.',
    long_description = """nodejs-codegen is a library for generating the infrastructure code of microservices.""",
    packages = [name],
    package_dir = {'codegen': 'code'},
    package_data = {'codegen': ["*.py"]},
    include_package_data = True,
    install_requires = requires,
    license = 'Apache',
    classifiers = [
               'Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: Apache Software License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries',
           ],
)
