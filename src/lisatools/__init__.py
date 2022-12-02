# read version from installed package
from importlib.metadata import version

__version__ = version("lisatools")


# populate package namespace
from lisatools.fund import Fund, ETF
from lisatools.portfolio import Holding, Portfolio
