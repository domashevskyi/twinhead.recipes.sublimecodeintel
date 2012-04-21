#!/usr/bin/env python
from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


name = 'twinhead.recipes.sublimecodeintel'
entry_points = {'zc.buildout': ['default = %s:SublimeCodeIntel' % name]}


setup(
    name=name,
    description="Generates SublimeCodeInt configuration file with all necessary extra paths",
    long_description=(
                       read('README.txt')
                       + "\n\n" +
                       read('CHANGES.txt')
    ),
    version='0.1.0a',
    author="Dmitriy Domashevskiy",
    author_email="dmitriy.domashevskiy@gmail.com",
    license="BSD",
    keywords="buildout recipe Sublime",
    url='https://github.com/domashevskiy/twinhead.recipes.sublimecodeintel',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['twinhead', 'twinhead.recipes'],
    install_requires=['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        'simplejson'
                        ],
    entry_points=entry_points,
    zip_safe=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Build Tools",
        ]
    )
