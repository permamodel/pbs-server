"""The `variables` module contains routines for updating the
*parameters.json* file of the ILAMB component in PBS.

"""
import os
import bisect
from ConfigParser import SafeConfigParser
from . import data_directory


pbs_data_dir = os.path.join('DATA-by-project', 'PBS')


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


def update_template(variable_name, file_name):
    """Create or update the *.cfg.tmpl* file for a variable.

    Parameters
    ----------
    variable_name : str
      A CMIP5 short variable name.
    file_name : str
      The path to the file on the PBS server.

    """
    base_file = variable_name + '.cfg.tmpl'
    tmpl_file = os.path.join(data_directory, base_file)
    tmpl_file_exists = os.path.exists(tmpl_file)
    config_update = SafeConfigParser()

    # If the file is new, add an [h2] entry.
    if not tmpl_file_exists:
        h2_section = 'h2: {}'.format(variable_name)
        config_update.add_section(h2_section)
        config_update.set(h2_section, 'variable', '"{}"'.format(variable_name))

    config_existing = SafeConfigParser()
    if tmpl_file_exists:
        config_existing.read(tmpl_file)

    # If a [PBS] entry doesn't exist, make it.
    pbs_section = 'PBS'
    if not config_existing.has_section(pbs_section):
        config_update.add_section(pbs_section)
        config_update.set(pbs_section, 'source',
                          '"{}"'.format(os.path.join(pbs_data_dir, file_name)))

    with open(tmpl_file, 'a') as fp:
        config_update.write(fp)
