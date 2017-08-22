"""Tests for the file module, minus the IlambConfigFile class."""

import os
from nose.tools import raises, assert_true, assert_false, assert_equal
from permafrost_benchmark_system.file import get_region_labels_txt
from permafrost_benchmark_system import data_directory


regions_file_txt = 'tropics.txt'
regions_file_txt_path = os.path.join(data_directory, regions_file_txt)
labels = ['tropics', 'afritrop']


@raises(IOError)
def test_get_region_labels_txt_path():
    x = get_region_labels_txt(regions_file_txt)


def test_get_region_labels_txt_type():
    x = get_region_labels_txt(regions_file_txt_path)
    assert_true(type(x), list)


def test_get_region_labels_txt_value():
    x = get_region_labels_txt(regions_file_txt_path)
    assert_equal(x, labels)
