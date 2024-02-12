# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import os

from setuptools import setup, find_namespace_packages

name = 'OpenAlea.Strawberry'
version = '1.2.0'

description = "Strawberry is a package for architecture analysis and 2D/3D reconstruction."
long_description = open('README.md').read()

authors="Marc Labadie, Christophe Pradal, Gaetan Heidsieck"
authors_email="marc.labadie@cirad.fr, christophe.pradal@cirad.fr"

url = "https://github.com/openalea/strawberry"

license = 'cecill-c'
# dependencies to other eggs
setup_requires = ['openalea.deploy']

# find packages
packages=find_namespace_packages(where='src', include=['openalea.*'])
package_dir={'': 'src'}

setup(
    name=name,
    version=version,

    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords='strawberry, architecture, FSPM, openalea',

    # package installation
    packages=packages,
    package_dir=package_dir,

    share_dirs={'share': 'share'},

    # Namespace packages creation by deploy
    #namespace_packages=['openalea'],
    zip_safe=False,

    # Dependencies
    setup_requires=setup_requires,

    include_package_data=True,

    # (you can provide an exclusion dictionary named exclude_package_data to remove parasites).
    # alternatively to global inclusion, list the file to include
    package_data={'': ['*.csv', '*.mtg', '*.R*', '*.ipynb']},

    # Declare scripts and wralea as entry_points (extensions) of your package
    entry_points={
        'wralea': ['strawberry = openalea.strawberry_wralea'],
        'console_scripts': [
            'strawberry = openalea.strawberry.application.run:main'  # Define a console script to run your Voilà app
        ]
        },
    )
