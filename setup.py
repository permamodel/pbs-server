from setuptools import setup, find_packages
from permafrost_benchmark_system import __version__


setup(name='permafrost-benchmark-system',
      version=__version__,
      author='Mark Piper',
      author_email='mark.piper@colorado.edu',
      license='Apache',
      url='http://github.com/permamodel/pbs',
      description='The Permafrost Benchmark System',
      long_description=open('README.md').read(),
      install_requires=[
          'pyyaml',
          'netCDF4',
          'basic-modeling-interface',
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
