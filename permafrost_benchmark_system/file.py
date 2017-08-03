"""Perform file operations in PBS."""

import os
from ConfigParser import SafeConfigParser
from . import data_directory


class IlambConfigFile(object):

    """Tool for generating an ILAMB config file."""

    def __init__(self,
                 variables=('gpp',),
                 relationships=False,
                 config_file='ilamb.cfg'):

        """Set parameters for an ILAMB config file.

        Parameters
        ----------
        variables : array_like, required
            A string, list, or tuple of model output variables, using
            CMIP5 short names (e.g., *gpp*, not *Gross Primary
            Production*).
        relationships : boolean, optional
            Set to calculate dyadic relationships between the input
            variables (default is False).
        config_file : str, optional
            The name of the ILAMB config file (default is
            **ilamb.cfg**).

        Examples
        --------
        Set up and create an ILAMB config file for *gpp*:

        >>> f = IlambConfigFile('gpp')
        >>> f.write()

        """
        if type(variables) is str:
            self.variables = variables,
        else:
            self.variables = variables
        self.relationships = relationships
        self.config_file = config_file
        self.config = dict()
        for var in self.variables:
            self.config[var] = SafeConfigParser()
            self.read(var)

    def get_template_file(self, var_name):
        """Gets path to a variable's template file.

        Parameters
        ----------
        var_name : str
            The CMIP5 short name for a variable.

        """
        return os.path.join(data_directory, var_name + '.cfg.tmpl')

    def read(self, var_name):
        """Reads configuration information from a template file.

        Parameters
        ----------
        var_name : str
            The CMIP5 short name for a variable.

        """
        tmpl_file = self.get_template_file(var_name)
        self.config[var_name].read(tmpl_file)

    def write(self):
        """Writes an ILAMB config file."""
        with open(self.config_file, 'w') as fp:
            self._write_header(fp)
            for var in self.variables:
                self.config[var].write(fp)

    def _write_header(self, ofp):
        header_file = self.get_template_file('header')
        with open(header_file, 'r') as ifp:
            header = ifp.read()
        ofp.write(header + '\n')
