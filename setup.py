#!/usr/bin/env python

from setuptools import setup, find_packages
import os


base_dir = os.path.dirname(os.path.abspath(__file__))

setup(name='search-api',
    version='1.0.0',
    description='Search API',
    author='Jonathon Scanes',
    author_email='me@jscanes.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'pyyaml',
        'pika',
        'elasticsearch',
        'requests',
        'tornado',
        'pymongo',
    ],
    package_data={
        '': ['*.yaml']
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': [
            'search = search.main:main'
        ]
    }
)
