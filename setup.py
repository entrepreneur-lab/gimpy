#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 14:04:10 2021

@author: martin
"""

from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name = "gimpy",
      version = 0.9,
      py_modules = ['gimpy'],
      url = "https://github.com/kynnemall/gimpy",
      description = "GUI app to annotate images by filename",
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      author = "Martin Kenny",
      author_email = "sideproject1892@gmail.com",
      maintainer = "Martin Kenny",
      maintainer_email = "sideproject1892@gmail.com",
      packages = find_packages(),
      entry_points = {
                      'gui_scripts': ['gimpy=gimpy:main']
                      },
      python_requires = ">=3.6",
      install_requires = [
          "matplotlib",
          "scikit-image",
          ],
      classifiers = [
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          ],
      )
