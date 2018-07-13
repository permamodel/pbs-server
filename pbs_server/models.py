"""Perform operations on models used in PBS."""

model_template = { "group": { "name": "pbs_models_group", "members":
    1, "leader": False }, "name": "{model_name}", "global": False,
    "value": { "default": "Off", "type": "choice", "choices": [ "On",
    "Off" ] }, "visible": True, "key": "_model_{model_name}",
    "description": "{model_name}" }


def get_name(pbs_file):
    """
    Extract the model name from a CMIP5-compatible filename.

    Parameters
    ----------
    pbs_file : str
      A filename that obeys the CMIP5 standard.

    Returns
    -------
    str
      The name of the model.

    """
    parts = pbs_file.split('_')
    name = parts[2]
    return name


def is_key_in_pbs_group(parameters, key):
    """
    Determine whether a model is listed in the PBS models group.

    Parameters
    ----------
    parameters : dict
      The contents of the ILAMB `parameters.json` file.
    key : str
      The value of the `key` attribute of a WMT parameter.

    Returns
    -------
    bool
      True if the model is in the PBS models group.

    """
    for param in parameters:
        if 'group' in param.keys():
            if param['group']['name'] == 'pbs_models_group':
                if param['key'] == key:
                    return True
    return False


def update_parameters(parameters, models):
    """
    Adds model names to the PBS group in the set of ILAMB parameters.

    Parameters
    ----------
    parameters : dict
      The contents of the ILAMB `parameters.json` file.
    models : list
      A list of model names whose output has been uploaded into the PBS.

    Notes
    -----
    The parameters list is updated by reference.

    """
    for index, param in enumerate(parameters):
        if param['key'] == '_pbs_models':
            pbs_group_header = param
            pbs_group_index = index

    for model in models:
        key = '_model_{model}'.format(model=model)
        if not is_key_in_pbs_group(parameters, key):
            entry = model_template.copy()
            entry['key'] = key
            entry['name'] = model
            entry['description'] = model
            pbs_group_header['group']['members'] += 1
            pbs_group_index += 1
            parameters.insert(pbs_group_index, entry)
