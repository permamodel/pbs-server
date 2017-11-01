"""Tests for the ModelIngest class."""

import os
import shutil
from nose.tools import nottest, assert_true, assert_equal
from permafrost_benchmark_system.ingest import ModelIngest
from . import (ingest_file, model_file, note_file, tmp_dir,
               make_test_files)


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


def test_verify():
    pass


def test_leave_file_note():
    x = ModelIngest()
    msg = 'Hi there'
    x._leave_file_note(model_file, msg)
    assert_true(os.path.isfile(note_file))


def test_move_file_new():
    x = ModelIngest(models_dir=tmp_dir)
    x.load(ingest_file)
    x.verify()
    x.move()
    assert_true(os.path.isfile(os.path.join(tmp_dir, model_file)))
    assert_true(os.path.isfile(note_file))


def test_move_file_exists():
    make_test_files()
    x = ModelIngest(models_dir=tmp_dir)
    x.load(ingest_file)
    x.verify()
    x.move()
    assert_true(os.path.isfile(os.path.join('tmp', model_file)))
    assert_true(os.path.isfile(note_file))
