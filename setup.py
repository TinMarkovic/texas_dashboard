import os
from setuptools import setup
from setuptools import find_packages

README = open(os.path.join(os.path.dirname(__file__), 'readme.md')).read()
REQUIREMENTS = [line.strip() for line in
                open("requirements.txt").readlines()]

setup(name='texas-dashboard',
      version='0.1',
      description='Dashboard django backend for Texas OnCourse project',
      long_description=README,
      install_requires=REQUIREMENTS,
      url='https://github.com/TinMarkovic/texas_dashboard',
      author='ExtensionEngine',
      author_email='tmarkovic@extensionengine.com',
      license='',
      packages=find_packages())
