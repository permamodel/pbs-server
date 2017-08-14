"""Perform file operations in PBS."""

import os
import yaml
from ConfigParser import SafeConfigParser
from . import data_directory


class IlambConfigFile(object):

    """Tool for generating an ILAMB config file."""

    sources_file = os.path.join(data_directory, 'cmip5-variables.yaml')

    def __init__(self,
                 variables,
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
            Set to calculate relationships between the input variables
            (default is False).
        config_file : str, optional
            The name of the ILAMB config file (default is
            **ilamb.cfg**).

        Examples
        --------
        Set up and write an ILAMB config file for *gpp*:

        >>> f = IlambConfigFile('gpp')
        >>> f.setup()
        >>> f.write()

        """
        if type(variables) is str:
            self.variables = variables,
        else:
            self.variables = variables
        self.has_relationships = relationships
        self.sources = None
        self.config_file = config_file
        self.config = dict()

    def setup(self):
        """Generate settings for an ILAMB config file."""
        for var in self.variables:
            self.read(var)

        if self.has_relationships and len(self.variables) > 1:
            self.get_sources()
            self.add_relationships()

    def get_template_file(self, var_name):
        """Get path to a variable's template file.

        Parameters
        ----------
        var_name : str
            The CMIP5 short name for a variable.

        """
        return os.path.join(data_directory, var_name + '.cfg.tmpl')

    def read(self, var_name):
        """Read configuration information from a template file.

        Parameters
        ----------
        var_name : str
            The CMIP5 short name for a variable.

        """
        tmpl_file = self.get_template_file(var_name)
        self.config[var_name] = SafeConfigParser()
        self.config[var_name].read(tmpl_file)

    def get_sources(self):
        """Load long name and benchmark source info for all variables."""
        with open(self.sources_file, 'r') as fp:
            self.sources = yaml.safe_load(fp)

    def add_relationships(self):
        """Add all relationships for a variable."""
        for var in self.variables:
            all_vars = list(self.variables)
            all_vars.pop(all_vars.index(var))
            relations = _make_relationships(all_vars)
            if len(all_vars) > 1:
                rel_string = ','.join(relations)
            else:
                rel_string = relations[0]
            self.config[var].set(self.sources[var]['benchmark_source'],
                                 'relationships', rel_string)

    def write(self):
        """Write an ILAMB config file."""
        with open(self.config_file, 'w') as fp:
            self._write_header(fp)
            for var in self.variables:
                self.config[var].write(fp)

    def _write_header(self, ofp):
        header_file = self.get_template_file('header')
        with open(header_file, 'r') as ifp:
            header = ifp.read()
        ofp.write(header + '\n')

    def _make_relationships(self, var_list):
        relations = list()
        for var in var_list:
            src = '/'.join([self.sources[var]['long_name'],
                            self.sources[var]['benchmark_source']])
            relations.append('"' + src + '"')
        return relations
