from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='dnetlib',
      version='0.11.4',
      description='dnet internal library',
      url='http://repo.dwp.io/sadnet/engineering-library.git',
      author='dnet',
      author_email='sa@dwp.co.id',
      license='DNET License',
      packages=find_packages(),
      zip_safe=False)
