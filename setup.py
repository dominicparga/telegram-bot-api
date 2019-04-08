#!/usr/bin/env python

'''
Setup script for telegram-python project.
'''

from setuptools import setup

setup(
    name='telegram',
    version='0.1',
    description='Telegram Bot API wrapper',
    url='https://github.com/dominicparga/telegram-python',
    author='Dominic Parga Cacheiro',
    author_email='dominic.parga@gmail.com',
    license='Apache-2.0',
    packages=['telegram'],
    zip_safe=False,
    install_requires=[
        'requests'
    ]
)
