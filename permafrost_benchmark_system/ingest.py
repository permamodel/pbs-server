"""Perform ingest operations in PBS."""
import os
import shutil
import yaml
from .file import IngestFile


models_dir = '/nas/data/tmp'


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
                try:
                    shutil.move(f.name, models_dir)
                except:
                    _leave_file_exists_note(f.name)
                    os.remove(f.name)
                else:
                    _leave_file_moved_note(f.name)

    def _leave_file_exists_note(self, filename):
        msg = '''# File Exists\n
The file `{1}/{0}` already exists in the PBS data store. The file has not been updated.
'''.format(filename, models_dir)
        with open(filename + '.txt', 'w') as fp:
            fp.write(msg)

    def _leave_file_moved_note(self, filename):
        msg = '''# File Moved\n
The file `{}` has been moved to `{}` in the PBS data store.
'''.format(filename, models_dir)
        with open(filename + '.txt', 'w') as fp:
            fp.write(msg)

    def cleanup(self):
        pass

class BenchmarkIngest(object):

    """Operator for uploading benchmark datasets into PBS."""

    def __init__(self):
        pass
