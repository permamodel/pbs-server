"""Tests for the IlambConfigFile class."""
import numpy as np
from nose.tools import raises, assert_true, assert_false, assert_equal
from ConfigParser import SafeConfigParser
from permafrost_benchmark_system.file import IlambConfigFile
from permafrost_benchmark_system import data_directory


default_config_file = 'ilamb.cfg'


@raises(TypeError)
def test_init_no_parameters():
    x = IlambConfigFile()


def test_init_string_variable():
    param = 'gpp'
    x = IlambConfigFile(param)
    assert_true(type(x.variables), tuple)


def test_init_list_variable():
    param = ['gpp']
    x = IlambConfigFile(param)
    assert_true(type(x.variables), list)


def test_init_tuple_variable():
    param = ('gpp',)
    x = IlambConfigFile(param)
    assert_true(type(x.variables), tuple)


def test_init_array_variable():
    param = np.array(('gpp',))
    x = IlambConfigFile(param)
    assert_true(type(x.variables), np.ndarray)


def test_init_multiple_variables():
    param = ('gpp', 'lai', 'le')
    x = IlambConfigFile(param)
    assert_equal(len(x.variables), len(param))


def test_config_file_default():
    param = 'gpp'
    x = IlambConfigFile(param)
    assert_equal(x.config_file, default_config_file)


def test_config_file_user():
    param = 'gpp'
    config_file = 'foo.cfg'
    x = IlambConfigFile(param, config_file=config_file)
    assert_equal(x.config_file, config_file)


def test_relationships_default():
    param = 'gpp'
    x = IlambConfigFile(param)
    assert_false(x.has_relationships)


def test_relationships_user():
    param = 'gpp'
    x = IlambConfigFile(param, relationships=True)
    assert_true(x.has_relationships)


def test_setup():
    param = 'gpp'
    x = IlambConfigFile(param)
    x.setup()
    assert_true(isinstance(x.config[param], SafeConfigParser))


