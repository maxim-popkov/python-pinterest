#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="python-pinterest",
      version="0.0.2",
      description="Pinterest API client",
      license="MIT",
      install_requires=["requests"],
      url="http://github.com/maxim-popkov/python-pinterest",
      packages = find_packages(),
      keywords= "pinterest",
      zip_safe = True)
