"""Perform ingest operations in PBS."""
import os
import shutil
import yaml
from .file import IngestFile


models_dir = '/nas/data/tmp'
file_exists_msg = '''# File Exists\n
The file `{1}/{0}` already exists in the PBS data store.
The file has not been updated.
'''
file_moved_msg = '''# File Moved\n
The file `{}` has been moved to `{}` in the PBS data store.
'''


class ModelIngest(object):

    """Operator for uploading model outputs into PBS."""

    def __init__(self, ingest_file=None):
        self.ingest_files = []
        self.make_public = True
        if ingest_file is not None:
            self.load(ingest_file)

    def load(self, ingest_file):
        with open(ingest_file, 'r') as fp:
            cfg = yaml.safe_load(fp)
        for f in cfg['ingest_files']:
            self.ingest_files.append(IngestFile(f))
        self.make_public = cfg['make_public']

    def validate(self):
        for f in self.ingest_files:
            f.is_valid = True

    def move(self):
        for f in self.ingest_files:
            if f.is_valid:
                msg = file_moved_msg.format(f.name, models_dir)
                try:
                    shutil.move(f.name, models_dir)
                except:
                    msg = file_exists_msg.format(f.name, models_dir)
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
