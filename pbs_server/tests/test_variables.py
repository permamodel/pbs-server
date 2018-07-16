"""Tests for the variables module."""

import os
import json
from nose.tools import assert_equal, assert_true, assert_false
from pbs_server.variables import get_name, update_parameters
from pbs_server import data_directory


variable_file = 'gpp_0.5x0.5.nc'
variable_name = 'gpp'
existing_var = 'tas'
new_var = 'nep'
variables = [existing_var, new_var]

parameters_file = os.path.join(data_directory, 'parameters.json')
with open(parameters_file, 'r') as fp:
    parameters = json.load(fp)


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
            assert_true(existing_var in param['value']['choices'])
