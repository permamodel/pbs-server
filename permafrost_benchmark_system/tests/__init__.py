"""Unit tests for the permafrost_benchmark_system package."""

import os
import yaml


ingest_file = 'test_ingest.yaml'
model_file = 'test_model.txt'
note_file = model_file + '.txt'
tmp_dir = 'tmp'


def make_test_files():
    """
    Creates sample files for testing.
    """
    with open(model_file, 'w') as fp:
        fp.write('This is a test model output file.\n')

    cfg = dict()
    cfg['ilamb_root'] = os.getcwd()
    cfg['dest_dir'] = tmp_dir
    cfg['ingest_files'] = [model_file]
    cfg['make_public'] = True
    with open(ingest_file, 'w') as fp:
        yaml.safe_dump(cfg, fp, default_flow_style=False)
