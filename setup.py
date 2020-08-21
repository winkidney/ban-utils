#!/usr/bin/env python
import os
from setuptools import setup, find_packages

project_root = os.path.abspath(os.path.dirname(__file__))

long_description = """
django-banish is a django middleware app to banish user agents by IP addresses or User Agent Header.
It also supports basic abuse prevention by automatically banning users
if they exceed a certain number of requests per minute
which is likely some form of attack or attemped denial of service.
"""

install_requires = (
    "redis",
)

setup(
    name='ban-utils',
    version="0.0.1",
    install_requires=install_requires,
    description="django middleware to ban users, prevent too many concurrent connections",
    long_description=long_description,
    author="winkidney",
    author_email="winidney@gmail.com",
    url="https://github.com/winkidney/banish-utils",
    packages=find_packages(project_root),
    license='BSD',
    platforms='Posix; MacOS X;',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
