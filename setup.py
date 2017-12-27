from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='pycWiki',
      version='0.1.0',
      description='Library to communicate wiki mediawiki APi',
      url='https://github.com/icesourceg/pycWiki',
      author='icesourceg',
      author_email='icesourceg@gmail.com',
      license='Public',
      packages=find_packages(),
      install_requires=[
          'simplejson', 
          'requests',
          'urllib2'
          'urllib',
          'ssl'
      ],
      zip_safe=False)
