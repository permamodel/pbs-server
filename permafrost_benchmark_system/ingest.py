"""Perform ingest operations in PBS."""

import os
import shutil
import yaml
from .file import IngestFile, Logger
from .verify import VerificationTool, VerificationError


file_exists = '''## File Exists\n
The file `{1}/{0}` already exists in the PBS data store.
The file has not been updated.
'''
file_moved = '''## File Moved\n
The file `{}` has been moved to `{}` in the PBS data store.
'''
file_not_verified = '''## File Verification Error\n
The file `{}` cannot be ingested into the PBS data store.
Error message:\n
{}
'''


class ModelIngestTool(object):
    """
    Tool for uploading CMIP5-compatible model outputs into PBS.

    Parameters
    ----------
    ingest_file : str, optional
      Path to the configuration file (default is None).

    Attributes
    ----------
    ilamb_root : str
      Path to the ILAMB root directory.
    dest_dir : str
      Directory relative to ILAMB_ROOT where model outputs are stored.
    ingest_files : list
      List of files to ingest.
    make_public : bool
      Set to True to allow others to see and use ingested files.

    """
    def __init__(self, ingest_file=None):
        self.ilamb_root = None
        self.dest_dir = None
        self.ingest_files = []
        self.make_public = True
        self.log = Logger(title='Model Ingest Tool Summary')
        if ingest_file is not None:
            self.load(ingest_file)

    def load(self, ingest_file):
        """
        Read and parse the contents of a configuration file.

        Parameters
        ----------
        ingest_file : str
          Path to the configuration file.

        """
        with open(ingest_file, 'r') as fp:
            cfg = yaml.safe_load(fp)
        self.ilamb_root = cfg['ilamb_root']
        self.dest_dir = cfg['dest_dir']
        for f in cfg['ingest_files']:
            self.ingest_files.append(IngestFile(f))
        self.make_public = cfg['make_public']

    def verify(self):
        """
        Check whether ingest files use the CMIP5 standard format.
        """
        for f in self.ingest_files:
            v = VerificationTool(f)
            try:
                v.verify()
            except VerificationError as e:
                msg = file_not_verified.format(f.name, e.msg)
                self.log.add(msg)
                if os.path.exists(f.name):
                    os.remove(f.name)
            else:
                f.data = v.model_name
                f.is_verified = True

    def move(self):
        """
        Move ingest files to the ILAMB MODELS directory.

        Notes
        -----
        A file that is moved is replaced with a text file listing the
        new location of the file. If the file exists in the target
        location, the file is replaced with a text file stating that
        the file was not moved.

        """
        models_dir = os.path.join(self.ilamb_root, self.dest_dir)
        for f in self.ingest_files:
            if f.is_verified:
                msg = file_moved.format(f.name, models_dir)
                try:
                    shutil.move(f.name, models_dir)
                except:
                    msg = file_exists.format(f.name, models_dir)
                    if os.path.exists(f.name):
                        os.remove(f.name)
                finally:
                    self.log.add(msg)


class BenchmarkIngestTool(object):

    """Tool for uploading benchmark datasets into PBS."""

    def __init__(self):
        pass
