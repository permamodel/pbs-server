from setuptools import setup, find_packages
from pbs_server import __version__


setup(name='pbs-server',
      version=__version__,
      author='Mark Piper',
      author_email='mark.piper@colorado.edu',
      license='Apache',
      url='http://github.com/permamodel/pbs-server',
      description='The Permafrost Benchmark System server',
      long_description=open('README.md').read(),
      install_requires=[
          'pyyaml',
          'netCDF4',
      ],
      packages=find_packages(exclude=['*.tests']),
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=[
          'nose',
          'numpy',
      ],
      keywords='PBS permafrost model benchmark ILAMB',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
)
