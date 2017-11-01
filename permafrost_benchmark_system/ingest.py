"""Perform ingest operations in PBS."""

import os
import shutil
import yaml
from .file import IngestFile


file_exists_msg = '''# File Exists\n
The file `{1}/{0}` already exists in the PBS data store.
The file has not been updated.
'''
file_moved_msg = '''# File Moved\n
The file `{}` has been moved to `{}` in the PBS data store.
'''


class ModelIngest(object):
    """
    Operator for uploading model outputs into PBS.

    Parameters
    ----------
    ingest_file : str, optional
      Path to the configuration file (default is None).
    models_dir : str, optional
      Path to the ILAMB MODELS directory (default is /nas/data/ilamb/MODELS).

    Attributes
    ----------
    models_dir : str
      Path to the ILAMB MODELS directory.
    ingest_files : list
      List of files to ingest.
    make_public : bool
      Set to True to allow others to see and use ingested files.

    """
    def __init__(self, ingest_file=None, models_dir='/nas/data/ilamb/MODELS'):
        self.models_dir = models_dir
        self.ingest_files = []
        self.make_public = True
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
        for f in cfg['ingest_files']:
            self.ingest_files.append(IngestFile(f))
        self.make_public = cfg['make_public']

    def validate(self):
        """
        Validate ingest files against the CMIP5 standard format.
        """
        for f in self.ingest_files:
            f.is_valid = True

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
        for f in self.ingest_files:
            if f.is_valid:
                msg = file_moved_msg.format(f.name, self.models_dir)
                try:
                    shutil.move(f.name, self.models_dir)
                except:
                    msg = file_exists_msg.format(f.name, self.models_dir)
                    if os.path.exists(f.name):
                        os.remove(f.name)
                finally:
                    self._leave_file_note(f.name, msg)

    def _leave_file_note(self, filename, mesg):
        with open(filename + '.txt', 'w') as fp:
            fp.write(mesg)

    def cleanup(self):
        pass


class BenchmarkIngest(object):

    """Operator for uploading benchmark datasets into PBS."""

    def __init__(self):
        pass
