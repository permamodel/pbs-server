"""Perform ingest operations in PBS."""
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


class BenchmarkIngest(object):

    """Operator for uploading benchmark datasets into PBS."""

    def __init__(self):
        pass
