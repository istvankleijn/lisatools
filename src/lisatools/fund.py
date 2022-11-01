import datetime
from collections import namedtuple


Fund = namedtuple(
    "Fund",
    ["symbol", "description", "asset_class", "price", "date"],
    defaults=["DEFAULT", "Default fund", "NA", 1.0, datetime.date.today()]
    )


# class Fund:
#     """A collection of information about a single tradeable fund"""
#     def __init__(self):
#         self.symbol = 
#         self.description = 
#         self.asset_class = 
