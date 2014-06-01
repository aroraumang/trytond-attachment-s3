#! /usr/bin/env python
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import re
import os
from setuptools import setup
import ConfigParser

requires = ['boto']


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

config = ConfigParser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        requires.append(
            'trytond_%s >= %s.%s, < %s.%s' % (
                dep, major_version, minor_version,
                major_version, minor_version + 1,
            )
        )
requires.append(
    'trytond >= %s.%s, < %s.%s' % (
        major_version, minor_version, major_version, minor_version + 1
    )
)

setup(
    name='trytond_attachment_s3',
    version=info.get('version', '0.0.1'),
    description=info.get('description', ''),
    long_description=read('README.md'),
    author='Openlabs Technologies & Consulting (P) Limited',
    author_email=info.get('email', ''),
    url=info.get('website', ''),
    package_dir={'trytond.modules.attachment_s3': '.'},
    packages=[
        'trytond.modules.attachment_s3',
        'trytond.modules.attachment_s3.tests',
    ],
    package_data={
        'trytond.modules.attachment_s3': info.get('xml', []) + [
            'tryton.cfg', 'locale/*.po', '*.odt', 'icons/*.svg'
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    license='BSD',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    attachment_s3 = trytond.modules.attachment_s3
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
)
