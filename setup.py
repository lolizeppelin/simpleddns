#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

__version__ = "1.0.0"

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from distutils.core import setup


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = f.read()
f.close()

setup(
    # oslo_cfg 要求 netaddr!=0.7.16,>=0.7.12 # BSD
    # kombu>=3.0.25否则timeout参数有问题
    install_requires=('netaddr>=0.7.5',
                      'psutil>=5.0',
                      'requests>=2.2',
                      'six>=1.9.0'),
    name='simpleddns',
    version=__version__,
    description='a simple ddns util',
    long_description=long_description,
    url='http://github.com/lolizeppelin/simpleddns',
    author='Lolizeppelin',
    author_email='lolizeppelin@gmail.com',
    maintainer='Lolizeppelin',
    maintainer_email='lolizeppelin@gmail.com',
    keywords=['simpleddns'],
    license='MIT',
    packages=find_packages(include=['simpleddns*']),
    # tests_require=['pytest>=2.5.0'],
    # cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
