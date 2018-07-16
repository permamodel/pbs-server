"""Perform operations on benchmark data uploaded through PBS."""

import os
import bisect


def get_name(pbs_file):
    """
    Extract the CMIP5 short variable name from a benchmark data filename.

    Parameters
    ----------
    pbs_file : str
      A filename that looks like other ILAMB data filenames.

    Returns
    -------
    str
      The name of the variable.

    """
    base, ext = os.path.splitext(pbs_file)
    parts = base.split('_')
    name = parts[0]
    return name


def update_parameters(parameters, variables):
    """
    Adds new variable names the set of ILAMB parameters.

    Parameters
    ----------
    parameters : list
      The contents of the ILAMB `parameters.json` file.
    variables : list
      A list of CMIP5 short variable names.

    Notes
    -----
    The parameters list is updated by reference.

    """
    variable_list_keys = ['_variable' + str(i) for i in range(1,4)]
    for param in parameters:
        for variable_list_key in variable_list_keys:
            if param['key'] == variable_list_key:
                for variable in variables:
                    if variable not in param['value']['choices']:
                        bisect.insort(param['value']['choices'], variable)
