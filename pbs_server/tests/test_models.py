"""Tests for the models module."""

import os
import json
from nose.tools import raises, assert_equal, assert_true, assert_false
from pbs_server.models import (get_model_name, is_key_in_pbs_group,
                               update_parameters)
from pbs_server import data_directory


pbs_file_good = 'gpp_Lmon_MPI-ESM-LR_historical_r3i1p1_185001-200512.nc'
model_name = 'MPI-ESM-LR'
pbs_file_bad = 'mlab.20141019.cdf'
model_present = '_model_SiBCASA'
model_absent = '_model_foobarbaz'
models = ['CLM4VIC', 'ISAM', 'PBS-test', 'SiBCASA']
model_added = '_model_ISAM'


parameters_file = os.path.join(data_directory, 'parameters.json')
with open(parameters_file, 'r') as fp:
    parameters = json.load(fp)


def test_get_model_name_pass():
    name = get_model_name(pbs_file_good)
    assert_equal(model_name, name)


@raises(IndexError)
def test_get_model_name_fail():
    name = get_model_name(pbs_file_bad)


def test_key_in_pbs_group():
    r = is_key_in_pbs_group(parameters, model_present)
    assert_true(r)


def test_key_not_in_pbs_group():
    r = is_key_in_pbs_group(parameters, model_absent)
    assert_false(r)


def test_update_parameters():
    update_parameters(parameters, models)
    r = is_key_in_pbs_group(parameters, model_added)
    assert_true(r)
