"""Tests for the variables module."""

import os
import shutil
import json
from ConfigParser import SafeConfigParser
from nose.tools import assert_equal, assert_true, assert_false
from pbs_server.variables import (get_name, update_parameters,
                                  update_template)
from pbs_server import data_directory


variable_file = 'gpp_0.5x0.5.nc'
variable_name = 'gpp'
old_var = 'tas'
new_var = 'foo'
variables = [old_var, new_var]
old_tmpl_file = os.path.join(data_directory,
                             '{}.cfg.tmpl'.format(old_var))
old_tmpl_file_copy = '{}.copy'.format(old_tmpl_file)
new_tmpl_file = os.path.join(data_directory,
                             '{}.cfg.tmpl'.format(new_var))

parameters_file = os.path.join(data_directory, 'parameters.json')
with open(parameters_file, 'r') as fp:
    parameters = json.load(fp)


def setup_module():
    shutil.copy(old_tmpl_file, old_tmpl_file_copy)


def teardown_module():
    shutil.move(old_tmpl_file_copy, old_tmpl_file)
    os.remove(new_tmpl_file)


def test_get_name():
    name = get_name(variable_file)
    assert_equal(variable_name, name)


def test_update_parameters_pretest():
    for param in parameters:
        if param['key'] == '_variable1':
            assert_false(new_var in param['value']['choices'])


def test_update_parameters():
    update_parameters(parameters, variables)
    for param in parameters:
        if param['key'] == '_variable1':
            assert_true(old_var in param['value']['choices'])


def test_create_template():
    update_template(new_var, '{}.nc'.format(new_var))
    config = SafeConfigParser()
    config.read(new_tmpl_file)
    assert_true(config.has_section('PBS'))


def test_update_template():
    update_template(old_var, '{}.nc'.format(old_var))
    config = SafeConfigParser()
    config.read(old_tmpl_file)
    assert_true(config.has_section('PBS'))
