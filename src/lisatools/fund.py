import datetime
from collections import namedtuple


Fund = namedtuple(
    "Fund",
    ["symbol", "description", "asset_class", "price", "date"],
    defaults=["DEFAULT", "Default fund", "NA", 1.0, datetime.date.today()]
    )
