"""Verify that ingest files follow the CMIP5 standard format."""

from netCDF4 import Dataset


class VerificationError(Exception):

    def __init__(self, msg):
        self.msg = ': '.join([type(self).__name__, msg])

    def __str__(self):
        return self.msg


class VerificationTool(object):
    """
    Tool for verifying that files are CMIP5-compatible.

    Notes
    -----
    filename = <variable name>_<MIP table>_<model>_<experiment>_<ensemble
member>[_<temporal subset>].nc

    An example:
      tas_Amon_HADCM3_ historical_r1i1p1_185001-200512.nc

    """
    def __init__(self, ingest_file):
        self.file = ingest_file
        self.parts = []
        self.variable_name = None
        self.mip_table = None
        self.model_name = None
        self.experiment = None
        self.ensemble_member = None
        self.temporal_subset = None

    def is_netcdf(self):
        try:
            Dataset(self.file.name)
        except IOError as e:
            raise VerificationError(e.message)

    def is_netcdf3_data_model(self):
        d = Dataset(self.file.name)
        if not d.data_model in ['NETCDF3_CLASSIC', 'NETCDF4_CLASSIC']:
            msg = 'NetCDF: File must use classic data model'
            raise VerificationError(msg)

    def parse_filename(self):
        self.parts = self.file.name.split('_')

    def filename_has_model_name(self):
        try:
            self.model_name = self.parts[2]
        except IndexError:
            msg = 'Model name not found'
            raise VerificationError(msg)

    def verify(self):
        self.is_netcdf()
        self.is_netcdf3_data_model()
        self.parse_filename()
        self.filename_has_model_name()
