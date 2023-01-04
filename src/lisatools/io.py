from lisatools.fund import ETF, Fund
from lisatools.portfolio import Holding

import datetime
import json


class JSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.parse_dict, **kwargs)

    def parse_dict(self, d):
        if "fund" in d:
            # assume it's a Holding
            return Holding.from_dict(d)
        elif "ISIN" in d:
            if "ticker" in d:
                # assume it's an ETF
                return ETF.from_dict(d)
            else:
                # assume it's a regular Fund
                return Fund.from_dict(d)
        else:
            return d


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        try:
            d = obj.as_dict()
        except AttributeError:
            d = super().default(obj)
        return d
