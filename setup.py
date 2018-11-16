#!/usr/bin/env python3
# Copyright (c) 2018 atlarge-research
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os.path
import setuptools

__version__ = '1.0.0'
__dir__ = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(__dir__, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='jsspp-osp',
    version=__version__,
    author='@Large Research',
    author_email='info@atlarge-research.com',
    license='MIT',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'jsspp-osp=jsspp.osp.cli:main',
        ]
    },
    install_requires=[
        'jsonschema==3.0.0a3'
    ],
    include_package_data=True,
    zip_safe=False, # Zipped eggs don't play nicely with namespace packaging
    description='Tooling and documentation of of the formats used for Open Scheduling Problems (OSPs) of JSSPP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/atlarge-research/jsspp-osp'
)
