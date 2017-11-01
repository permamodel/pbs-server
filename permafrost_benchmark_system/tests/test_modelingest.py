"""Tests for the ModelIngest class."""

import os
import shutil
import yaml
from nose.tools import nottest, assert_true, assert_equal
from permafrost_benchmark_system.ingest import ModelIngest


ingest_file = 'test_ingest.yaml'
model_file = 'test_model.txt'
note_file = model_file + '.txt'
tmp_dir = 'tmp'


@nottest
def make_test_files():
    with open(model_file, 'w') as fp:
        fp.write('This is a test model output file.\n')
    cfg = {'ingest_files': [model_file], 'make_public': True}
    with open(ingest_file, 'w') as fp:
        yaml.safe_dump(cfg, fp, default_flow_style=False)


def setup_module():
    make_test_files()
    os.mkdir(tmp_dir)


def teardown_module():
    shutil.rmtree(tmp_dir)
    for f in [ingest_file, model_file, note_file]:
        try:
            os.remove(f)
        except:
            pass


def test_init():
    x = ModelIngest()
    assert_true(isinstance(x, ModelIngest))


def test_init_with_models_dir():
    x = ModelIngest(models_dir=tmp_dir)
    assert_true(isinstance(x, ModelIngest))
    assert_equal(x.models_dir, tmp_dir)


def test_load():
    x = ModelIngest()
    x.load(ingest_file)
    assert_equal(x.ingest_files[0].name, model_file)


def test_init_with_ingest_file():
    x = ModelIngest(ingest_file=ingest_file)
    assert_true(isinstance(x, ModelIngest))
    assert_equal(x.ingest_files[0].name, model_file)


def test_set_models_dir():
    x = ModelIngest()
    x.models_dir = tmp_dir
    assert_equal(x.models_dir, tmp_dir)


def test_validate():
    pass


def test_leave_file_note():
    x = ModelIngest()
    msg = 'Hi there'
    x._leave_file_note(model_file, msg)
    assert_true(os.path.isfile(note_file))


def test_move_file_new():
    x = ModelIngest()
    x.load(ingest_file)
    x.validate()
    x.move(tmp_dir)
    assert_true(os.path.isfile(os.path.join('tmp', model_file)))
    assert_true(os.path.isfile(note_file))


def test_move_file_exists():
    make_test_files()
    x = ModelIngest()
    x.load(ingest_file)
    x.validate()
    x.move(tmp_dir)
    assert_true(os.path.isfile(os.path.join('tmp', model_file)))
    assert_true(os.path.isfile(note_file))


def test_cleanup():
    pass
