"""Perform operations on benchmark data uploaded through PBS."""

import os


def get_variable_name(pbs_file):
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
