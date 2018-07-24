import os
from stat import ST_MODE
from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils import log
from pbs_server import __version__


class InstallWithPermissions(install):
    """An installer that modifies permissions on package data files.

    See https://stackoverflow.com/a/25761434.

    """
    def run(self):
        install.run(self)
        fmode = 0666
        dmode = 0777
        for filepath in self.get_outputs():
            if filepath.endswith('.cfg.tmpl'):
                log.info('Changing permissions of %s to %s' %
                         (filepath, oct(fmode)))
                os.chmod(filepath, fmode)
                data_dir = os.path.dirname(filepath)
                if oct(os.stat(data_dir)[ST_MODE])[-3:] != str(dmode):
                    log.info('Changing permissions of %s to %s' %
                             (data_dir, oct(dmode)))
                    os.chmod(data_dir, dmode)


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
      cmdclass={'install': InstallWithPermissions},
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
