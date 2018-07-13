"""Tests for the variables module."""

from nose.tools import assert_equal
from pbs_server.variables import get_name


variable_file = 'gpp_0.5x0.5.nc'
variable_name = 'gpp'


def test_get_name():
    name = get_name(variable_file)
    assert_equal(variable_name, name)
