import datetime
from collections import namedtuple


class Fund:
    """
    Details of a fund, including its current market price.
    
    Attributes
    ----------
    description : str
        Description of the fund, for example the name given by its provider.
    price : float
        Latest market price available for the fund.
    isin : str or None
        If a real fund, the International Securities Identification Number
        (ISIN) of the fund, otherwise None.
        The ISIN is a unique 12-character alphanumerical identifier.
    date : datetime.date
        Date at which the `price` was last updated.
    
    Examples
    --------

    Constructing a Fund from a description and current price.
    
    >>> f = lisatools.Fund("FTSE Global All Cap Index Fund", 170.14)

    Constructing a Fund with all optional details.

    >>> f = lisatools.Fund("FTSE Global All Cap Index Fund", 170.14,
    ...                    isin="GB00BD3RZ582",
    ...                    date=datetime.date(2022, 11, 1))
    """

    def __init__(self,
                 description="Default fund",
                 price=1.0,
                 *,
                 isin=None,
                 date=datetime.date.today()):
        self.description = description        
        self.isin = isin       
        self.update_price(price, date=date)
    
    def update_price(self, price, *, date=datetime.date.today()):
        """Set the price of the fund to the given value. Specify the date when
        the fund had the given price by the keyword `date`. If left unspecified,
        set the date to today.
        """
        self.price = price
        self.date = date
