#!/usr/bin/env python

from distutils.core import setup

DEPENDENCIES = [
      "paramiko",
      "requests",
      "sqlalchemy",
      "sqlalchemy_utils",
      "ssdp",
      "werkzeug=='0.16.1'",
      "flask",
      "flask-restplus",
      "git+https://github.com/myronww/automationkit.git"
]

DEPENDENCY_LINKS = []

setup(name='akit',
      version='1.0',
      description='Automation Kit',
      author='Myron Walker',
      author_email='myron.walker@automationmojo.com',
      url='https://automationmojo.com/products/akit',
      packages=["packages/sonos"],
      install_requires=DEPENDENCIES,
      dependency_links=DEPENDENCY_LINKS
     )
