# -*- coding: utf-8 -*-

import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='meio_pagamento-koin',
    version='develop',
    url='https://github.com/lojaintegrada/meio_pagamento-koin',
    license='MIT',
    description='Meio de pagamento usando o Koin (http://www.koin.com.br/)',
    author=u'Loja Integrada',
    author_email='suporte@lojaintegrada.com.br',
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        ],
    packages=['meio_pagamento'],
    install_requires=['distribute'],
)