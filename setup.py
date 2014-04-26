# -*- coding: utf-8 -*-

from setuptools import setup

version = '0.1'

setup(name='btsync-cli',
      version=version,
      description="CLI interface for btsync",
      long_description=open('README.rst').read(),
      keywords='btsync',
      author='Ryon Bounds',
      author_email='',
      url='https://github.com/rbounds/btsync-cli',
      license='MIT',
      py_modules=['btsyncli'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'btsync.py',
          'blessings',
      ],
      entry_points={
          'console_scripts': [
              'btsyncli= btsyncli:main',
              ]
          }
      )
