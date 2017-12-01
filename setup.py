import os
from setuptools import setup, find_packages


__version__ = '0.1.0'
__author__ = 'Takumi Sueda'
__author_email__ = 'puhitaku@gmail.com'
__license__ = 'MIT License'
__classifiers__ = (
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: User Interfaces')


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()


setup(
    name='naam',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/puhitaku/naam',
    description='Truly pythonic argument parser.',
    long_description=readme,
    classifiers=__classifiers__,
    packages=find_packages(),
    license=__license__,
    include_package_data=True)

